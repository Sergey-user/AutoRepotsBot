import datetime
import uuid
import pyqiwi

from settings.bot_settings import QIWI_TOKEN, QIWI_WALLET, QIWI_P_PUBLIC

wallet = pyqiwi.Wallet(token=QIWI_TOKEN, number=QIWI_WALLET)

class NotEnoughMoney(Exception):
    pass

class NotPaymentFound(Exception):
    pass


class Payment():
    id: str = None
    amount: int

    async def create(self, amount: int):
        self.id = str(uuid.uuid4())
        self.amount = amount

    async def check_payment(self):
        start_date = datetime.datetime.now() - datetime.timedelta(days=2)
        transactions = wallet.history(start_date=start_date).get('transactions')
        for transaction in transactions:
            if transaction.comment:
                if str(self.id) in transaction.comment:
                    if int(transaction.total.amount) >= int(self.amount):
                        return True
                    else:
                        raise NotEnoughMoney
        else:
            return False


    async def get_invoice_link(self):
        link = 'https://oplata.qiwi.com/create?publicKey={pubkey}&amount={amount}&comment={comment}'
        return link.format(pubkey=QIWI_P_PUBLIC, amount=self.amount, comment=self.id)
