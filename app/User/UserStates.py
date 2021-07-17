from aiogram.dispatcher.filters.state import StatesGroup, State

class FindReportState(StatesGroup):
    waiting_VIN_or_autonumber = State()

class ExpertComplaintState(StatesGroup):
    waiting_complaint_text = State()
    waiting_phone = State()
