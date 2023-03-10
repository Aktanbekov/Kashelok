from django.utils.crypto import get_random_string

from core.settings import NIKITA_LOGIN, NIKITA_PASSWORD

from celery import shared_task
import xml.etree.cElementTree as ET
import requests


def send_request(xml):
    response = requests.post(
        'https://smspro.nikita.kg/api/message', data=xml.encode(
            'UTF-8'
        ), headers={'content-type': 'application/xml; charset=utf-8'}
    )
    return response


def check_status(response):
    resp = ET.fromstring(response.content)
    status_code = resp.find('.//status')
    failed = True
    if status_code == '0':
        message = 'success'
        failed = False
    elif status_code == '4':
        message = 'Пополните баланс Nikita.kg'
    else:
        message = 'Ошибка'
    return message, failed


@shared_task
def send_otp_to_phone(phone_number, message):
    message_id = get_random_string(8)
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    <message>
        <login>{NIKITA_LOGIN}</login>
        <pwd>{NIKITA_PASSWORD}</pwd>\n
        <id>{message_id}</id>
        <sender>Agameskg</sender>
        <text>{message}</text>
        <time></time>
        <phones>
            <phone>{phone_number}</phone>
        </phones>
    </message>'''

    response = send_request(xml=xml)
    check_status(response=response)
