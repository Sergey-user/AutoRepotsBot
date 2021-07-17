from peewee import PrimaryKeyField, CharField, IntegerField, FloatField, DateField, ForeignKeyField, ManyToManyField
from peewee import BooleanField
from peewee import DoesNotExist
from datetime import date

from database.db_connect import db
from database.BaseModel import BaseModel
from app.User.UserModels import UserModel


class ExpertModel(UserModel):
    balance = IntegerField(default=0)
    rating = FloatField()
    phone = CharField(null=True)
    FIO = CharField()
    is_admin = BooleanField(default=False)
    is_super_admin = BooleanField(default=False)
    is_blocked = BooleanField(default=False)

    async def block(self):
        await ExpertModel.connect_DB()
        self.is_blocked = True
        self.is_admin = False
        self.save()
        db.close()

    async def unblock(self):
        await ExpertModel.connect_DB()
        self.is_blocked = False
        self.save()
        db.close()

    async def update_balance(self, new_balance):
        await ExpertModel.connect_DB()
        self.balance = new_balance
        self.save()
        db.close()

    @classmethod
    async def get_super_admin(cls):
        await cls.connect_DB()
        super_admin = cls.get(cls.is_super_admin==True)
        db.close()
        return super_admin

    @classmethod
    async def find_by_tg_id_or_none(cls, tg_id):
        # db.connect(reuse_if_open=True)
        await cls.connect_DB()

        try:
            expert = cls.get(cls.tg_id==tg_id)
            db.close()
            return expert
        except DoesNotExist:
            db.close()
            return None

    @classmethod
    async def create_expert(cls, tg_id, tg_username=None, phone=None, FIO=None):
        # db.connect(reuse_if_open=True)
        await cls.connect_DB()

        expert = cls.create(
            tg_id=tg_id,
            tg_username=tg_username,
            phone=phone,
            rating=5.0,
            FIO=FIO,
        )
        return expert
        db.close()

    async def update_balance(self, new_balance):
        await ExpertModel.connect_DB()
        self.balance = new_balance
        self.save()
        db.close()

    async def update_rating(self):
        await ExpertModel.connect_DB()

        estimations_summ = 0
        estimations_count = 0
        for estimation in self.estimations:
            estimations_summ += estimation.estimate
            estimations_count += 1
        self.rating = estimations_summ / estimations_count
        self.save()

        db.close()

    @classmethod
    async def get_by_tg_username_or_none(cls, tg_username):
        await cls.connect_DB()

        try:
            expert = cls.get(cls.tg_username==tg_username)
            db.close()
            return expert
        except:
            db.close()
            return None

    @classmethod
    async def get_by_phone_or_none(cls, phone):
        await cls.connect_DB()

        try:
            expert = cls.get(cls.phone==phone)
            db.close()
            return expert
        except:
            db.close()
            return None


    class Meta:
        db_table = 'experts'

class EstimationModel(BaseModel):
    expert = ForeignKeyField(ExpertModel, to_field='id', related_name='estimations')
    estimate = IntegerField()

    @classmethod
    async def add_expert_estimataion(cls, expert, estimate):
        await cls.connect_DB()
        cls.create(expert=expert, estimate=estimate)
        db.close()

    class Meta:
        db_table = 'estimations'


class AutoReportModel(BaseModel):
    VIN = CharField()
    auto_number = CharField()
    name = CharField(unique=True)
    create_date = DateField()
    archive_name = CharField(unique=True) # archives/'self.name'.zip
    expert = ForeignKeyField(ExpertModel, to_field='id', related_name='auto_reports')
    from_chat_id = IntegerField()
    message_id = IntegerField(default=0)

    @classmethod
    async def find_reports_by_auto_number_or_none(cls, auto_number):
        # db.connect(reuse_if_open=True)
        await cls.connect_DB()

        auto_number = auto_number.upper()
        intab = 'ABEKMHOPCTYX'
        outtab = 'АВЕКМНОРСТУХ'
        number = auto_number.maketrans(intab, outtab)

        auto_number = auto_number.translate(number).lower()

        try:
            reports = cls.select().where(cls.auto_number==auto_number)

            last_VIN = ''
            selects = []
            for report in reports:
                print(last_VIN)
                if report.VIN == last_VIN:
                    # print('TRUE' + report.VIN)
                    continue
                print(cls.select().where(cls.VIN==report.VIN))
                selects.append(cls.select().where(cls.VIN==report.VIN))
                last_VIN = report.VIN

            report_return_list = []
            for select in selects:
                for report in select:
                    report_return_list.append(report)

            db.close()
            return report_return_list
        except DoesNotExist:
            db.close()
            print(db.is_closed())

            return None

    async def user_is_buy(self, tg_id):
        await AutoReportModel.connect_DB()
        try:
            self.transactions.get(TransactionModel.client==tg_id)
            db.close()
        except:
            db.close()
            return False
        else:
            db.close()
            return True

    @classmethod
    async def get_expert_by_report_name_or_none(cls, report_name):
        await cls.connect_DB()

        try:
            report = cls.get(cls.name==report_name)
            db.close()
            return report.expert
        except:
            db.close()
            return None

    @classmethod
    async def get_by_VIN_or_none(cls, VIN):
        # db.connect(reuse_if_open=True)
        await cls.connect_DB()

        try:
            reports = cls.select().where(cls.VIN==VIN)
            db.close()
            return reports
        except DoesNotExist:
            db.close()
            return None

    async def check_expert(self, expert_tg_id):
        # db.connect(reuse_if_open=True)
        await AutoReportModel.connect_DB()

        if self.expert.tg_id == expert_tg_id:
            db.close()
            return True
        else:
            db.close()
            return False

    @classmethod
    async def delete_report(cls, report_id):
        await cls.connect_DB()
        report = cls.get(cls.id==report_id)
        name = report.name
        report.delete_instance()
        db.close()
        return name

    async def get_buy_count(self):
        await AutoReportModel.connect_DB()
        buy_count = TransactionModel.select().where(TransactionModel.report_name==self.name).count()
        db.close()
        return buy_count

    @classmethod
    async def get_by_name_or_none(cls, name):
        await cls.connect_DB()

        try:
            report = cls.get(cls.name==name)
            db.close()
            return report
        except:
            db.close()
            return None

    @classmethod
    async def create_report(cls, data):
        # db.connect(reuse_if_open=True)
        await cls.connect_DB()

        expert = cls.create(
            VIN=data['VIN'],
            auto_number=data['auto_number'],
            name=data['name'],
            create_date=date.today(),
            price=10,
            archive_name=data['archive_name'],
            expert=data['expert']
        )
        db.close()
        return expert

    class Meta:
        db_table = 'auto_reports'


class TransactionModel(BaseModel):
    client = CharField()
    expert = ForeignKeyField(ExpertModel, to_field='id', related_name='transactions')
    report_name = CharField()
    date = DateField()
    amount = IntegerField()

    @classmethod
    async def check_user_buy_report(cls, report, user_tg_id):
        await cls.connect_DB()
        try:
            cls.get(cls.report_name==report.name, cls.client==user_tg_id)
            db.close()
        except:
            db.close()
            return False
        else:
            db.close()
            return True

    @classmethod
    async def create_transaction(cls, client, expert, auto_report, amount):
        await cls.connect_DB()

        cls.create(
            client = client,
            expert = expert,
            report_name = auto_report,
            date = date.today(),
            amount = amount
        )

        db.close()

    @classmethod
    async def get_client_transactions(cls, client_tg_id):
        await cls.connect_DB()

        try:
            transactions = cls.select().where(cls.client==client_tg_id)
            db.close()
            return transactions
        except:
            db.close()
            return None

    class Meta:
        db_table = 'transactions'

class CommissionModel(BaseModel):
    change_date = DateField()
    amount = IntegerField(default=50)
    is_now = BooleanField()


    @classmethod
    async def create_new_now_commission(cls, amount):
        await cls.connect_DB()
        now_commission = await cls.get_now_commission()
        now_commission.is_now = False
        now_commission.save()

        new_now_commision = cls.create(amount=amount, is_now=True, change_date=date.today())
        db.close()

    @classmethod
    async def get_now_commission(cls):
        await cls.connect_DB()
        now_commission = cls.get(cls.is_now==True)
        db.close()
        return now_commission

    class Meta:
        db_table = 'commissions'

class ReportPriceModel(BaseModel):
    change_date = DateField()
    amount = IntegerField(default=50)
    is_now = BooleanField()


    @classmethod
    async def create_new_now_commission(cls, amount):
        await cls.connect_DB()
        now_commission = await cls.get_now_commission()
        now_commission.is_now = False
        now_commission.save()

        new_now_commision = cls.create(amount=amount, is_now=True, change_date=date.today())
        db.close()

    @classmethod
    async def get_now_commission(cls):
        await cls.connect_DB()
        now_commission = cls.get(cls.is_now==True)
        db.close()
        return now_commission

    class Meta:
        db_table = 'report_prices'

class WithdrawalModel(BaseModel):
    expert = ForeignKeyField(ExpertModel, to_field='id', related_name='withdrawals')
    date = DateField()
    amount = IntegerField()
    balance_before_withdrawal = IntegerField()

    @classmethod
    async def create_withdrawal(cls, expert, amount, balance_before_withdrawal):
        await cls.connect_DB()
        cls.create(
            expert = expert,
            date = date.today(),
            amount = amount,
            balance_before_withdrawal = balance_before_withdrawal
        )
        db.close()

    class Meta:
        db_table = 'withdrawals'


class YookassaApiKeys(BaseModel):
    shop_id = CharField()
    api_key = CharField()
    is_now = BooleanField()

    @classmethod
    async def get_now_api(cls):
        await cls.connect_DB()

        try:
            api = cls.get(cls.is_now==True)
            db.close()
            return api
        except:
            db.close()
            return None

# class TransactionCheckModel(BaseModel):
#     pay_id = CharField(unique=True)
#     client_tg_id = IntegerField()
#     report_from_user_tg_id = IntegerField()
#     report_message_id = IntegerField()
#     report_name = CharField()

# TransactionCheckModel.create_table()

# Expert_Estimation_through.set_model(Expert_Estimation_foreign)
# ExpertModel.create_table()
# EstimationModel.create_table()
# AutoReportModel.create_table()
#
# WithdrawalModel.create_table()
# CommissionModel.create_table()
#
# TransactionModel.create_table()
# ReportPriceModel.create_table()
# YookassaApiKeys.create_table()