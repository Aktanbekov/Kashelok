from .models import Payment

payment = Payment()


class UrlKassa24:
    BASE_URL = f"https://kassa24.kg/EntranceService/EntranceService.svc/f/"

    def get_base_url(self):
        BASE_URL = f"https://kassa24.kg/EntranceService/EntranceService.svc/f/"
        return BASE_URL

    def get_login(self):
        return Payment.login

    def get_password(self):
        return Payment.password

    connectiontest_url = "https://localhost/EntranceService/EntranceService.svc/f/connectiontest"  # Проверка связи

    # Проверка логина и пароля
    connectiontestauthcheck_url = f"{BASE_URL}connectiontestauthcheck?login={payment.login}&password={payment.password}"

    # Валидация возможности совершить платеж
    preexaminationpayment_url = f"{BASE_URL}preexaminationpayment?login={payment.login}&password={payment.password}&serviceId={payment.serviceId}&amount={payment.amount}"

    # Платеж
    def pay_url(self, local_id, service_id, requisite, amount):
        paymentasync_url = f"{self.get_base_url()}paymentasync?login={self.get_login()}&password={self.get_password()}&localId={local_id}&serviceId={service_id}&requisite={requisite}&amount={amount}"
        return paymentasync_url

    # Отмена платежа
    cancelpaymentsync_url = f"{BASE_URL}cancelpaymentsync?login={payment.login}&password={payment.password}&receiptId={payment.receiptId}"

    # Получение информации о клиенте
    getclientinfo_url = f"{BASE_URL}getclientinfo?login={payment.login}&password={payment.password}&serviceId={payment.serviceId}&requisite={payment.requisite}"

    # Проверка статуса платежей   #receipID можно не использовать
    def check_status_url(self, local_id, requisite):
        checkstatus_url = f"{self.get_base_url()}checkstatus?login={self.get_login()}&password={self.get_password()}&localId={local_id}&requisite={requisite}"
        return checkstatus_url

    # Информациа о балансе агента
    getpointinfo_url = f"{BASE_URL}getpointinfo?login={payment.login}&password={payment.password}&dateFrom={payment.dateFrom}&dateTo={payment.dateTo}"

    # Получение данных для отчёта
    getreportsdata_url = f"{BASE_URL}getreportsdata?login={payment.login}&password={payment.password}&reportID={payment.reportID}&receiptID={payment.receiptId}&requisite={payment.requisite}&dateFrom={payment.dateFrom}&dateTo={payment.dateTo}"

    # Получение списка операторов
    getoperators_url = (
        f"{BASE_URL}getoperators?login={payment.login}&password={payment.password}"
    )

    # Получение списка сервисов
    getservices_url = (
        f"{BASE_URL}getservices?login={payment.login}&password={payment.password}"
    )

    # Получение списка сервисов по ID сервиса и\или оператора
    getservicebyid_url = f"{BASE_URL}getservicebyid?login={payment.login}&password={payment.password}&operatorid={payment.serviceId}&serviceid={payment.serviceId}"

