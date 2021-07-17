from aiogram.dispatcher.filters.state import StatesGroup, State

class ExpertPanelState(StatesGroup):
    in_expert_menu = State()

class ExpertWithdrawalState(StatesGroup):
    waiting_amount = State()

class AddReportState(StatesGroup):
    waiting_VIN = State()
    waiting_auto_number = State()
    waiting_VIN_photo = State()
    waiting_odometer_data = State()
    waiting_vehicle_condition = State()
    waiting_defects_photo = State()
    waiting_computer_diagnostics = State()
    waiting_checking_databases = State()
    waiting_defects_description = State()
    waiting_voice = State()
    dele = State()
    # waiting_price = State()