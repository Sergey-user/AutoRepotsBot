# from redis import StrictRedis


from app.BaseKeyboard import BaseKeyboard
from app.Expert.ExpertModels import ExpertModel
from app.Expert.ExpertKeyboard import ExpertKeyboard
from app.Admin.AdminKeyboard import AdminKeyboard
from app.Expert.ExpertRedis import ExpertRedis

from database.db_connect import db

class BaseHandler():
    redis: ExpertRedis

    def __init__(self):
        self.redis = ExpertRedis()

    async def _get_now_user_find_report_key(self, tg_id):
        expert = await ExpertModel.get_by_tg_id_or_none(tg_id)

        if expert and expert.is_admin:
            admin_keyboard = ExpertKeyboard()
            key = await admin_keyboard.expert_menu_with_admin_kb(expert.id)
        elif expert and not expert.is_admin and not expert.is_blocked:
            expert_keyboard = ExpertKeyboard()
            key = await expert_keyboard.expert_menu_kb(expert.id)
        else:
            key = None

        return key