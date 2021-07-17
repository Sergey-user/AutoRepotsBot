from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from app.texts import KEYBOARD


class BaseKeyboard():
    back_cd: CallbackData
    main_menu_cd: CallbackData

    def __init__(self):
        self.back_cd = CallbackData('back_cd', 'function_start')
        self.main_menu_cd = CallbackData('main_menu_cd', 'proxy')

    async def phone_kb(self):
        key = ReplyKeyboardMarkup()
        key.insert(await self._get_phone_btn())
        return key

    async def remove_kb(self):
        key = ReplyKeyboardRemove()
        return key

    async def _get_phone_btn(self):
        text = KEYBOARD['send_phone']
        btn = KeyboardButton(text, request_contact=True)
        return btn

    async def _get_back_btn(self, function_start):
        text = KEYBOARD['back']
        cd = self.back_cd.new(function_start=function_start)
        return await self._get_inline_btn(text, cd)

    async def _get_main_menu_btn(self):
        text = KEYBOARD['main_menu']
        cd = self.main_menu_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def _get_inline_btn(self, text, callback_data):
        return InlineKeyboardButton(text=text, callback_data=callback_data)