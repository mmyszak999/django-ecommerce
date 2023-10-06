from django.utils import timezone

def payment_deadline_calc():
    return timezone.now() + timezone.timedelta(+5)