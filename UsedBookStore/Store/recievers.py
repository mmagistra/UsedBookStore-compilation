from datetime import datetime, timedelta

from django.dispatch import receiver

from Store.signals import book_instance_reserved
from Store.tasks import task_cancel_reservation


@receiver(book_instance_reserved)
def book_instance_reserved(sender, book_instance, profile, reserve_expiration_datetime: datetime, **kwargs):
    # print(f"Book instance {book_instance} reserved by {profile} until {reserve_expiration_datetime}")
    # if datetime.now() - reserve_expiration_datetime < timedelta(minutes=30):
    #     result = task_cancel_reservation.apply_async(
    #         kwargs={
    #             'book_instance_id': book_instance.pk,
    #             'profile_id': profile.id
    #         },
    #         countdown=(reserve_expiration_datetime - datetime.now()).total_seconds()
    #     )
    # else:
    # result = task_cancel_reservation.apply_async(
    #     args=[book_instance.pk, profile.id],
    #     eta=reserve_expiration_datetime
    # )
    # print('Task scheduled')
    pass
