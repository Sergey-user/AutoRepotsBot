from yookassa import Configuration, Payment

from app.Expert.ExpertModels import YookassaApiKeys

# Configuration.account_id = '54401'
# Configuration.secret_key = 'test_Fh8hUAVVBGUGbjmlzba6TB0iyUbos_lueTHE-axOwM0'


# Набор утилит для оплаты
class YookassaPayment():

    @classmethod
    async def create_payment(cls, name, amount):
        await cls.__configuration_api()
        payment: Payment = Payment.create({
            "amount": {
                "value": amount,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me//zanosru_bot"
            },
            "capture": True,
            "description": name
        })

        return payment

    @classmethod
    async def check_payment_status(cls, id):
        await cls.__configuration_api()

        payment = Payment.find_one(id)
        return payment.status

    @classmethod
    async def __configuration_api(cls):
        now_yookassa_api: YookassaApiKeys = await YookassaApiKeys.get_now_api()

        Configuration.account_id = now_yookassa_api.shop_id
        Configuration.secret_key = now_yookassa_api.api_key