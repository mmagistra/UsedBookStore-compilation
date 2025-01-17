from datetime import datetime
from time import sleep

from celery import shared_task
from django.utils import timezone

from Store.models import BookInstance, Status, Profile


@shared_task
def task_cancel_reservation(book_instance_id, profile_id):
    print('task task_cancel_reservation started at ' + str(timezone.now()))
    # book_instance_id = int(book_instance_id)
    # book_instance = BookInstance.objects.get(pk=book_instance_id)
    # profile = Profile(pk=profile_id)
    # if book_instance.reserved_by_profile == profile:
    #     if book_instance.reserve_expiration_datetime and book_instance.reserve_expiration_datetime <= datetime.now():
    #         book_instance.status = Status.IN_STOCK
    #         book_instance.reserved_by_profile = None
    #         book_instance.reserve_expiration_datetime = None
    #         book_instance.save()
    #         print(f'Reservation of {book_instance} canceled')
    #     elif book_instance.reserve_expiration_datetime and book_instance.reserve_expiration_datetime > datetime.now():
    #         print('Task work too early!')
    #     else:
    #         print('Reservation already canceled')
    # else:
    #     print('Wrong profile')
    pass


@shared_task
def task_cancel_all_expired_reservations():
    print('task task_cancel_all_expired_reservations started at ' + str(timezone.now()))
    for book_instance in BookInstance.objects.filter(reserve_expiration_datetime__lt=timezone.now()):
        book_instance.status = Status.IN_STOCK
        book_instance.reserved_by_profile = None
        book_instance.reserve_expiration_datetime = None
        book_instance.save()
