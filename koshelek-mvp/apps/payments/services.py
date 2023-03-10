from apps.payments.models import Payment
import requests


def create_payment_object(user, local_id, status, **validate_data):
    payment = Payment.objects.create(
        user=user, local_id=local_id, status=status, **validate_data
    )
    return payment


def response_check_status_kassa24(kassa_obj, local_id, requisite):
    check_status_url = kassa_obj.check_status_url(
        local_id=local_id, requisite=requisite
    )
    response = requests.get(check_status_url)
    return response


def response_payment_to(kassa_obj, local_id, service_id, requisite, amount):
    pay_to_url = kassa_obj.pay_url(
        local_id=local_id,
        service_id=service_id,
        requisite=requisite,
        amount=amount,
    )
    response_pay = requests.get(pay_to_url)
    return response_pay
