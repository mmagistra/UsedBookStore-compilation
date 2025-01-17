import pprint
from datetime import datetime
from typing import List

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import QuerySet, Count, Min, Max, Q, OuterRef, Subquery, ForeignKey, F, PROTECT
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Store.models import (
    Profile,
    Book,
    BookInstance,
    Condition,
    Genre,
    Author,
    Publisher,
    Status,
)
from Store.permissions import DjangoModelPermissionsWithViewAll
from Store.serializers import (
    ProfileSerializer,
    UserSerializer,
    BookSerializer,
    BookInstanceSerializer,
    ConditionSerializer,
    GenreSerializer,
    AuthorSerializer,
    PublisherSerializer,
    CatalogSerializer,
    CatalogDetailSerializer,
    BookUpdateSerializer,
    GetReservedInstancesSerializer, UserSaveSerializer,
)
from Store.signals import book_instance_reserved
from UsedBookStore.settings import DEBUG, RESERVE_PERIOD

UserModel = get_user_model()


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [DjangoModelPermissions]


class UserViewSet(ModelViewSet):
    queryset = UserModel.objects.all()
    if DEBUG:
        serializer_class = UserSaveSerializer
    else:
        serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissionsWithViewAll]
    http_method_names = ['get']


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [DjangoModelPermissionsWithViewAll]


class BookInstanceViewSet(ModelViewSet):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    permission_classes = [DjangoModelPermissionsWithViewAll]


class ConditionViewSet(ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [DjangoModelPermissionsWithViewAll]


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissionsWithViewAll]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [DjangoModelPermissionsWithViewAll]


class PublisherViewSet(ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [DjangoModelPermissionsWithViewAll]


class CheckMediaUrl(TemplateView):
    template_name = 'Store/check_media_url.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(pk=self.kwargs['pk'])
        context['media_name'] = book.title
        context['media_url'] = book.cover.url
        return context


class CatalogView(APIView):
    permission_classes = [DjangoModelPermissionsWithViewAll]

    def get(self, request, *args, **kwargs):
        order_by = 'pk'
        min_degree_of_wear = Subquery(
            BookInstance.objects.values(
                'book__id',
            ).filter(
                status=Status.IN_STOCK,
                book=OuterRef('pk')
            ).annotate(
                minimal_degree_of_wear=Min('condition__degree_of_wear')
            ).values(
                'minimal_degree_of_wear'
            )
        )

        data: QuerySet = Book.objects.prefetch_related(
            'genres', 'authors', 'instances', 'publisher',
        ).filter(
            instances__status=Status.IN_STOCK
        ).annotate(
            count=Count('instances'),
            minPrice=Min('instances__sale_price'),
            maxPrice=Max('instances__sale_price'),
            min_degree_of_wear=Min('instances__condition__degree_of_wear'),
            bestCondition=Min(
                F('instances__condition__description'),
                filter=Q(instances__condition__degree_of_wear=min_degree_of_wear),
            ),
            # bestCondition=Min(
            #     F('instances__condition__description'),
            #     filter=Q(instances__condition__degree_of_wear=min_degree_of_wear),
            # ),
        ).order_by(
            order_by
        )
        result: List[dict] = []
        for book in data:
            result.append({
                'pk': book.pk,
                'title': book.title,
                'description': book.description,
                'cover': book.cover,
                'authors': [author.name for author in book.authors.all()],
                'genres': [genre.name for genre in book.genres.all()],
                'publisher': book.publisher.name,
                'published_year': book.published_year,
                'count': book.count,
                'minPrice': book.minPrice,
                'maxPrice': book.maxPrice,
                'bestCondition': book.bestCondition,
                'degree_of_wear': book.min_degree_of_wear
            })

        return Response(
            CatalogSerializer(
                result,
                many=True,
                context={
                    'request': request
                }
            ).data,
        )


class CatalogDetailView(APIView):
    permission_classes = [DjangoModelPermissionsWithViewAll]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']

        order_by = 'pk'

        min_degree_of_wear = Subquery(
            BookInstance.objects.values(
                'book__id',
            ).filter(
                status=Status.IN_STOCK,
                book=OuterRef('pk')
            ).annotate(
                minimal_degree_of_wear=Min('condition__degree_of_wear')
            ).values(
                'minimal_degree_of_wear'
            )
        )

        data: QuerySet = Book.objects.prefetch_related(
            'genres', 'authors', 'instances', 'publisher', 'instances__condition',
        ).filter(
            pk=pk,
        ).annotate(
            count=Count('instances'),
            minPrice=Min('instances__sale_price'),
            maxPrice=Max('instances__sale_price'),
            min_degree_of_wear=Min('instances__condition__degree_of_wear'),
            bestCondition=Min(
                'instances__condition__description',
                filter=Q(instances__condition__degree_of_wear=min_degree_of_wear)
            ),
        ).order_by(
            order_by
        )

        result: dict = {}
        for book in data:
            result = {
                'pk': book.pk,
                'title': book.title,
                'description': book.description,
                'cover': book.cover,
                'instances': [
                    {
                        "pk": instance.pk,
                        "condition": instance.condition,
                        "storage_cell": instance.storage_cell,
                        "purchase_price": instance.purchase_price,
                        "sale_price": instance.sale_price,
                        "status": instance.status,
                    }
                    for instance in book.instances.all()
                ],
                'authors': [author.name for author in book.authors.all()],
                'genres': [genre.name for genre in book.genres.all()],
                'publisher': book.publisher.name,
                'published_year': book.published_year,
                'count': book.count,
                'minPrice': book.minPrice,
                'maxPrice': book.maxPrice,
                'bestCondition': book.bestCondition,
                'degree_of_wear': book.min_degree_of_wear
            }

        return Response(
            CatalogDetailSerializer(
                result,
                many=False,
                context={
                    'request': request
                }
            ).data,
        )


# Reserve instance, cancel instance reservation and get reserved instances
class CancelReserveInstanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_instance_id = request.data.get('book_instance_pk')
        book_instance = BookInstance.objects.get(pk=book_instance_id)
        if book_instance.reserved_by_profile != request.user.profile:
            return Response(status=status.HTTP_403_FORBIDDEN)
        book_instance.status = Status.IN_STOCK
        book_instance.reserved_by_profile = None
        book_instance.reserve_expiration_datetime = None
        book_instance.save()
        return Response(status=status.HTTP_200_OK)


class ReserveInstanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_instance_id = request.data.get('book_instance_pk')
        book_instance = BookInstance.objects.get(pk=book_instance_id)
        book_instance.status = Status.RESERVED
        book_instance.reserved_by_profile = request.user.profile
        book_instance.reserve_expiration_datetime = timezone.now() + RESERVE_PERIOD
        book_instance.save()
        # book_instance_reserved.send(
        #     sender=self,
        #     book_instance=book_instance,
        #     profile=request.user.profile,
        #     reserve_expiration_datetime=book_instance.reserve_expiration_datetime
        # )
        return Response(status=status.HTTP_200_OK)


class GetReservedInstancesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        reserved_instances = BookInstance.objects.filter(status=Status.RESERVED, reserved_by_profile=profile)
        return Response(GetReservedInstancesSerializer(reserved_instances, many=True).data)


# Registration
class RegisterView(APIView):
    def post(self, request):
        data = {
            "username": request.data.get("username"),
            "password": request.data.get("password"),
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
        }
        serializer = UserSaveSerializer(data=data)
        if serializer.is_valid():
            try:
                user = UserModel.objects.create_user(**serializer.validated_data)
                user.save()
                profile = Profile(user=user)
                profile.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

