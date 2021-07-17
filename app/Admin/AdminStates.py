from aiogram.dispatcher.filters.state import StatesGroup, State


class FindExpertState(StatesGroup):
    waiting_tg_id = State()

class AdminPanelState(StatesGroup):
    in_main_menu = State()
    in_expert_menu = State()

class AddExpertState(StatesGroup):
    waiting_forward = State()
    waiting_phone = State()
    waiting_FIO = State()

class ChangeCommissionState(StatesGroup):
    waiting_amount = State()
    waiting_new_report_price = State()

class DeleteReportState(StatesGroup):
    waiting_name = State()
    waiting_confirm = State()

class ExpertWithdrawalState(StatesGroup):
    waiting_new_expert_balance = State()


class YookassaApiState(StatesGroup):
    shop_id = State()
    api_key = State()


class AgreementState(StatesGroup):
    file = State()