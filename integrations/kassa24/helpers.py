# from .models import KassaPayment as Payment
from core.settings import KASSA_LOGIN, KASSA_PASSWORD


# payment = Payment()


class UrlKassa24:
    BASE_URL = f"https://kassa24.kg/EntranceService/EntranceService.svc/f/"

    def get_base_url(self):
        BASE_URL = f"https://kassa24.kg/EntranceService/EntranceService.svc/f/"
        return BASE_URL

    def get_login(self):
        return KASSA_LOGIN

    def get_password(self):
        return KASSA_PASSWORD

    def connectiontest_url(self):
        connectiontest_url = "https://localhost/EntranceService/EntranceService.svc/f/connectiontest"  # Проверка связи
        return connectiontest_url

    def pay_url(self, local_id, service_id, requisite, amount):
        paymentasync_url = f"{self.get_base_url()}paymentasync?login={self.get_login()}&password={self.get_password()}&localId={local_id}&serviceId={service_id}&requisite={requisite}&amount={amount}"
        return paymentasync_url

    # Проверка статуса платежей   #receipID можно не использовать
    def check_status_url(self, local_id, requisite):
        checkstatus_url = f"{self.get_base_url()}checkstatus?login={self.get_login()}&password={self.get_password()}&localId={local_id}&requisite={requisite}"
        return checkstatus_url





    # Проверка логина и пароля

    # Валидация возможности совершить платеж
    # preexaminationpayment_url = f"{BASE_URL}preexaminationpayment?login={get_login()}&password={get_login()}&serviceId={payment.serviceId}&amount={payment.amount}"

    connectiontestauthcheck_url = f"{get_base_url}connectiontestauthcheck?login={get_login}&password={get_password}"
    # Платеж

    # # Отмена платежа
    # cancelpaymentsync_url = f"{BASE_URL}cancelpaymentsync?login={get_login()}&password={payment.password}&receiptId={payment.receiptId}"
    #
    # # Получение информации о клиенте
    # getclientinfo_url = f"{BASE_URL}getclientinfo?login={get_login()}&password={payment.password}&serviceId={payment.serviceId}&requisite={payment.requisite}"
    #
    #
    # # Информациа о балансе агента
    # getpointinfo_url = f"{BASE_URL}getpointinfo?login={get_login()}&password={payment.password}&dateFrom={payment.dateFrom}&dateTo={payment.dateTo}"
    #
    # # Получение данных для отчёта
    # getreportsdata_url = f"{BASE_URL}getreportsdata?login={get_login()}&password={get_password()}&reportID={payment.reportID}&receiptID={payment.receiptId}&requisite={payment.requisite}&dateFrom={payment.dateFrom}&dateTo={payment.dateTo}"
    #
    # # Получение списка операторов
    # getoperators_url = (
    #     f"{BASE_URL}getoperators?login={get_login()}&password={get_password()}"
    # )
    #
    # # Получение списка сервисов
    # getservices_url = f"{BASE_URL}getservices?login={get_login()}&password={get_password()}"
    #
    # # Получение списка сервисов по ID сервиса и\или оператора
    # getservicebyid_url = f"{BASE_URL}getservicebyid?login={get_login()}&password={get_login()}&operatorid={}&serviceid={payment.serviceId}"
