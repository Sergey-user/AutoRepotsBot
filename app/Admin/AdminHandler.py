import os
import re

from aiogram.types import Message, CallbackQuery, ContentType, LabeledPrice, PreCheckoutQuery, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from app.ZipManager import ZipManager

from main import bot
from app.texts import MESSAGES

from app.BaseHandler import BaseHandler
from app.User.UserStates import FindReportState
from app.Expert.ExpertModels import *
from app.Admin.AdminKeyboard import AdminKeyboard
from app.Admin.AdminStates import *
from app.Admin.AdminRedis import AdminRedis
from app.Admin.Utils.ExcelManager import ExcelManager

from database.db_connect import db

from settings.bot_settings import PROJECT_PATH

class AdminHandler(BaseHandler):
	bot = ''
	keyboard = ''

	def __init__(self):
		super().__init__()
		self.bot = bot
		self.keyboard = AdminKeyboard()
		self.redis = AdminRedis()


	@classmethod
	def register_handlers(cls, dp):
		#super().register_handlers(dp)
		handler = cls()

		dp.register_callback_query_handler(
			handler.back,
			handler.keyboard.back_cd.filter(),
			state='*'
		)

		dp.register_callback_query_handler(
			handler.main_menu,
			handler.keyboard.admin_panel_cd.filter(),
			state='*'
		)
		dp.register_callback_query_handler(
			handler.find_expert_start,
			handler.keyboard.find_expert_cd.filter(),
			state='*'
		)
		dp.register_message_handler(
			handler.find_expert_tg_id,
			state=FindExpertState.waiting_tg_id,
			content_types=ContentType.ANY
		)
		dp.register_callback_query_handler(
			handler.in_expert_menu_expert_reports,
			handler.keyboard.expert_reports_cd.filter(),
			state=AdminPanelState.in_expert_menu
		)
		dp.register_callback_query_handler(
			handler.add_expert_start,
			handler.keyboard.add_expert_cd.filter(),
			state=AdminPanelState.in_main_menu
		)
		dp.register_message_handler(
			handler.add_expert_forward,
			state=AddExpertState.waiting_forward,
			content_types=ContentType.ANY
		)
		dp.register_message_handler(
			handler.add_expert_phone,
			state=AddExpertState.waiting_phone,
			content_types=ContentType.ANY
		)
		dp.register_message_handler(
			handler.add_expert_FIO,
			state=AddExpertState.waiting_FIO,
			content_types=ContentType.ANY
		)

		dp.register_callback_query_handler(
			handler.block_expert,
			handler.keyboard.block_expert_cd.filter(),
			state=AdminPanelState.in_expert_menu
		)
		dp.register_callback_query_handler(
			handler.unblock_expert,
			handler.keyboard.unblock_expert_cd.filter(),
			state=AdminPanelState.in_expert_menu
		)

		dp.register_callback_query_handler(
			handler.change_commission_start,
			handler.keyboard.change_commission_cd.filter(),
			state=AdminPanelState.in_main_menu
		)
		dp.register_message_handler(
			handler.change_commission_amount,
			state=ChangeCommissionState.waiting_amount,
			content_types=ContentType.ANY
		)
		dp.register_message_handler(
			handler.change_commission_new_report_price,
			state=ChangeCommissionState.waiting_new_report_price,
			content_types=ContentType.ANY
		)

		dp.register_callback_query_handler(
			handler.delete_report_start,
			handler.keyboard.delete_report_cd.filter(),
			state=AdminPanelState.in_main_menu
		)
		dp.register_message_handler(
			handler.delete_report_name,
			state=DeleteReportState.waiting_name,
			content_types=ContentType.ANY
		)
		dp.register_callback_query_handler(
			handler.delete_report_confirm_true,
			handler.keyboard.confirm_true_cd.filter(),
			state=DeleteReportState.waiting_confirm
		)
		dp.register_callback_query_handler(
			handler.in_expert_menu_expert_revenues,
			handler.keyboard.expert_revenues_cd.filter(),
			state=AdminPanelState.in_expert_menu
		)
		dp.register_callback_query_handler(
			handler.in_expert_menu_expert_expenses,
			handler.keyboard.expert_expenses_cd.filter(),
			state=AdminPanelState.in_expert_menu
		)
		dp.register_callback_query_handler(
			handler.in_expert_menu_expert_withdrawals,
			handler.keyboard.expert_withdrawals_cd.filter(),
			state=AdminPanelState.in_expert_menu
		)


		dp.register_callback_query_handler(
			handler.admin_expert_withdrawal_finish_start,
			handler.keyboard.admin_expert_withdrawal_finish_cd.filter(),
			state='*'
		)
		dp.register_callback_query_handler(
			handler.admin_expert_withdrawal_cancel,
			handler.keyboard.admin_expert_withdrawal_cancel_cd.filter(),
			state='*'
		)
		dp.register_callback_query_handler(
			handler.admin_expert_withdrawal_finish_auto_new_balance,
			handler.keyboard.admin_expert_withdrawal_finish_auto_new_balance_cd.filter(),
			state=ExpertWithdrawalState.waiting_new_expert_balance
		)
		dp.register_message_handler(
			handler.admin_expert_withdrawal_finish_new_balance,
			state=ExpertWithdrawalState.waiting_new_expert_balance,
			content_types=ContentType.ANY
		)


		dp.register_message_handler(
			handler.add_yookassa_api_start,
			commands=['api'],
			state='*'
		)
		dp.register_message_handler(
			handler.add_yookassa_api_shop_id,
			state=YookassaApiState.shop_id
		)
		dp.register_message_handler(
			handler.add_yookassa_api_key,
			state=YookassaApiState.api_key
		)

		dp.register_message_handler(
			handler.agreement_file_start,
			commands=['agreement'],
			state='*'
		)
		dp.register_message_handler(
			handler.agreement_file,
			state=AgreementState.file,
			content_types=ContentType.ANY
		)

	async def agreement_file_start(self, msg: Message):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		await AgreementState.file.set()

		key = await self.keyboard.cancel_kb('start')
		message = await msg.answer('Отправьте новый файл соглашения:', reply_markup=key)

		try:
			await self.__delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

	async def agreement_file(self, msg: Message, state: FSMContext):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		if not msg.document:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer('Вы можете отправить только файл❗️')

			key = await self.keyboard.cancel_kb('start')
			message = await msg.answer('Отправьте новый файл соглашения:', reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		os.remove(PROJECT_PATH + '/dogovor.pdf')
		await self.bot.download_file_by_id(msg['document']['file_id'], PROJECT_PATH+'/dogovor.pdf')

		await msg.answer('Файл соглашения успешно изменён!')

		await state.finish()

		key = await self._get_now_user_find_report_key(msg.from_user.id)
		message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

	async def add_yookassa_api_start(self, msg: Message):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		key = await self.keyboard.cancel_kb('start')
		message = await msg.answer('Введите уникальный идентификатор магазина (shop_id):', reply_markup=key)

		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		await YookassaApiState.shop_id.set()

		db.close()

	async def add_yookassa_api_shop_id(self, msg: Message, state: FSMContext):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		await state.update_data(shop_id=msg.text)

		key = await self.keyboard.cancel_kb('start')
		message = await msg.answer('Введите API ключ:', reply_markup=key)

		await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		await YookassaApiState.api_key.set()

		db.close()

	async def add_yookassa_api_key(self, msg: Message, state: FSMContext):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		state_data = await state.get_data()
		shop_id = state_data.get('shop_id')
		api_key = msg.text

		now_api = await YookassaApiKeys.get_now_api()
		now_api.is_now = False
		now_api.save()
		YookassaApiKeys.create(shop_id=shop_id, api_key=api_key, is_now=True)

		await msg.answer('Платежные данные успешно изменены!')

		await state.finish()

		# await FindReportState.waiting_VIN_or_autonumber.set()

		key = await self._get_now_user_find_report_key(msg.from_user.id)
		message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()

	async def back(self, call: CallbackQuery, callback_data: dict, state=None):
		await call.message.delete()

		if state:
			state_data = await state.get_data()
			if len(state_data) <= 1:
				await state.finish()

		function_start = callback_data.get('function_start')

		functions = {
			'main_menu': self.main_menu,
			'start': self.start
		}
		function = functions[function_start]
		if function_start in ['add_report_start', 'start']:
			await function(call, state=state, is_back=True, call_back_tg_id=call.from_user.id)
		else:
			await function(call.message, state=state, is_back=True, call_back_tg_id=call.from_user.id)


	async def start(self, call, state, call_back_tg_id, is_back=False):  # В главное меню
		if is_back:
			if state:
				await state.finish()
			# await FindReportState.waiting_VIN_or_autonumber.set()

			key = await self._get_now_user_find_report_key(call_back_tg_id)
			message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

			# await self.__delete_now_deleted_message(call_back_tg_id)
			await self.redis.redis_save_deleted_message_id(call_back_tg_id, message.message_id)

			print(db.is_closed())

	async def main_menu(self, call, is_back=False, call_back_tg_id=None, state=None):
		if is_back:
			expert = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if not await self.__check_admin(call, expert): return

			if state:
				await state.finish()

			await AdminPanelState.in_main_menu.set()

			key = await self.keyboard.admin_main_menu_kb('start', expert.is_super_admin)
			message = await call.answer(MESSAGES['admin_panel'], reply_markup=key)

			# await self.__delete_now_deleted_message(call_back_tg_id)
			await self.redis.redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			return

		expert = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		await self.__check_admin(call.message, expert)

		await AdminPanelState.in_main_menu.set()

		await call.message.delete()

		key = await self.keyboard.admin_main_menu_kb('start', expert.is_super_admin)
		message = await call.message.answer(MESSAGES['admin_panel'], reply_markup=key)

		try:
			await self.__delete_now_deleted_message(call.from_user.id)
		except:
			pass

		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())

	async def block_expert(self, call: CallbackQuery, callback_data: dict):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		expert_id = callback_data.get('expert_id')
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		print(expert.tg_id)

		await expert.block()

		await call.message.answer(MESSAGES['expert_blocked'])

		await AdminPanelState.in_expert_menu.set()

		key = await self.keyboard.admin_in_expert_menu(expert.id, expert.is_blocked, 'main_menu', call.from_user.id)
		await self.bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=key)

		await call.answer()


	async def unblock_expert(self, call: CallbackQuery, callback_data: dict):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		expert_id = callback_data.get('expert_id')
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		await expert.unblock()

		await call.message.answer(MESSAGES['expert_unblocked'])

		await AdminPanelState.in_expert_menu.set()

		key = await self.keyboard.admin_in_expert_menu(expert.id, expert.is_blocked, 'main_menu', call.from_user.id)
		await self.bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=key)

		await call.answer()

	async def find_expert_start(self, call: CallbackQuery):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		await call.message.delete()

		await FindExpertState.waiting_tg_id.set()

		key = await self.keyboard.cancel_kb('main_menu')
		message = await call.message.answer(MESSAGES['find_expert_tg_id'], reply_markup=key)

		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def find_expert_tg_id(self, msg: Message, state: FSMContext):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['find_expert_tg_id'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		tg_id = msg.text

		expert = (await ExpertModel.get_by_tg_id_or_none(tg_id) or
						  await ExpertModel.get_by_id_or_none(tg_id) or
						  await ExpertModel.get_by_tg_username_or_none(tg_id) or
				  	      await ExpertModel.get_by_phone_or_none(tg_id) or
				  		  await AutoReportModel.get_expert_by_report_name_or_none(tg_id))
		if not expert:

			await msg.answer(MESSAGES['find_expert_does_not_exist'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['find_expert_tg_id'], reply_markup=key)

			await self.__delete_now_deleted_message(msg.from_user.id)
			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		await state.finish()

		await AdminPanelState.in_expert_menu.set()

		expert_text = await self.__get_expert_text(expert)
		key = await self.keyboard.admin_in_expert_menu(expert.id, expert.is_blocked, 'main_menu', msg.from_user.id)
		message = await msg.answer(expert_text, reply_markup=key)

		await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def in_expert_menu_expert_reports(self, call: CallbackQuery, callback_data: dict):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		expert_id = callback_data.get('expert_id')
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		if not expert.auto_reports:
			await call.message.answer(MESSAGES['admin_in_expert_menu_expert_not_reports'])

			await call.answer()

			db.close()
			print(db.is_closed())
			return

		excel_manager = ExcelManager()
		xlsx_file_path = await excel_manager.get_expert_reports_xlsx(call.from_user.id, expert.auto_reports)

		await call.message.answer_document(InputFile(xlsx_file_path, xlsx_file_path))
		await excel_manager.delete_xlsx(xlsx_file_path)

		await call.answer()


		db.close()
		print(db.is_closed())


	async def in_expert_menu_expert_revenues(self, call: CallbackQuery, callback_data):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		expert_id = callback_data.get('expert_id')
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		if not expert.transactions:
			await call.message.answer(MESSAGES['admin_in_expert_menu_not_revenues'])

			await call.answer()

			db.close()
			print(db.is_closed())
			return

		excel_manager = ExcelManager()
		xlsx_file_path = await excel_manager.get_expert_revenues_xlsx(call.from_user.id, expert.transactions)

		await call.message.answer_document(InputFile(xlsx_file_path, xlsx_file_path))
		await excel_manager.delete_xlsx(xlsx_file_path)

		await call.answer()


		db.close()
		print(db.is_closed())


	async def in_expert_menu_expert_expenses(self, call: CallbackQuery, callback_data):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		expert_id = callback_data.get('expert_id')
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		expenses = await TransactionModel.get_client_transactions(expert.tg_id)

		if not expenses:
			await call.message.answer(MESSAGES['admin_in_expert_menu_not_expenses'])

			await call.answer()

			db.close()
			print(db.is_closed())
			return

		excel_manager = ExcelManager()
		xlsx_file_path = await excel_manager.get_expert_expenses_xlsx(call.from_user.id, expenses)

		await call.message.answer_document(InputFile(xlsx_file_path, xlsx_file_path))
		await excel_manager.delete_xlsx(xlsx_file_path)

		await call.answer()


		db.close()
		print(db.is_closed())


	async def in_expert_menu_expert_withdrawals(self, call: CallbackQuery, callback_data):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		expert_id = callback_data.get('expert_id')
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		if not expert.withdrawals:
			await call.message.answer(MESSAGES['admin_in_expert_menu_not_withdrawals'])

			await call.answer()

			db.close()
			print(db.is_closed())
			return

		excel_manager = ExcelManager()
		xlsx_file_path = await excel_manager.get_expert_withdrawals_xlsx(call.from_user.id, expert.withdrawals)

		await call.message.answer_document(InputFile(xlsx_file_path, xlsx_file_path))
		await excel_manager.delete_xlsx(xlsx_file_path)

		await call.answer()

		db.close()
		print(db.is_closed())


	async def add_expert_start(self, call: CallbackQuery):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		await call.message.delete()

		await AddExpertState.waiting_forward.set()

		key = await self.keyboard.cancel_kb('main_menu')
		message = await call.message.answer(MESSAGES['add_expert_waiting_forward'], reply_markup=key)

		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def add_expert_forward(self, msg: Message, state: FSMContext):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		if not msg.forward_from and not msg.forward_from_chat:
			await self.__delete_now_deleted_message(msg.from_user.id)

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['add_expert_waiting_forward'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return
		elif msg.forward_from_chat:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer('Канал нельзя сделать автоэкспертом!')

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['add_expert_waiting_forward'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return
		elif msg.forward_from.is_bot:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer('Бота нельзя сделать автоэкспертом!')

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['add_expert_waiting_forward'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return


		new_expert_tg_id = msg.forward_from.id

		if await ExpertModel.find_by_tg_id_or_none(new_expert_tg_id):
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['add_expert_exist'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['add_expert_waiting_forward'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			db.close()
			print(db.is_closed())
			return

		new_expert_tg_username = msg.forward_from.username or None

		await self.__delete_now_deleted_message(msg.from_user.id)

		await state.update_data(new_expert_tg_username=new_expert_tg_username)
		await state.update_data(new_expert_tg_id=new_expert_tg_id)

		await AddExpertState.waiting_phone.set()

		key = await self.keyboard.cancel_kb('main_menu')
		message = await msg.answer(MESSAGES['add_expert_phone'], reply_markup=key)

		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def add_expert_phone(self, msg: Message, state: FSMContext):
		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['add_expert_phone'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		phone = msg.text

		if len(phone) > 12:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['invalid_phone'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['add_expert_phone'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return


		if not re.match('[+, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]{11,12}', phone):
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['invalid_phone'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['add_expert_phone'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		await state.update_data(phone=phone)

		await AddExpertState.waiting_FIO.set()

		key = await self.keyboard.cancel_kb('main_menu')
		message = await msg.answer(MESSAGES['add_expert_FIO'], reply_markup=key)

		await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def add_expert_FIO(self, msg: Message, state=FSMContext):
		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['add_expert_FIO'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		FIO = msg.text

		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return

		state_data = await state.get_data()
		new_expert_tg_id = state_data.get('new_expert_tg_id')
		new_expert_tg_username = state_data.get('new_expert_tg_username')
		new_expert_phone = state_data.get('phone')

		expert = await ExpertModel.create_expert(
			tg_id = new_expert_tg_id,
			phone = new_expert_phone,
			FIO=FIO
		)
		if new_expert_tg_username:
			expert.tg_username = new_expert_tg_username
			expert.save()

		for i in range(5):
			await EstimationModel.add_expert_estimataion(expert, 5)
		await expert.update_rating()

		await state.finish()

		await msg.answer(MESSAGES['add_expert_success'])

		if new_expert_tg_username:
			text = MESSAGES['add_expert_success_with_phone'].format(
				id=expert.id,
				tg_id=expert.tg_id,
				tg_username=expert.tg_username,
				FIO=expert.FIO,
				phone=expert.phone
			)
		else:
			text = MESSAGES['add_expert_success_with_phone'].format(
				id = expert.id,
				tg_id = expert.tg_id,
				FIO=expert.FIO,
				phone = expert.phone
			)
		await msg.answer(text)

		await AdminPanelState.in_main_menu.set()

		key = await self.keyboard.admin_main_menu_kb('start', expert_in_menu.is_super_admin)
		await msg.answer(MESSAGES['admin_panel'], reply_markup=key)

		await self.__delete_now_deleted_message(msg.from_user.id)

		db.close()
		print(db.is_closed())


	async def change_commission_start(self, call: CallbackQuery):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return
		if not expert_in_menu.is_super_admin:
			await call.message.answer('Вы не являетесь главным администратором!')
			db.close()
			print(db.is_closed())
			return

		await ChangeCommissionState.waiting_amount.set()

		text = await self.__get_now_commission_text()
		key = await self.keyboard.cancel_kb('main_menu')
		message = await call.message.answer(text, reply_markup=key)

		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		await call.message.delete()

		db.close()
		print(db.is_closed())

	async def change_commission_amount(self, msg: Message, state: FSMContext):
		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			text = await self.__get_now_commission_text()
			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(text, reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu) or not expert_in_menu.is_super_admin: return


		try:
			amount = int(msg.text)
		except:
			await msg.answer('Вы можете использовать только целые числа❗️')

			text = await self.__get_now_commission_text()
			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(text, reply_markup=key)

			await self.__delete_now_deleted_message(msg.from_user.id)
			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return

		await state.update_data(commission=amount)

		await ChangeCommissionState.waiting_new_report_price.set()

		text = await self.__get_now_report_price_text()
		key = await self.keyboard.cancel_kb('main_menu')
		message = await msg.answer(text, reply_markup=key)

		await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())

	async def change_commission_new_report_price(self, msg: Message, state: FSMContext):
		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			text = await self.__get_now_report_price_text()
			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(text, reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu) or not expert_in_menu.is_super_admin: return

		try:
			amount = int(msg.text)
		except:
			await msg.answer('Вы можете использовать только целые числа❗️')

			text = await self.__get_now_report_price_text()
			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(text, reply_markup=key)

			await self.__delete_now_deleted_message(msg.from_user.id)
			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return

		state_data = await state.get_data()
		commission = state_data.get('commission')
		price = amount

		await CommissionModel.create_new_now_commission(commission)
		await ReportPriceModel.create_new_now_commission(price)

		await state.finish()

		await AdminPanelState.in_main_menu.set()

		await msg.answer(MESSAGES['change_commission_successful'])

		key = await self.keyboard.admin_main_menu_kb('start', expert_in_menu.is_super_admin)
		await msg.answer(MESSAGES['admin_panel'], reply_markup=key)

		await self.__delete_now_deleted_message(msg.from_user.id)

		db.close()
		print(db.is_closed())



	async def delete_report_start(self, call: CallbackQuery):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		await DeleteReportState.waiting_name.set()

		key = await self.keyboard.cancel_kb('main_menu')
		message = await call.message.answer(MESSAGES['delete_report_waiting_name'], reply_markup=key)

		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		await call.message.delete()

		db.close()
		print(db.is_closed())


	async def delete_report_name(self, msg: Message, state: FSMContext):
		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['delete_report_waiting_name'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if not await self.__check_admin(msg, expert_in_menu): return


		report_name = msg.text
		report = await AutoReportModel.get_by_name_or_none(report_name)

		if not report:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['delete_report_does_not_exist'])

			key = await self.keyboard.cancel_kb('main_menu')
			message = await msg.answer(MESSAGES['delete_report_waiting_name'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			db.close()
			print(db.is_closed())
			return

		await DeleteReportState.waiting_confirm.set()

		text = await self.__get_delete_report_text(report)
		key = await self.keyboard.delete_report_confirm(report.id, 'main_menu')
		message = await msg.answer(text, reply_markup=key)

		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def delete_report_confirm_true(self, call: CallbackQuery, state: FSMContext, callback_data: dict):
		expert_in_menu = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if not await self.__check_admin(call.message, expert_in_menu): return

		report_id = callback_data.get('report_id')
		name = await AutoReportModel.delete_report(report_id)
		await ZipManager.delete_report_zip(name)

		await state.finish()

		await call.message.answer(MESSAGES['delete_report_success'])

		await AdminPanelState.in_main_menu.set()

		key = await self.keyboard.admin_main_menu_kb('start', expert_in_menu.is_super_admin)
		await call.message.answer(MESSAGES['admin_panel'], reply_markup=key)

		await call.message.delete()

		db.close()
		print(db.is_closed())



	async def admin_expert_withdrawal_finish_start(self, call: CallbackQuery, callback_data: dict, state: FSMContext):
		if state:
			await state.finish()

		expert_id = callback_data.get('expert_id')
		amount = callback_data.get('amount')
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		await ExpertWithdrawalState.waiting_new_expert_balance.set()

		text = await self.__get_admin_expert_withdrawal_new_balance_text(expert, amount)
		key = await self.keyboard.admin_expert_withdrawal_finish_new_balance(expert_id, amount)
		message = await call.message.answer(text, reply_markup=key)

		await self.__delete_now_deleted_message(call.from_user.id)
		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		await self.redis.withdrawal_expert_id_save(call.from_user.id, expert_id)
		await self.redis.withdrawal_amount_save(call.from_user.id, amount)

		await call.message.delete()

		db.close()
		print(db.is_closed())


	async def admin_expert_withdrawal_cancel(self, call: CallbackQuery, state: FSMContext=None):

		if state:
			await state.finish()

		# await FindReportState.waiting_VIN_or_autonumber.set()

		await call.message.answer(MESSAGES['admin_expert_withdrawal_cancel'])

		key = await self._get_now_user_find_report_key(call.from_user.id)
		message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.__delete_now_deleted_message(call.from_user.id)
		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		await call.message.delete()


		db.close()
		print(db.is_closed())


	async def admin_expert_withdrawal_finish_auto_new_balance(self, call: CallbackQuery, state: FSMContext, callback_data: dict):
		amount = callback_data.get('amount')
		expert_id = callback_data.get('expert_id')
		expert: ExpertModel = await ExpertModel.get_by_id_or_none(expert_id)

		await WithdrawalModel.create_withdrawal(expert, amount, expert.balance)

		new_balance = expert.balance - int(amount)
		await expert.update_balance(new_balance)

		await state.finish()

		# await FindReportState.waiting_VIN_or_autonumber.set()

		await call.message.answer(MESSAGES['admin_expert_withdrawal_finish_auto_new_balance_success'])

		key = await self._get_now_user_find_report_key(call.from_user.id)
		message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		await call.message.delete()

		# await self.__delete_now_deleted_message(call.from_user.id)

		db.close()
		print(db.is_closed())


	async def admin_expert_withdrawal_finish_new_balance(self, msg: Message, state: FSMContext):
		await self.__delete_now_deleted_message(msg.from_user.id)

		amount = await self.redis.withdrawal_amount_get(msg.from_user.id)
		expert_id = await self.redis.withdrawal_expert_id_get(msg.from_user.id)
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			text = await self.__get_admin_expert_withdrawal_new_balance_text(expert, amount)
			key = await self.keyboard.admin_expert_withdrawal_finish_new_balance(expert_id, amount)
			message = await msg.answer(text, reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return


		new_balance = msg.text

		try:
			new_balance = int(new_balance)
		except:
			await msg.answer(MESSAGES['only_int_msg'])

			text = await self.__get_admin_expert_withdrawal_new_balance_text(expert, amount)
			key = await self.keyboard.admin_expert_withdrawal_finish_new_balance(expert_id, amount)
			message = await msg.answer(text, reply_markup=key)

			await self.__delete_now_deleted_message(msg.from_user.id)
			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return

		await WithdrawalModel.create_withdrawal(expert, amount, expert.balance)

		await expert.update_balance(new_balance)

		await state.finish()

		# await FindReportState.waiting_VIN_or_autonumber.set()

		await msg.answer(MESSAGES['admin_expert_withdrawal_finish_auto_new_balance_success'])

		key = await self._get_now_user_find_report_key(msg.from_user.id)
		message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		# await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	# Вспомогательные функции
	# ----------------------------------------------------------------------------------
	async def __get_admin_expert_withdrawal_new_balance_text(self, expert, amount):
		if expert.tg_username:
			text = MESSAGES['admin_expert_withdrawal_finish_new_balance'].format(
				id=expert.id,
				balance=expert.balance,
				rating=expert.rating,
				reports_count=expert.auto_reports.count(),
				buy_count=expert.transactions.count(),
				request_amount=amount,
				FIO=expert.FIO,
				expert_data=f'@{expert.tg_username}'
			)
		else:
			text = MESSAGES['admin_expert_withdrawal_finish_new_balance'].format(
				id=expert.id,
				balance=expert.balance,
				rating=expert.rating,
				reports_count=expert.auto_reports.count(),
				buy_count=expert.transactions.count(),
				request_amount=amount,
				FIO=expert.FIO,
				expert_data=expert.phone
			)
		return text

	async def __get_delete_report_text(self, report):
		text = MESSAGES['delete_report_confirm'].format(
			name = report.name,
			create_date = report.create_date,
			buy_count = await report.get_buy_count()
		)
		return text

	async def __get_now_commission_text(self):
		now_commission = await CommissionModel.get_now_commission()

		text = MESSAGES['change_commission_amount'].format(
			now_commission=now_commission.amount
		)
		return text

	async def __get_now_report_price_text(self):
		now_price = await ReportPriceModel.get_now_commission()

		text = MESSAGES['change_report_price'].format(
			price=now_price.amount
		)
		return text

	async def __delete_now_deleted_message(self, user_tg_id):
		now_deleted_message_id = await self.redis.redis_get_deleted_message_id(user_tg_id)
		await self.bot.delete_message(user_tg_id, now_deleted_message_id)
		await self.redis.delete_deleted_message_id(user_tg_id)


	async def __get_expert_text(self, expert: ExpertModel):
		if expert.tg_username:
			expert_text = MESSAGES['admin_in_expert_menu_with_username'].format(
				id=expert.id,
				balance=expert.balance,
				rating=round(expert.rating, 1),
				reports_count=expert.auto_reports.count(),
				buy_count=expert.transactions.count(),
				FIO=expert.FIO,
				tg_username=expert.tg_username,
				phone=expert.phone
			)
		else:
			expert_text = MESSAGES['admin_in_expert_menu'].format(
				id=expert.id,
				balance=expert.balance,
				rating=round(expert.rating, 1),
				reports_count=expert.auto_reports.count(),
				buy_count=expert.transactions.count(),
				FIO=expert.FIO,
				phone=expert.phone
			)

		return expert_text

	async def __check_admin(self, msg, expert):
		if not expert.is_admin:
			await self.bot.send_message(expert.tg_id, MESSAGES['not_admin'])
			await msg.delete()
			return False
		else:
			return True
	# ----------------------------------------------------------------------------------

