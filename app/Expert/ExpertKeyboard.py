from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from aiogram.utils.callback_data import CallbackData

from app.texts import KEYBOARD
from app.BaseKeyboard import BaseKeyboard
from app.Admin.AdminKeyboard import AdminKeyboard


class ExpertKeyboard(BaseKeyboard):
    add_report_cd: CallbackData
    my_account_cd: CallbackData
    my_reports_cd: CallbackData
    withdrawal_money_cd: CallbackData
    defects_photo_download_success_cd = CallbackData
    computer_diagnostics_download_success: CallbackData
    checking_databases_cd: CallbackData
    back_cd: CallbackData



    def __init__(self):
        super().__init__()
        self.add_report_cd = CallbackData('add_report_cd', 'expert_id')
        self.my_account_cd = CallbackData('my_account_cd', 'expert_id')
        self.my_reports_cd = CallbackData('my_reports_cd', 'expert_id')
        self.withdrawal_money_cd = CallbackData('withdrawal_money_cd', 'expert_id')
        self.defects_photo_download_success_cd = CallbackData('defects_photo_download_success_cd', 'proxy')
        self.computer_diagnostics_download_success = CallbackData('computer_diagnostics_download_success', 'proxy')
        self.checking_databases_cd = CallbackData('checking_databases_cd', 'proxy')
        self.back_cd = CallbackData('back_cd_expert', 'function_start')

    async def expert_menu_kb(self, expert_tg_id):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(
            await self.__get_add_report_btn(expert_tg_id),
            await self.__get_my_account_btn(expert_tg_id)
        )
        return key

    async def expert_menu_with_admin_kb(self, expert_tg_id):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(
            await self.__get_add_report_btn(expert_tg_id),
            await self.__get_my_account_btn(expert_tg_id),
            await self.__get_admin_panel_btn()
        )
        return key

    async def expert_my_account_menu_kb(self, expert_id, function_start, is_super_admin=False):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(await self.__get_my_reports_btn(expert_id))

        if not is_super_admin:
            key.insert(await self.__get_withdrawal_money_btn(expert_id))

        key.add(await self._get_back_btn(function_start))

        return key

    async def test(self):
        key = ReplyKeyboardMarkup(resize_keyboard=True)
        t = 'Продолжить   📥'
        btn = KeyboardButton(text=t)
        key.insert(btn)
        return key


    async def defects_photo_download_success_kb(self, function_start):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(await self.__get_defects_photo_download_success_btn())
        key.add(
            await self._get_back_btn(function_start=function_start),
            await self._get_main_menu_btn()
        )
        return key

    async def defects_photo_next_step(self, function_start):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(await self.__get_defects_photo_next_step_btn())
        key.add(
            await self._get_back_btn(function_start=function_start),
            await self._get_main_menu_btn()
        )
        return key

    async def computer_diagnostic_download_success_kb(self, function_start):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(await self.__get_computer_diagnostics_download_success_btn())
        key.add(
            await self._get_back_btn(function_start=function_start),
            await self._get_main_menu_btn()
        )
        return key

    async def computer_diagnostic_next_step(self, function_start):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(await self.__get_computer_diagnostic_next_step_btn())
        key.add(
            await self._get_back_btn(function_start=function_start),
            await self._get_main_menu_btn()
        )
        return key

    async def checking_databases_download_success_kb(self, function_start):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(await self.__get_checking_databases_download_success_btn())
        key.add(
            await self._get_back_btn(function_start=function_start),
            await self._get_main_menu_btn()
        )
        return key

    async def checking_databases_next_step(self, function_start):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(await self.__get_checking_databases_next_step_btn())
        key.add(
            await self._get_back_btn(function_start=function_start),
            await self._get_main_menu_btn()
        )
        return key

    async def add_report_back_main_menu_kb(self, function_start):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(
            await self._get_back_btn(function_start=function_start),
            await self._get_main_menu_btn()
        )
        return key

    async def only_main_menu_kb(self):
        key = InlineKeyboardMarkup()
        key.insert(await self._get_main_menu_btn())
        return key

    async def cancel_kb(self, function_start):
        key = InlineKeyboardMarkup()
        key.insert(await self.__get_cancel_btn(function_start))
        return key


    # Логика отдельных кнопок
    # ----------------------------------------------------------------------
    async def __get_cancel_btn(self, function_start):
        text = KEYBOARD['cancel']
        cd = self.back_cd.new(function_start=function_start)
        return await self._get_inline_btn(text, cd)

    async def __get_admin_panel_btn(self):
        text = KEYBOARD['find_report_admin_menu']['menu']
        admin_keyboard = AdminKeyboard()
        cd = admin_keyboard.admin_panel_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_checking_databases_download_success_btn(self):
        text = KEYBOARD['download_success']
        cd = self.checking_databases_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_checking_databases_next_step_btn(self):
        text = KEYBOARD['next_step']
        cd = self.checking_databases_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_defects_photo_download_success_btn(self):
        text = KEYBOARD['download_success']
        cd = self.defects_photo_download_success_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_defects_photo_next_step_btn(self):
        text = KEYBOARD['next_step']
        cd = self.defects_photo_download_success_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_computer_diagnostics_download_success_btn(self):
        text = KEYBOARD['download_success']
        cd = self.computer_diagnostics_download_success.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_computer_diagnostic_next_step_btn(self):
        text = KEYBOARD['next_step']
        cd = self.computer_diagnostics_download_success.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_my_reports_btn(self, expert_id):
        text = KEYBOARD['expert_my_account_menu']['my_reports']
        cd = self.my_reports_cd.new(expert_id=expert_id)
        return await self._get_inline_btn(text=text, callback_data=cd)

    async def __get_withdrawal_money_btn(self, expert_id):
        text = KEYBOARD['expert_my_account_menu']['withdrawal_money']
        cd = self.withdrawal_money_cd.new(expert_id=expert_id)
        return await self._get_inline_btn(text=text, callback_data=cd)

    async def __get_my_account_btn(self, expert_id):
        text = KEYBOARD['find_report_expert_menu']['my_account']
        cd = self.my_account_cd.new(expert_id=expert_id)
        btn = await self._get_inline_btn(text, cd)
        return btn

    async def __get_add_report_btn(self, expert_id):
        text = KEYBOARD['find_report_expert_menu']['add_report']
        cd = self.add_report_cd.new(expert_id=expert_id)
        btn = await self._get_inline_btn(text, cd)
        return btn
    # ----------------------------------------------------------------------
