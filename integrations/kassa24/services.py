from apps.payment.models import Payment, Transaction
import requests
import uuid
import httpx


def create_payment_object(user, local_id, status, **validate_data):
    payment: Payment = Payment.objects.create(
        user=user.id, integration='kassa24', status=status, **validate_data
    )
    Transaction.objects.create(partner_id=local_id, payment_db=payment)

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
        amount=int(amount),
    )
    # response = httpx.get(pay_to_url)
    response = requests.get(pay_to_url)
    return response


def generate_uuid():
    return str(uuid.uuid4())
