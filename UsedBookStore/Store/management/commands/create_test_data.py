from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import IntegrityError
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from Store.models import Book, BookInstance, Genre, Author, Publisher, Condition, Profile
from django.contrib.auth.models import User, Group

from Store.management.data_sets.test_data import test_data as new_data

UserModel = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Creating test data')

        print('Creating admin if not exists')
        if UserModel.objects.filter(username='admin').exists():
            print('Admin already exists')
        else:
            print('Creating admin...')
            # Create a superuser
            User.objects.create_superuser(
                username='admin',
                email='lXK7t@example.com',
                password='admin',
            )
            print('Admin created')

        # Create a publisher

        test_data = new_data.copy()


        print('Creating authors, genres, publishers, conditions, users, profiles, books and book instances...')
        try:
            # Authors
            authors = [Author(name=author) for author in test_data['Authors']]
            Author.objects.bulk_create(authors)
            print('+ Authors created')
        except IntegrityError:
            print('- Authors already exist')

        try:
            # Genres
            genres = [Genre(name=genre) for genre in test_data['Genres']]
            Genre.objects.bulk_create(genres)
            print('+ Genres created')
        except IntegrityError:
            print('- Genres already exist')

        try:
            # Publishers
            publishers = [Publisher(name=publisher) for publisher in test_data['Publishers']]
            Publisher.objects.bulk_create(publishers)
            print('+ Publishers created')
        except IntegrityError:
            print('- Publishers already exist')

        try:
            # Conditions
            conditions = [Condition(**condition) for condition in test_data['Conditions']]
            Condition.objects.bulk_create(conditions)
            print('+ Conditions created')
        except IntegrityError:
            print('- Conditions already exist')

        try:
            # Users
            users = []
            for data in test_data['Users']:
                user = UserModel(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                )
                users.append(user)
            UserModel.objects.bulk_create(users)
            for i, user in enumerate(users):
                for group_name in test_data['Users'][i]['group']:
                    group = Group.objects.get(name=group_name)
                    user.groups.add(group)

            print('+ Users created')
        except IntegrityError as e:
            print('- Users already exist')

        try:
            # Profiles
            profiles = [
                Profile(
                    user=UserModel.objects.get(username=user['username'])
                )
                for user in test_data['Profiles']
            ]
            Profile.objects.bulk_create(profiles)
            print('+ Profiles created')
        except IntegrityError:
            print('- Profiles already exist')

        # Books
        try:
            # Books
            books = [
                Book(
                    title=book['title'],
                    description=book['description'],
                    cover='covers/default_cover.jpg',
                    publisher=Publisher.objects.get(name=book['publisher']),
                    published_year=book['published_year'],
                )
                for book in test_data['Books']
            ]
            Book.objects.bulk_create(books)
            for i, book in enumerate(books):
                for genre_name in test_data['Books'][i]['genres']:
                    genre = Genre.objects.get(name=genre_name)
                    book.genres.add(genre)
                for author_name in test_data['Books'][i]['authors']:
                    author = Author.objects.get(name=author_name)
                    book.authors.add(author)
            print('+ Books created')
        except IntegrityError:
            print('- Books already exist')

        # BookInstances
        try:
            for book_instance in test_data['BookInstances']:
                book = Book.objects.get(
                    title=book_instance['book']['title'],
                    publisher=Publisher.objects.get(name=book_instance['book']['publisher']),
                    published_year=book_instance['book']['published_year'],
                )
                condition = Condition.objects.get(degree_of_wear=book_instance['condition'])
                BookInstance.objects.create(
                    book=book,
                    condition=condition,
                    storage_cell=book_instance['storage_cell'],
                    purchase_price=book_instance['purchase_price'],
                    sale_price=book_instance['sale_price'],
                )
            print('+ BookInstances created')
        except IntegrityError:
            print('- BookInstances can not be created')

        try:
            if PeriodicTask.objects.filter(name='task_cancel_all_expired_reservations').exists():
                print('- Periodic task already exists')
            else:
                interval = IntervalSchedule.objects.create(every=1, period=IntervalSchedule.MINUTES)
                periodic_task = PeriodicTask.objects.create(
                    task='Store.tasks.task_cancel_all_expired_reservations',
                    name='task_cancel_all_expired_reservations',
                    description='Cancel all expired reservations',
                    interval=interval,
                )
                print('+ Periodic task created')
        except IntegrityError:
            print('- Periodic task can not be created')

        print('Done!')
