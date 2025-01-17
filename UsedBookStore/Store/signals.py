from django.dispatch import Signal

book_instance_reserved = Signal(['book_instance', 'user', 'reserve_expiration_datetime'])
