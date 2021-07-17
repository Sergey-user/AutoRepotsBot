from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

from app.texts import KEYBOARD
from app.BaseKeyboard import BaseKeyboard
from app.Expert.ExpertModels import ExpertModel


class AdminKeyboard(BaseKeyboard):
    admin_panel_cd: CallbackData
    find_expert_cd: CallbackData
    add_expert_cd: CallbackData
    delete_report_cd: CallbackData
    change_commission_cd: CallbackData
    # cancel_cd: CallbackData

    expert_reports_cd: CallbackData
    expert_revenues_cd: CallbackData
    expert_expenses_cd: CallbackData
    expert_withdrawals_cd: CallbackData
    block_expert_cd: CallbackData
    unblock_expert_cd: CallbackData

    confirm_true_cd: CallbackData
    # confirm_false_cd: CallbackData

    admin_expert_withdrawal_finish_cd: CallbackData
    admin_expert_withdrawal_cancel_cd: CallbackData
    admin_expert_withdrawal_finish_auto_new_balance_cd: CallbackData


    def __init__(self):
        super().__init__()
        self.admin_panel_cd = CallbackData('admin_panel_cd', 'proxy')
        self.find_expert_cd = CallbackData('find_expert_cd', 'proxy')
        self.add_expert_cd = CallbackData('add_expert_cd', 'proxy')
        self.delete_report_cd = CallbackData('delete_report_cd', 'proxy')
        self.change_commission_cd = CallbackData('change_commission_cd', 'proxy')
        self.admin_expert_withdrawal_finish_auto_new_balance_cd = CallbackData(
            'admin_expert_withdrawal_finish_auto_new_balance_cd',
            'expert_id',
            'amount'
        )
        # self.cancel_cd = CallbackData('cancel_cd', 'function_start')

        self.expert_reports_cd = CallbackData('expert_reports_cd', 'expert_id')
        self.expert_revenues_cd = CallbackData('expert_revenues_cd', 'expert_id')
        self.expert_expenses_cd = CallbackData('expert_expenses_cd', 'expert_id')
        self.expert_withdrawals_cd = CallbackData('expert_withdrawals_cd', 'expert_id')
        self.block_expert_cd = CallbackData('block_expert_cd', 'expert_id')
        self.unblock_expert_cd = CallbackData('unblock_expert_cd', 'expert_id')

        self.confirm_true_cd = CallbackData('confirm_true_cd', 'report_id')
        # self.confirm_false_cd = CallbackData('confirm_false_cd', 'report_id')

        self.admin_expert_withdrawal_finish_cd = CallbackData('admin_expert_withdrawal_finish_cd', 'expert_id', 'amount')
        self.admin_expert_withdrawal_cancel_cd = CallbackData('admin_expert_withdrawal_cancel_cd', 'proxy')

    # async def find_report_kb(self, tg_id):
    #     key = InlineKeyboardMarkup(row_width=2)
    #     key.add(
    #         await self.__get_add_report_btn(tg_id),
    #         await self.__get_my_account_btn(tg_id)
    #     )
    #     return key

    async def admin_main_menu_kb(self, function_start, is_super_admin=False):
        key = InlineKeyboardMarkup(row_width=2)

        key.add(
            await self.__get_find_expert_btn(),
            await self.__get_add_expert_btn(),
        )

        if is_super_admin:
            key.insert(await self.__get_change_commission_btn())

        key.add(await self.__get_delete_report_btn())
        key.add(await self._get_back_btn(function_start))
        return key

    async def cancel_kb(self, function_start):
        key = InlineKeyboardMarkup()
        key.insert(await self.__get_cancel_btn(function_start))
        return key

    async def admin_in_expert_menu(self, expert_id, is_blocked=False, function_start=None, now_admin_tg_id=False):
        key = InlineKeyboardMarkup(row_width=2)

        key.add(
            await self.__get_expert_revenues_btn(expert_id),
            await self.__get_expert_expenses_btn(expert_id),
            await self.__get__expert_reports_btn(expert_id),
            await self.__get_expert_withdrawals_btn(expert_id),
        )

        now_admin = await ExpertModel.get_by_tg_id_or_none(now_admin_tg_id)
        if now_admin.id == expert_id:
            key.insert(await self._get_back_btn(function_start))
            return key

        if not is_blocked:
            key.insert(await self.__get_block_expert_btn(expert_id))
        elif is_blocked:
            key.insert(await self.__get_unblock_expert_btn(expert_id))

        key.add(await self._get_back_btn(function_start))
        return key

    async def delete_report_confirm(self, report_id, function_start):
        key = InlineKeyboardMarkup(row_width=2)

        key.add(
            await self.__get_delete_report_true_btn(report_id),
            await self.__get_delete_report_false_btn(function_start)
        )
        return key

    async def admin_expert_withdrawal(self, expert_id, amount):
        key = InlineKeyboardMarkup(row_width=1)
        key.add(
            await self.__get_admin_expert_withdrawal_finish_btn(expert_id, amount),
            await self.__get_admin_expert_withdrawal_cancel_btn()
        )
        return key

    async def admin_expert_withdrawal_finish_new_balance(self, expert_id, amount):
        key = InlineKeyboardMarkup(row_width=1)
        key.insert(await self.__get_admin_expert_withdrawal_finish_auto_new_balance(expert_id, amount))
        return key

    # Логика отдельных кнопок
    # -----------------------------------------------------------------------------
    async def __get_admin_expert_withdrawal_finish_auto_new_balance(self, expert_id, amount):
        text = KEYBOARD['admin_expert_withdrawal_finish_auto_new_balance']
        cd = self.admin_expert_withdrawal_finish_auto_new_balance_cd.new(expert_id=expert_id, amount=amount)
        return await self._get_inline_btn(text, cd)

    async def __get_admin_expert_withdrawal_finish_btn(self, expert_id, amount):
        text = KEYBOARD['admin_expert_withdrawal_finish']
        cd = self.admin_expert_withdrawal_finish_cd.new(expert_id=expert_id, amount=amount)
        return await self._get_inline_btn(text, cd)

    async def __get_admin_expert_withdrawal_cancel_btn(self):
        text = KEYBOARD['admin_expert_withdrawal_cancel']
        cd = self.admin_expert_withdrawal_cancel_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_delete_report_true_btn(self, report_id):
        text = KEYBOARD['confirm']['true']
        cd = self.confirm_true_cd.new(report_id=report_id)
        return await self._get_inline_btn(text, cd)

    async def __get_delete_report_false_btn(self, function_start):
        text = KEYBOARD['confirm']['false']
        cd = self.back_cd.new(function_start=function_start)
        return await self._get_inline_btn(text, cd)

    async def __get__expert_reports_btn(self, expert_id):
        text = KEYBOARD['admin']['in_expert_menu']['expert_reports']
        cd = self.expert_reports_cd.new(expert_id=expert_id)
        return await self._get_inline_btn(text, cd)

    async def __get_expert_revenues_btn(self, expert_id):
        text = KEYBOARD['admin']['in_expert_menu']['revenues']
        cd = self.expert_revenues_cd.new(expert_id=expert_id)
        return await self._get_inline_btn(text, cd)

    async def __get_expert_expenses_btn(self, expert_id):
        text = KEYBOARD['admin']['in_expert_menu']['expenses']
        cd = self.expert_expenses_cd.new(expert_id=expert_id)
        return await self._get_inline_btn(text, cd)

    async def __get_expert_withdrawals_btn(self, expert_id):
        text = KEYBOARD['admin']['in_expert_menu']['withdrawals']
        cd = self.expert_withdrawals_cd.new(expert_id=expert_id)
        return await self._get_inline_btn(text, cd)

    async def __get_block_expert_btn(self, expert_id):
        text = KEYBOARD['admin']['in_expert_menu']['block_unblock_expert']['block']
        cd = self.block_expert_cd.new(expert_id=expert_id)
        return await self._get_inline_btn(text, cd)

    async def __get_unblock_expert_btn(self, expert_id):
        text = KEYBOARD['admin']['in_expert_menu']['block_unblock_expert']['unblock']
        cd = self.unblock_expert_cd.new(expert_id=expert_id)
        return await self._get_inline_btn(text, cd)


    async def __get_cancel_btn(self, function_start):
        text = KEYBOARD['cancel']
        cd = self.back_cd.new(function_start=function_start)
        return await self._get_inline_btn(text, cd)

    async def __get_find_expert_btn(self):
        text = KEYBOARD['admin']['main_menu']['find_expert']
        cd = self.find_expert_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_add_expert_btn(self):
        text = KEYBOARD['admin']['main_menu']['add_expert']
        cd = self.add_expert_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_delete_report_btn(self):
        text = KEYBOARD['admin']['main_menu']['delete_report']
        cd = self.delete_report_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

    async def __get_change_commission_btn(self):
        text = KEYBOARD['admin']['main_menu']['change_commission']
        cd = self.change_commission_cd.new(proxy=1)
        return await self._get_inline_btn(text, cd)

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

    # -----------------------------------------------------------------------------