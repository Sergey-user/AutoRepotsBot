from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from app.texts import KEYBOARD
from app.BaseKeyboard import BaseKeyboard


class UserKeyboard(BaseKeyboard):
    buy_report_cd: CallbackData
    download_report_cd: CallbackData
    add_report_cd: CallbackData
    my_account_cd: CallbackData
    admin_menu_cd: CallbackData
    check_report_buy_cd: CallbackData
    expert_estimation_cd: CallbackData
    expert_complaint_cd: CallbackData

    expert_buy_from_balance_cd: CallbackData


    def __init__(self):
        super().__init__()
        self.buy_report_cd = CallbackData('buy_report_cd', 'report_id', 'price')
        self.download_report_cd = CallbackData('download_report_cd', 'report_id')
        self.add_report_cd = CallbackData('add_report_cd', 'expert_id')
        self.my_account_cd = CallbackData('my_account_cd', 'expert_id')
        self.admin_menu_cd = CallbackData('admin_menu_cd', 'admin_id')
        self.check_report_buy_cd = CallbackData('check_report_buy_cd', 'report_id', 'payment_id', 'amount')
        self.expert_estimation_cd = CallbackData('expert_estimation_cd', 'expert_id', 'report_id', 'estimation')
        self.expert_complaint_cd = CallbackData('expert_complaint_cd', 'report_id')
        self.expert_buy_from_balance_cd = CallbackData('expert_buy_from_balance_cd', 'expert_id', 'report_id')

        # self.confirm_btn_cd = CallbackData('confirm_btn_cd', 'proxy')
        # self.new_order_engineer_confirm_cd = CallbackData('new_order_engineer_confirm_cd', 'order_id')
        # self.new_order_engineer_cancel_cd = CallbackData('new_order_engineer_cancel_cd', 'order_id')

    async def buy_report_kb(self, report_id, price):
        key = InlineKeyboardMarkup()
        key.insert(await self.__get_buy_report_btn(report_id, price))
        return key

    async def download_report_kb(self, report_id):
        key = InlineKeyboardMarkup()

        text = KEYBOARD['download_report']
        callback_data = self.download_report_cd.new(report_id=report_id)
        btn = InlineKeyboardButton(text=text, callback_data=callback_data)

        key.insert(btn)
        return key

    async def expert_menu_kb(self, expert_tg_id):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(
            await self.__get_add_report_btn(expert_tg_id),
            await self.__get_my_account_btn(expert_tg_id)
        )
        return key

    async def waiting_buy_report(self, report_id, payment_id, url, amount):
        key = InlineKeyboardMarkup(row_width=1)

        buy_text = f'Купить отчёт за {str(amount)} руб   💵'
        btn = InlineKeyboardButton(buy_text, url)

        buy_check_text = 'Проверить оплату   🤖'
        buy_check_cd = self.check_report_buy_cd.new(report_id=report_id, payment_id=payment_id, amount=amount)
        buy_btn = InlineKeyboardButton(buy_check_text, callback_data=buy_check_cd)

        key.add(btn, buy_btn)
        return key

    async def find_report_admin_menu_kb(self, admin_id):
        key = InlineKeyboardMarkup(row_width=2)
        key.add(
            await self.__get_add_report_btn(admin_id),
            await self.__get_my_account_btn(admin_id),
            await self.__get_admin_menu_btn(admin_id)
        )
        return key

    async def expert_estimation_or_complaint(self, expert_id, report_id):
        key = InlineKeyboardMarkup(row_width=3)

        for i in range(1, 6):
            key.insert(await self.__get_expert_estimation_btn(expert_id, report_id, i))

        key.add(await self.__get_expert_complaint_btn(report_id))

        return key

    async def expert_buy_from_balance(self, expert_id, report_id, price):
        key = InlineKeyboardMarkup(row_width=1)
        key.insert(await self.__buy_from_balance(expert_id, report_id, price))
        return key


    async def cancel_kb(self, function_start):
        key = InlineKeyboardMarkup()
        key.insert(await self.__get_cancel_btn(function_start))
        return key

    # Логика отдельных кнопок
    # ----------------------------------------------------------------------
    async def __buy_from_balance(self, expert_id, report_id, price):
        text = KEYBOARD['expert_buy_from_balance'].format(price=price)
        cd = self.expert_buy_from_balance_cd.new(expert_id=expert_id, report_id=report_id)
        return await self.__get_inline_btn(text, cd)

    async def __get_expert_complaint_btn(self, report_id):
        text = KEYBOARD['expert_complaint']
        cd = self.expert_complaint_cd.new( report_id=report_id)
        return await self.__get_inline_btn(text, cd)

    async def __get_expert_estimation_btn(self, expert_id, report_id, estimation: int):
        text = estimation
        cd = self.expert_estimation_cd.new(expert_id=expert_id, report_id=report_id, estimation=estimation)
        return await self.__get_inline_btn(text, cd)

    async def __get_admin_menu_btn(self, admin_id):
        text = KEYBOARD['find_report_admin_menu']['menu']
        cd = self.admin_menu_cd.new(admin_id=admin_id)
        btn = await self.__get_inline_btn(text, cd)
        return btn

    async def __get_buy_report_btn(self, report_id, price):
        text = KEYBOARD['buy_report'].format(price=price)
        cd = self.buy_report_cd.new(report_id=report_id, price=price)
        btn = await self.__get_inline_btn(text, cd)
        return btn

    async def __get_cancel_btn(self, function_start):
        text = KEYBOARD['cancel']
        cd = self.back_cd.new(function_start=function_start)
        return await self._get_inline_btn(text, cd)
    # ----------------------------------------------------------------------


    # Вспомогательные функции
    # ----------------------------------------------------------------------
    async def __get_inline_btn(self, text, callback_data):
        return InlineKeyboardButton(text=text, callback_data=callback_data)
    # ----------------------------------------------------------------------
