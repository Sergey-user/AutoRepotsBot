from aiogram.types import CallbackQuery

from app.BaseHandler import BaseHandler
from app.texts import MESSAGES
from app.BaseKeyboard import BaseKeyboard
from app.User.UserStates import FindReportState
from app.User.UserHandler import UserHandler
from app.Expert.ExpertHandler import ExpertHandler
from app.User.UserRedis import UserRedis


class StandartHandler(BaseHandler):
    keyboard: BaseKeyboard

    def __init__(self):
        self.keyboard = BaseKeyboard()

    @classmethod
    def register_handlers(cls, dp):
        handler = cls()

        dp.register_callback_query_handler(
            handler.main_menu,
            handler.keyboard.main_menu_cd.filter(),
            state='*'
        )
        # dp.register_callback_query_handler(
        #     handler.back,
        #     handler.keyboard.back_cd.filter(),
        #     state='*'
        # )

    async def main_menu(self, call: CallbackQuery, state=None):
        await call.message.delete()

        if state:
            await state.finish()

        # await FindReportState.waiting_VIN_or_autonumber.set()

        if call.message.reply_markup:
            rm_key = await self.keyboard.remove_kb()
            m = await call.message.answer('a', reply_markup=rm_key)
            await m.delete()

        key = await self._get_now_user_find_report_key(call.from_user.id)
        message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

        user_redis = UserRedis()
        await user_redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

        expert_handler: ExpertHandler = ExpertHandler()
        await expert_handler.delete_state_redis_data(call.from_user.id)

        await call.answer()

