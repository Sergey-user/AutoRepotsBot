import shutil, os

from aiogram.types import Message, CallbackQuery, ContentType, LabeledPrice, PreCheckoutQuery, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import time


from main import bot
from app.texts import MESSAGES

from app.BaseHandler import BaseHandler

from app.Expert.ExpertKeyboard import ExpertKeyboard
from app.Expert.ExpertModels import ExpertModel, AutoReportModel, TransactionModel
from app.Expert.ExpertStates import AddReportState, ExpertWithdrawalState, ExpertPanelState
from app.Expert.ExpertFilters import *
from app.Expert.ExpertAddReportUtils import ExpertAddReportUtil

from app.User.UserStates import FindReportState

from app.Admin.AdminKeyboard import AdminKeyboard

# from settings.bot_settings import PROJECT_PATH

# from app.User.UserHandler import UserHandler

from settings.bot_settings import PROJECT_PATH

from database.db_connect import db



class ExpertHandler(BaseHandler):
	bot = ''
	keyboard = ''

	def __init__(self):
		super().__init__()
		self.bot = bot
		self.keyboard = ExpertKeyboard()


	@classmethod
	def register_handlers(cls, dp):
		#super().register_handlers(dp)
		handler = cls()

		dp.register_message_handler(handler.expert, commands=['expert'], state='*')
		dp.register_callback_query_handler(
			handler.my_account,
			handler.keyboard.my_account_cd.filter(),
			state='*'
		)
		dp.register_callback_query_handler(
			handler.my_reports,
			handler.keyboard.my_reports_cd.filter(),
			state=ExpertPanelState.in_expert_menu
		)

		# Добавление отчёта
		# --------------------------------------------------------------------------
		dp.register_callback_query_handler(
			handler.add_report_start,
			handler.keyboard.add_report_cd.filter(),
			state='*'
		)
		dp.register_message_handler(
			handler.add_report_VIN,
			state=AddReportState.waiting_VIN,
			content_types=ContentType.ANY
		)
		dp.register_message_handler(
			handler.add_report_auto_number,
			state=AddReportState.waiting_auto_number,
			content_types=ContentType.ANY
		)
		dp.register_message_handler(
			handler.add_report_VIN_photo,
			state=AddReportState.waiting_VIN_photo,
			content_types=[ContentType.ANY]
		)
		dp.register_message_handler(
			handler.add_report_odometer_data,
			state=AddReportState.waiting_odometer_data,
			content_types=ContentType.ANY
		)
		dp.register_message_handler(
			handler.add_report_vehicle_condition,
			state=AddReportState.waiting_vehicle_condition,
			content_types=[ContentType.ANY]
		)

		dp.register_message_handler(
			handler.add_report_download_defects_photos_success,
			Text(['Продолжить   📥']),
			state=AddReportState.waiting_defects_photo
		)
		dp.register_message_handler(
			handler.add_report_defect_photo,
			state=AddReportState.waiting_defects_photo,
			content_types=[ContentType.ANY]
		)


		dp.register_callback_query_handler(
			handler.add_report_download_defects_photos_success,
			handler.keyboard.defects_photo_download_success_cd.filter(),
			state=AddReportState.waiting_defects_photo
		)

		dp.register_message_handler(
			handler.add_report_computer_diagnostics_download_success,
			Text(['Продолжить   📥']),
			state=AddReportState.waiting_computer_diagnostics
		)
		dp.register_message_handler(
			handler.add_report_computer_diagnostics,
			state=AddReportState.waiting_computer_diagnostics,
			content_types=[ContentType.ANY]
		)

		dp.register_callback_query_handler(
			handler.back,
			handler.keyboard.back_cd.filter(),
			state='*'
		)

		dp.register_callback_query_handler(
			handler.add_report_computer_diagnostics_download_success,
			handler.keyboard.computer_diagnostics_download_success.filter(),
			state=AddReportState.waiting_computer_diagnostics
		)

		dp.register_message_handler(
			handler.add_report_checking_databases_download_successfull,
			Text(['Продолжить   📥']),
			state=AddReportState.waiting_checking_databases
		)
		dp.register_message_handler(
			handler.add_report_checking_databases,
			state=AddReportState.waiting_checking_databases,
			content_types=[ContentType.ANY]
		)

		dp.register_callback_query_handler(
			handler.add_report_checking_databases_download_successfull,
			handler.keyboard.checking_databases_cd.filter(),
			state=AddReportState.waiting_checking_databases
		)
		dp.register_message_handler(
			handler.add_report_defects_description,
			state=AddReportState.waiting_defects_description,
			content_types=ContentType.ANY
		)
		dp.register_message_handler(
			handler.add_report_voice,
			state=AddReportState.waiting_voice,
			content_types=ContentType.ANY
		)


		dp.register_callback_query_handler(
			handler.expert_withdrawal_start,
			handler.keyboard.withdrawal_money_cd.filter(),
			state=ExpertPanelState.in_expert_menu
		)
		dp.register_message_handler(
			handler.expert_withdrawal_amount,
			state=ExpertWithdrawalState.waiting_amount,
			content_types=ContentType.ANY
		)

		# --------------------------------------------------------------------------

	async def back(self, call: CallbackQuery, callback_data: dict, state=None):

		await call.message.delete()

		if state:
			state_data = await state.get_data()
			if len(state_data) <= 1:
				await state.finish()

		function_start = callback_data.get('function_start')

		functions = {
			'add_report_start': self.add_report_start,
			'add_report_VIN': self.add_report_VIN,
			'add_report_auto_number': self.add_report_auto_number,
			'add_report_VIN_photo': self.add_report_VIN_photo,
			'add_report_odometer_data': self.add_report_odometer_data,
			'add_report_vehicle_condition': self.add_report_vehicle_condition,
			'add_report_defect_photo': self.add_report_defect_photo,
			'add_report_computer_diagnostics': self.add_report_computer_diagnostics,
			'add_report_checking_databases': self.add_report_checking_databases,
			'add_report_defects_description': self.add_report_defects_description,
			'start': self.start,
			'my_account': self.my_account
		}
		# print(str(call.from_user.id) + 'backbackback')
		function = functions[function_start]
		if function_start in ['add_report_start', 'start']:
			await function(call, state, is_back=True, call_back_tg_id=call.from_user.id)
		else:
			await function(call.message, state, is_back=True, call_back_tg_id=call.from_user.id)

		# await call.message.delete()


	async def start(self, call, state, call_back_tg_id, is_back=False):  # В главное меню
		# await call.message.delete()
		if is_back:
			if state:
				await state.finish()
			# await FindReportState.waiting_VIN_or_autonumber.set()

			key = await self._get_now_user_find_report_key(call_back_tg_id)
			message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

			# await self.__add_report_delete_now_deleted_message(call_back_tg_id)
			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)

			print(db.is_closed())

	async def expert(self, msg: Message, state=None):
		await self.__delete_state_redis_data(msg.from_user.id)

		await msg.answer('Expert')
		await state.finish()

		print(db.is_closed())


	async def my_account(self, call: CallbackQuery, callback_data: dict, is_back=False, call_back_tg_id=None):
		if is_back:
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, call)
				await call.message.delete()
				return

			await ExpertPanelState.in_expert_menu.set()

			text = await self.__get_my_account_text(expert)
			key = await self.keyboard.expert_my_account_menu_kb(expert.id, 'start', expert.is_super_admin)
			message = await call.answer(text, reply_markup=key)

			try:
				await self.__add_report_delete_now_deleted_message(call_back_tg_id)
			except:
				pass

			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			return

		expert = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(call.from_user.id, call.message)
			await call.message.delete()
			return

		await ExpertPanelState.in_expert_menu.set()

		text = await self.__get_my_account_text(expert)
		key = await self.keyboard.expert_my_account_menu_kb(expert.id, 'start', expert.is_super_admin)
		message = await call.message.answer(text, reply_markup=key)

		await call.message.delete()

		try:
			await self.__add_report_delete_now_deleted_message(call.from_user.id)
		except:
			pass

		await self.redis.add_report_redis_save_deleted_message_id(call.from_user.id, message.message_id)

		# await self.bot.edit_message_text(text, call.from_user.id, call.message.message_id, reply_markup=key)

		# await call.message.answer(text, reply_markup=key)

		db.close()

		print(db.is_closed())


	async def my_reports(self, call: CallbackQuery, callback_data: dict):

		expert_id = callback_data.get('expert_id')
		expert: ExpertModel = await ExpertModel.get_by_id_or_none(expert_id)
		if expert.is_blocked:
			await self.__expert_is_blocked(call.from_user.id, call.message)
			await call.message.delete()
			return

		if not expert.auto_reports:
			await call.message.answer(MESSAGES['expert_not_reports'])

			await call.answer()

			db.close()
			print(db.is_closed())
			return

		for report in expert.auto_reports:
			report_text = MESSAGES['expert_my_report'].format(
				name=report.name,
				create_date=report.create_date.strftime('%d.%m.%Y'),
				buy_count=TransactionModel.select().where(TransactionModel.report_name==report.name).count()
			)
			await call.message.answer(report_text)

		await call.message.delete()

		# await FindReportState.waiting_VIN_or_autonumber.set()

		key = await self._get_now_user_find_report_key(call.from_user.id)
		message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.redis.add_report_redis_save_deleted_message_id(call.from_user.id, message.message_id)

		await call.answer()

		db.close()
		print(db.is_closed())



	async def expert_withdrawal_start(self, call: CallbackQuery):
		expert = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(call.from_user.id, call.message)
			await call.message.delete()
			return

		await ExpertWithdrawalState.waiting_amount.set()

		key = await self.keyboard.cancel_kb('my_account')
		message = await call.message.answer(MESSAGES['withdrawal_amount'], reply_markup=key)

		await self.redis.add_report_redis_save_deleted_message_id(call.from_user.id, message.message_id)

		await call.message.delete()

		db.close()
		print(db.is_closed())


	async def expert_withdrawal_amount(self, msg: Message, state: FSMContext):
		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			return


		if not msg.text:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.cancel_kb('my_account')
			message = await msg.answer(MESSAGES['withdrawal_amount'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return

		amount = msg.text

		try:
			amount = int(amount)
		except:
			await msg.answer(MESSAGES['only_int_msg'])

			key = await self.keyboard.cancel_kb('my_account')
			message = await msg.answer(MESSAGES['withdrawal_amount'], reply_markup=key)

			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return


		if amount < 1000:
			key = await self.keyboard.cancel_kb('my_account')
			message = await msg.answer(MESSAGES['withdrawal_amount'], reply_markup=key)

			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return
		elif amount > expert.balance:
			await msg.answer(MESSAGES['withdrawal_too_expert_balance'])

			key = await self.keyboard.cancel_kb('my_account')
			message = await msg.answer(MESSAGES['withdrawal_amount'], reply_markup=key)

			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		super_admin: ExpertModel = await ExpertModel.get_super_admin()

		if expert.tg_username:
			admin_request_text = MESSAGES['admin_expert_withdrawal_request'].format(
			id = expert.id,
			balance = expert.balance,
			rating = expert.rating,
			reports_count = expert.auto_reports.count(),
			buy_count = expert.transactions.count(),
			request_amount = amount,
			FIO=expert.FIO,
			expert_data = f"@{expert.tg_username}"
			)
		else:
			admin_request_text = MESSAGES['admin_expert_withdrawal_request'].format(
				id = expert.id,
				balance = expert.balance,
				rating = expert.rating,
				reports_count = expert.auto_reports.count(),
				buy_count = expert.transactions.count(),
				request_amount = amount,
				FIO=expert.FIO,
				expert_data = expert.phone
			)

		admin_keyboard = AdminKeyboard()

		key = await admin_keyboard.admin_expert_withdrawal(expert.id, amount)
		await self.bot.send_message(super_admin.tg_id, admin_request_text, reply_markup=key)

		await state.finish()

		await ExpertPanelState.in_expert_menu.set()

		await msg.answer(MESSAGES['expert_withdrawal_send_admin'])

		text = await self.__get_my_account_text(expert)
		key = await self.keyboard.expert_my_account_menu_kb(expert.id, 'start')
		await msg.answer(text, reply_markup=key)

		try:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
		except:
			pass

		db.close()
		print(db.is_closed())



	# Логика добавления отчёта
	# ------------------------------------------------------------------------
	async def add_report_start(self, call: CallbackQuery, state, is_back=False, call_back_tg_id=None):
		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if expert.is_blocked:
			# await call.message.delete()
			await self.__expert_is_blocked(call.from_user.id, call.message)
			return

		if is_back:
			await AddReportState.waiting_VIN.set()

			key = await self.keyboard.only_main_menu_kb()
			msg = await call.message.answer(MESSAGES['waiting_VIN'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(call.from_user.id, msg.message_id)
			return

		await AddReportState.waiting_VIN.set()

		key = await self.keyboard.only_main_menu_kb()

		if type(call) == CallbackQuery:
			await call.message.delete()
			msg = await call.message.answer(MESSAGES['waiting_VIN'], reply_markup=key)

			await call.answer()
		elif type(call) == Message:
			await call.delete()
			msg = await call.answer(MESSAGES['waiting_VIN'], reply_markup=key)

		try:
			await self.__add_report_delete_now_deleted_message(call.from_user.id)
		except:
			pass

		await self.redis.add_report_redis_save_deleted_message_id(str(call.from_user.id), str(msg.message_id))

		print(db.is_closed())


	async def add_report_VIN(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):
		if not msg.text:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.only_main_menu_kb()
			message = await msg.answer(MESSAGES['waiting_VIN'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return


		state_data = await state.get_data()
		if is_back and state_data.get('VIN'):
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await AddReportState.waiting_auto_number.set()
			await self.redis.VIN_photo_tg_id_delete(call_back_tg_id)
			key = await self.keyboard.add_report_back_main_menu_kb('add_report_start')
			message = await msg.answer(MESSAGES['waiting_auto_number'], reply_markup=key)
			# await self.__add_report_delete_now_deleted_message(call_back_tg_id)
			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			await self.redis.only_one_file_delete(call_back_tg_id)

			return

		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return

		VIN = msg.text
		try:
			await AddReportFilter.VIN_filter(VIN.upper())
		except InvalidVINFormat:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['invalid_VIN_format'])

			key = await self.keyboard.only_main_menu_kb()
			message = await msg.answer(MESSAGES['waiting_VIN'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return

		await state.update_data(VIN=VIN.upper())
		await AddReportState.waiting_auto_number.set()

		key = await self.keyboard.add_report_back_main_menu_kb('add_report_start')
		message = await msg.answer(MESSAGES['waiting_auto_number'], reply_markup=key)

		await self.redis.only_one_file_delete(msg.from_user.id)

		try:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		print(db.is_closed())


	async def add_report_auto_number(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):
		if not msg.text:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_start')
			message = await msg.answer(MESSAGES['waiting_auto_number'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return


		state_data = await state.get_data()
		if is_back and state_data.get('auto_number'):
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await state.update_data(VIN_photo_tg_id=None)
			await self.redis.VIN_photo_tg_id_delete(call_back_tg_id)
			await AddReportState.waiting_VIN_photo.set()
			key = await self.keyboard.add_report_back_main_menu_kb('add_report_VIN')
			message = await msg.answer(MESSAGES['waiting_VIN_photo'], reply_markup=key)
			# await self.__add_report_delete_now_deleted_message(call_back_tg_id)
			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			await self.redis.only_one_file_delete(call_back_tg_id)
			return

		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return

		auto_number = msg.text

		auto_number = auto_number.upper()
		intab = 'ABEKMHOPCTYX'
		outtab = 'АВЕКМНОРСТУХ'
		number = auto_number.maketrans(intab, outtab)

		auto_number = auto_number.translate(number).lower()

		try:
			await AddReportFilter.auto_number_filter(auto_number.upper())
		except InvalidAutoNumberFormat:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['invalid_auto_number_format'])

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_start')
			message = await msg.answer(MESSAGES['waiting_auto_number'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return


		await state.update_data(auto_number=auto_number)
		await AddReportState.waiting_VIN_photo.set()

		key = await self.keyboard.add_report_back_main_menu_kb('add_report_VIN')
		message = await msg.answer(MESSAGES['waiting_VIN_photo'], reply_markup=key)

		await self.redis.only_one_file_delete(msg.from_user.id)

		try:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		message = await self.bot.send_message(1677813886, 'error_message')
		await self.redis.error_msg_save(1677813886, message.message_id)

		print(db.is_closed())


	async def add_report_VIN_photo(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):
		if is_back:
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await AddReportState.waiting_odometer_data.set()
			key = await self.keyboard.add_report_back_main_menu_kb('add_report_auto_number')
			message = await msg.answer(MESSAGES['waiting_odometer_data'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			await self.redis.condition_data_delete(call_back_tg_id)

			return

		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return


		# await self.redis.VIN_photo_tg_id_save(msg.from_user.id)
		if await self.redis.VIN_photo_tg_id_get(msg.from_user.id):
			return

		if msg['media_group_id']:
			await self.__delete_now_error_message(msg.from_user.id)

			message = await msg.answer(MESSAGES['only_one_file'])


			await self.redis.error_msg_save(msg.from_user.id, message.message_id)
			return

		await self.redis.VIN_photo_tg_id_save(msg.from_user.id)

		if msg.photo:

			photo_tg_id = msg['photo'][2]['file_id']
			mime_type = 'mime/jpg'
			data = {
				'tg_id': photo_tg_id,
				'mime_type': mime_type,
				'is_document': False
			}
			await self.redis.VIN_photo_tg_id_save(msg.from_user.id)
			await state.update_data(VIN_photo_tg_id=data)
			# await self.redis.only_one_file_delete(msg.from_user.id)
		elif msg.document:

			if msg['document']['file_size'] >= 10468488:
				await self.redis.VIN_photo_tg_id_delete(msg.from_user.id)
				await msg.answer(MESSAGES['too_file_size'])
				return

			document_extension = msg['document']['mime_type']
			try:
				await AddReportFilter.is_photo_filter(document_extension)
			except InvalidPhotoExtension:

				message = await msg.answer(MESSAGES['invalid_photo'])
				await self.redis.VIN_photo_tg_id_delete(msg.from_user.id)

				return

			await msg.answer('Сжимаю фотографию...')

			path = PROJECT_PATH + f'/app/Expert/photo_proxy/'
			tg_id = msg['document']['file_id']

			await self.bot.download_file_by_id(tg_id, path + tg_id)
			photo_msg = await self.bot.send_photo(1677813886, InputFile(path + tg_id, tg_id))

			os.remove(path + tg_id)

			photo_tg_id = photo_msg['photo'][2]['file_id']
			mime_type = msg['document']['mime_type']
			data = {
				'tg_id': photo_tg_id,
				'mime_type': mime_type,
				'is_document': True
			}
			await self.redis.VIN_photo_tg_id_save(msg.from_user.id)
			await state.update_data(VIN_photo_tg_id=data)

		elif msg.text:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['defects_photos_not_text'])

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_VIN')
			message = await msg.answer(MESSAGES['waiting_VIN_photo'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			await self.redis.VIN_photo_tg_id_delete(msg.from_user.id)

			return
		else:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_photo_msg'])

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_VIN')
			message = await msg.answer(MESSAGES['waiting_VIN_photo'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			await self.redis.VIN_photo_tg_id_delete(msg.from_user.id)

			return

		await AddReportState.waiting_odometer_data.set()

		key = await self.keyboard.add_report_back_main_menu_kb('add_report_auto_number')
		message = await msg.answer(MESSAGES['waiting_odometer_data'], reply_markup=key)
		try:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)


		print(db.is_closed())


	async def add_report_odometer_data(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):
		# print(await self.redis.add_report_redis_get_deleted_message_id(msg.from_user.id))
		if not msg.text:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_auto_number')
			message = await msg.answer(MESSAGES['waiting_odometer_data'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return


		state_data = await state.get_data()

		if is_back and state_data.get('odometer_data'):
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await state.update_data(defects_photos_list=None)
			await self.redis.add_report_defects_photos_delete(call_back_tg_id)
			await self.redis.test_delete(call_back_tg_id)
			await self.redis.voice_delete(call_back_tg_id)
			await AddReportState.waiting_vehicle_condition.set()
			key = await self.keyboard.add_report_back_main_menu_kb('add_report_VIN_photo')
			message = await msg.answer(MESSAGES['waiting_vehicle_condition'], reply_markup=key)

			await self.redis.condition_data_delete(call_back_tg_id)


			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)

			return

		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return

		odometer_data = msg.text
		try:
			await AddReportFilter.odometer_data_filter(odometer_data)
		except ValueError:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['invalid_odometer_data'])

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_auto_number')
			message = await msg.answer(MESSAGES['waiting_odometer_data'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return

		await state.update_data(odometer_data=odometer_data)
		await AddReportState.waiting_vehicle_condition.set()

		key = await self.keyboard.add_report_back_main_menu_kb('add_report_VIN_photo')
		message = await msg.answer(MESSAGES['waiting_vehicle_condition'], reply_markup=key)

		await self.redis.only_one_file_delete(msg.from_user.id)

		try:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		message = await self.bot.send_message(1677813886, 'error_message')
		await self.redis.error_msg_save(1677813886, message.message_id)

		print(db.is_closed())


	async def add_report_vehicle_condition(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):
		if msg['media_group_id']:
			await self.__delete_now_error_message(msg.from_user.id)

			message = await msg.answer(MESSAGES['only_one_file'])

			await self.redis.error_msg_save(msg.from_user.id, message.message_id)
			return

		state_data = await state.get_data()
		if is_back and (state_data.get('vehicle_condition_photo_tg_id') or
		state_data.get('vehicle_condition_text') or state_data.get('vehicle_condition_voice_tg_id')):
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await self.redis.add_report_defects_photos_delete(call_back_tg_id)
			await self.redis.computer_diagnostic_delete(call_back_tg_id)
			await self.redis.computer_diagnostic_files_delete(call_back_tg_id)

			await AddReportState.waiting_defects_photo.set()

			rm_key = await self.keyboard.remove_kb()
			m = await msg.answer('a', reply_markup=rm_key)
			await m.delete()

			key = await self.keyboard.defects_photo_download_success_kb('add_report_odometer_data')
			message = await msg.answer(MESSAGES['waiting_defects_photo'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			return

		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return


		if msg.photo:
			photo_tg_id = msg['photo'][2]['file_id']
			mime_type = 'mime/jpg'
			data = {
				'tg_id': photo_tg_id,
				'mime_type': mime_type
			}

			# await self.redis.condition_data_save(msg.from_user.id)
			await state.update_data(vehicle_condition_photo_tg_id=data)
		elif msg.document:
			if msg['document']['file_size'] >= 10468488:
				await msg.answer(MESSAGES['too_file_size'])
				return

			document_extension = msg['document']['mime_type']
			try:
				await AddReportFilter.is_photo_filter(document_extension)
			except InvalidPhotoExtension:
				await msg.answer(MESSAGES['invalid_photo'])

				return

			await msg.answer('Сжимаю фотографию...')

			path = PROJECT_PATH + f'/app/Expert/photo_proxy/'
			tg_id = msg['document']['file_id']

			await self.bot.download_file_by_id(tg_id, path + tg_id)
			photo_msg = await self.bot.send_photo(1677813886, InputFile(path + tg_id, tg_id))

			os.remove(path + tg_id)

			photo_tg_id = photo_msg['photo'][2]['file_id']
			mime_type = msg['document']['mime_type']
			data = {
				'tg_id': photo_tg_id,
				'mime_type': mime_type
			}

			await state.update_data(vehicle_condition_photo_tg_id=data)
		elif msg.text:
			await self.redis.condition_data_save(msg.from_user.id)
			await state.update_data(vehicle_condition_text=msg.text)
		elif msg['voice']:
			now_voice_list = await self.redis.voice_get(msg.from_user.id)
			if now_voice_list:
				message = await msg.answer(MESSAGES['only_one_voice'])
				await self.redis.voice_delete(msg.from_user.id)

				await self.__add_report_delete_now_deleted_message(msg.from_user.id)
				await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

				return

			voice_tg_id = msg['voice']['file_id']
			mime_type = msg['voice']['mime_type']

			data = {
				'tg_id': voice_tg_id,
				'mime_type': mime_type
			}

			now_voice_list.append(data)
			await self.redis.voice_save(msg.from_user.id, now_voice_list)
			await state.update_data(vehicle_condition_voice_tg_id=data)
		else:
			await msg.answer('Вы можете отправить только текстовое сообщение, голосовое сообщение или фото')
			return



		await AddReportState.waiting_defects_photo.set()

		key = await self.keyboard.defects_photo_download_success_kb('add_report_odometer_data')
		message = await msg.answer(MESSAGES['waiting_defects_photo'], reply_markup=key)

		await self.redis.voice_delete(msg.from_user.id)

		try:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		print(db.is_closed())


	async def add_report_defect_photo(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):
		print(msg)

		state_data = await state.get_data()

		if is_back and state_data.get('defects_photos_list'):
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await self.redis.computer_diagnostic_files_delete(call_back_tg_id)
			await self.redis.computer_diagnostic_delete(call_back_tg_id)
			await self.redis.checking_databases_delete(call_back_tg_id)
			await self.redis.checking_databases_files_delete(call_back_tg_id)
			await AddReportState.waiting_computer_diagnostics.set()
			key = await self.keyboard.computer_diagnostic_download_success_kb('add_report_vehicle_condition')
			message = await msg.answer(MESSAGES['waiting_computer_diagnostics'], reply_markup=key)
			# await self.__add_report_delete_now_deleted_message(call_back_tg_id)
			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			return

		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return

		now_photos_list = await self.redis.add_report_defects_photos_get(msg.from_user.id)

		if len(now_photos_list) > 19:
			await self.__delete_now_error_message(msg.from_user.id)

			message = await msg.answer('Вы можете добавить только 20 фото!')

			await self.redis.error_msg_save(msg.from_user.id, message.message_id)

			return

		if msg.photo:
			photo_tg_id = msg['photo'][2]['file_id']
			mime_type = 'mime/jpg'
			data = {
				'tg_id': photo_tg_id,
				'mime_type': mime_type,
				'is_document': False
			}
			now_photos_list.append(data)

			await self.redis.add_report_defects_photos_redis_save(msg.from_user.id, now_photos_list)

			file_unique_id = msg['photo'][2]['file_unique_id']


		elif msg.document:
			if msg['document']['file_size'] >= 10468488:
				await msg.answer(MESSAGES['too_file_size'])
				return

			document_extension = msg['document']['mime_type']
			try:
				await AddReportFilter.is_photo_filter(document_extension)
			except InvalidPhotoExtension:
				message = await msg.answer(MESSAGES['invalid_photo'])

				return

			photo_tg_id = msg['document']['file_id']
			mime_type = msg['document']['mime_type']
			data = {
				'tg_id': photo_tg_id,
				'mime_type': mime_type,
				'is_document': True
			}
			now_photos_list.append(data)
			await self.redis.add_report_defects_photos_redis_save(msg.from_user.id, now_photos_list)

			file_unique_id = msg['document']['file_unique_id']
		else:
			message = await msg.answer(MESSAGES['only_photo_msg'])
			return

		await msg.answer(f"Загружено: {file_unique_id}", reply_markup=await self.keyboard.test())


		if len(now_photos_list) == 20:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			files = await self.redis.add_report_defects_photos_get(msg.from_user.id)

			key = await self.keyboard.defects_photo_next_step('add_report_odometer_data')
			message = await msg.answer(MESSAGES['defects_photos_all'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		print(db.is_closed())


	async def add_report_download_defects_photos_success(self, call: CallbackQuery, state: FSMContext):
		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(call.from_user.id, call)
			await self.__add_report_delete_now_deleted_message(call.from_user.id)
			return

		files = await self.redis.add_report_defects_photos_get(call.from_user.id)
		if len(files) == 0:
			if type(call) == Message:
				await AddReportState.waiting_defects_photo.set()

				await call.answer(MESSAGES['files_not_add'])
				return
			elif type(call) == CallbackQuery:


				await AddReportState.waiting_defects_photo.set()

				await call.message.answer(MESSAGES['files_not_add'])

				await call.answer()
				return

		key = await self.keyboard.remove_kb()
		if type(call) == Message:
			await call.answer('Сжимаю фотографии...', reply_markup=key)
			try:
				await self.__add_report_delete_now_deleted_message(call.from_user.id)
			except:
				pass
		elif type(call) == CallbackQuery:
			await call.message.delete()
			await call.message.answer('Сжимаю фотографии...', reply_markup=key)


		for photo in files:
			if photo['is_document']:
				path = PROJECT_PATH + f'/app/Expert/photo_proxy/'

				await self.bot.download_file_by_id(photo['tg_id'], path + photo['tg_id'])
				photo_msg = ''
				while True:
					try:
						photo_msg = await self.bot.send_photo(1677813886, InputFile(path + photo['tg_id'], photo['tg_id']))
						break
					except:
						print('e')
						continue

				os.remove(path + photo['tg_id'])

				photo['tg_id'] = photo_msg['photo'][2]['file_id']



		await state.update_data(defects_photos_list=files)
		await AddReportState.waiting_computer_diagnostics.set()

		key = await self.keyboard.computer_diagnostic_download_success_kb('add_report_vehicle_condition')

		if type(call) == Message:
			message = await call.answer(MESSAGES['waiting_computer_diagnostics'], reply_markup=key)
		elif type(call) == CallbackQuery:
			message = await call.message.answer(MESSAGES['waiting_computer_diagnostics'], reply_markup=key)

		await self.redis.add_report_redis_save_deleted_message_id(call.from_user.id, message.message_id)

		print(db.is_closed())


	async def add_report_computer_diagnostics(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):
		state_data = await state.get_data()
		if is_back and state_data.get('computer_diagnostics_files'):
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await self.redis.checking_databases_delete(call_back_tg_id)
			await self.redis.checking_databases_files_delete(call_back_tg_id)

			await AddReportState.waiting_checking_databases.set()
			key = await self.keyboard.checking_databases_download_success_kb('add_report_defect_photo')
			message = await msg.answer(MESSAGES['waiting_checking_databases'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			return

		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return

		now_computer_diagnostics_files = await self.redis.computer_diagnostic_files_get(msg.from_user.id)

		if len(now_computer_diagnostics_files) > 2:
			await self.__delete_now_error_message(msg.from_user.id)

			message = await msg.answer(MESSAGES['only_three_file'])

			await self.redis.error_msg_save(msg.from_user.id, message.message_id)

			return


		if msg.photo:
			photo_tg_id = msg['photo'][2]['file_id']
			mime_type = 'mime/jpg'
			data = {
				'tg_id': photo_tg_id,
				'mime_type': mime_type,
				'is_document': False
			}
			now_computer_diagnostics_files.append(data)
			await self.redis.computer_diagnostic_file_save(msg.from_user.id, now_computer_diagnostics_files)

			file_unique_id = msg['photo'][2]['file_unique_id']


		elif msg.document:
			if msg['document']['file_size'] >= 10468488:
				await msg.answer(MESSAGES['too_file_size'])
				return

			document_extension = msg['document']['mime_type']
			try:
				await AddReportFilter.computer_diagnostics_filter(document_extension)
			except InvalidDiagnosticDocumentExtension:
				await msg.answer(MESSAGES['invalid_diagnostic_document_extension'])
				return

			photo_tg_id = msg['document']['file_id']
			mime_type = msg['document']['mime_type']
			if mime_type in ['image/jpg', 'image/jpeg', 'image/png']:
				data = {
					'tg_id': photo_tg_id,
					'mime_type': mime_type,
					'is_document': True
				}
			else:
				data = {
					'tg_id': photo_tg_id,
					'mime_type': mime_type,
					'is_document': False
				}

			now_computer_diagnostics_files.append(data)
			await self.redis.computer_diagnostic_file_save(msg.from_user.id, now_computer_diagnostics_files)

			file_unique_id = msg['document']['file_unique_id']

		else:
			await msg.answer('Вы можете загружать только .pdf, .txt и фото!')

			return

		key = await self.keyboard.test()
		await msg.answer(f"Загружено: {file_unique_id}", reply_markup=key)


		if len(now_computer_diagnostics_files) == 3:
			print(await self.redis.add_report_defects_photos_get(msg.from_user.id))
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			files = await self.redis.computer_diagnostic_files_get(msg.from_user.id)


			key = await self.keyboard.computer_diagnostic_next_step('add_report_defect_photo')
			message = await msg.answer(MESSAGES['computer_diagnostics_all'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)


	async def add_report_computer_diagnostics_download_success(self, call: CallbackQuery, state: FSMContext):
		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(call.from_user.id, call)
			await self.__add_report_delete_now_deleted_message(call.from_user.id)
			return

		files = await self.redis.computer_diagnostic_files_get(call.from_user.id)

		if len(files) == 0:
			if type(call) == Message:
				await AddReportState.waiting_computer_diagnostics.set()

				await call.answer(MESSAGES['files_not_add'])
			elif type(call) == CallbackQuery:
				await AddReportState.waiting_computer_diagnostics.set()

				await call.message.answer(MESSAGES['files_not_add'])

				await call.answer()
			return

		key = await self.keyboard.remove_kb()

		if type(call) == Message:
			await call.answer('Сжимаю файлы...', reply_markup=key)
			try:
				await self.__add_report_delete_now_deleted_message(call.from_user.id)
			except:
				pass
		elif type(call) == CallbackQuery:
			await call.message.delete()
			await call.message.answer('Сжимаю файлы...', reply_markup=key)

		for photo in files:
			if photo['is_document']:
				path = PROJECT_PATH + f'/app/Expert/photo_proxy/'

				await self.bot.download_file_by_id(photo['tg_id'], path + photo['tg_id'])
				photo_msg = ''
				while True:
					try:
						photo_msg = await self.bot.send_photo(1677813886, InputFile(path + photo['tg_id'], photo['tg_id']))
						break
					except:
						print('e')
						continue

				os.remove(path + photo['tg_id'])

				photo['tg_id'] = photo_msg['photo'][2]['file_id']


		await state.update_data(computer_diagnostics_files=files)

		await AddReportState.waiting_checking_databases.set()

		key = await self.keyboard.checking_databases_download_success_kb('add_report_defect_photo')

		if type(call) == Message:
			message = await call.answer(MESSAGES['waiting_checking_databases'], reply_markup=key)
		elif type(call) == CallbackQuery:
			message = await call.message.answer(MESSAGES['waiting_checking_databases'], reply_markup=key)

		await self.redis.add_report_redis_save_deleted_message_id(call.from_user.id, message.message_id)

		print(db.is_closed())


	async def add_report_checking_databases(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):


		state_data = await state.get_data()
		if is_back and state_data.get('checking_databases_files'):
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await AddReportState.waiting_defects_description.set()
			key = await self.keyboard.add_report_back_main_menu_kb('add_report_computer_diagnostics')
			message = await msg.answer(MESSAGES['waiting_defects_description'], reply_markup=key)

			await self.redis.condition_data_delete(call_back_tg_id)
			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			return

		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return

		now_checking_databases_files = await self.redis.checking_databases_files_get(msg.from_user.id)

		if len(now_checking_databases_files) > 3:
			await self.__delete_now_error_message(msg.from_user.id)

			message = await msg.answer(MESSAGES['only_four_file'])

			await self.redis.error_msg_save(msg.from_user.id, message.message_id)

			return


		if msg.photo:
			document_tg_id = msg['photo'][2]['file_id']
			mime_type = 'mime/jpg'
			data = {
				'tg_id': document_tg_id,
				'mime_type': mime_type,
				'is_document': False
			}
			now_checking_databases_files.append(data)
			await self.redis.checking_databases_files_save(msg.from_user.id, now_checking_databases_files)

			file_unique_id = msg['photo'][2]['file_unique_id']
		elif msg.document:
			if msg['document']['file_size'] >= 10468488:
				await msg.answer(MESSAGES['too_file_size'])
				return

			document_extension = msg['document']['mime_type']
			try:
				await AddReportFilter.checking_databases_filter(document_extension)
			except InvalidCheckingDatabaseDocumentExtension:
				await msg.answer(MESSAGES['invalid_diagnostic_document_extension']) #------------------------------------
				return
			document_tg_id = msg['document']['file_id']
			mime_type = msg['document']['mime_type']
			if mime_type in ['image/jpg', 'image/jpeg', 'image/png']:
				data = {
					'tg_id': document_tg_id,
					'mime_type': mime_type,
					'is_document': True
				}
			else:
				data = {
					'tg_id': document_tg_id,
					'mime_type': mime_type,
					'is_document': False
				}

			now_checking_databases_files.append(data)
			await self.redis.checking_databases_files_save(msg.from_user.id, now_checking_databases_files)

			file_unique_id = msg['document']['file_unique_id']

		else:
			await msg.answer('Вы можете загружать только .pdf и фото!')

			return

		key = await self.keyboard.test()
		await msg.answer(f"Загружено: {file_unique_id}", reply_markup=key)


		if len(now_checking_databases_files) == 4:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			key = await self.keyboard.checking_databases_next_step('add_report_computer_diagnostics')
			message = await msg.answer(MESSAGES['checking_databases_all'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		print(db.is_closed())


	async def add_report_checking_databases_download_successfull(self, call: CallbackQuery, state: FSMContext):
		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(call.from_user.id, call)
			await self.__add_report_delete_now_deleted_message(call.from_user.id)
			return

		files = await self.redis.checking_databases_files_get(call.from_user.id)

		if len(files) == 0:
			if type(call) == Message:
				await AddReportState.waiting_checking_databases.set()

				await call.answer(MESSAGES['files_not_add'])
			elif type(call) == CallbackQuery:


				await AddReportState.waiting_checking_databases.set()

				await call.message.answer(MESSAGES['files_not_add'])

				await call.answer()
			return

		key = await self.keyboard.remove_kb()
		if type(call) == Message:
			await call.answer('Сжимаю файлы...', reply_markup=key)
			await self.__add_report_delete_now_deleted_message(call.from_user.id)
		elif type(call) == CallbackQuery:
			await call.message.delete()
			await call.message.answer('Сжимаю файлы...', reply_markup=key)

		for photo in files:
			if photo['is_document']:
				path = PROJECT_PATH + f'/app/Expert/photo_proxy/'

				await self.bot.download_file_by_id(photo['tg_id'], path + photo['tg_id'])
				photo_msg = ''
				while True:
					try:
						photo_msg = await self.bot.send_photo(1677813886, InputFile(path + photo['tg_id'], photo['tg_id']))
						break
					except:
						print('e')
						continue

				os.remove(path + photo['tg_id'])

				photo['tg_id'] = photo_msg['photo'][2]['file_id']


		await state.update_data(checking_databases_files=files)
		await AddReportState.waiting_defects_description.set()

		key = await self.keyboard.add_report_back_main_menu_kb('add_report_computer_diagnostics')

		if type(call) == Message:
			message = await call.answer(MESSAGES['waiting_defects_description'], reply_markup=key)
		elif type(call) == CallbackQuery:
			message = await call.message.answer(MESSAGES['waiting_defects_description'], reply_markup=key)

		await self.redis.condition_data_delete(call.from_user.id)
		await self.redis.add_report_redis_save_deleted_message_id(call.from_user.id, message.message_id)

		print(db.is_closed())



	async def add_report_defects_description(self, msg: Message, state: FSMContext, is_back=False, call_back_tg_id=None):
		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return

		if not msg.text:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_computer_diagnostics')
			message = await msg.answer(MESSAGES['waiting_defects_description'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return

		state_data = await state.get_data()
		if is_back and state_data.get('defects_description'):
			expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(call_back_tg_id)
			if expert.is_blocked:
				await self.__expert_is_blocked(call_back_tg_id, msg)
				return

			await AddReportState.waiting_defects_description.set()
			key = await self.keyboard.add_report_back_main_menu_kb('add_report_computer_diagnostics')
			message = await msg.answer(MESSAGES['waiting_defects_description'], reply_markup=key)
			await self.__add_report_delete_now_deleted_message(call_back_tg_id)
			await self.redis.add_report_redis_save_deleted_message_id(call_back_tg_id, message.message_id)
			return



		if await self.redis.condition_data_get(msg.from_user.id):
			return

		description = msg.text
		await self.redis.condition_data_save(msg.from_user.id)
		await state.update_data(defects_description=description)
		await AddReportState.waiting_voice.set()

		key = await self.keyboard.add_report_back_main_menu_kb('add_report_checking_databases')
		message = await msg.answer(MESSAGES['waiting_voice'], reply_markup=key)

		await self.redis.only_one_file_delete(msg.from_user.id)

		try:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		print(db.is_closed())


	async def add_report_voice(self, msg: Message, state: FSMContext):
		expert: ExpertModel = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		if expert.is_blocked:
			await self.__expert_is_blocked(msg.from_user.id, msg)
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
			return

		if not msg.voice:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer('Вы можете отправить только голосовое сообщение')

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_checking_databases')
			message = await msg.answer(MESSAGES['waiting_voice'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		if await self.redis.last_voice_get(msg.from_user.id):
			# await msg.answer('ARA')
			return

		try:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await msg.answer(MESSAGES['waiting_create_report'])

		voice = msg['voice']
		try:
			await AddReportFilter.only_voice_filter(voice['mime_type'])
		except InvalidVoiceExtension:
			await self.__add_report_delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['invalid_voice_extension'])

			key = await self.keyboard.add_report_back_main_menu_kb('add_report_checking_databases')
			message = await msg.answer(MESSAGES['waiting_voice'], reply_markup=key)

			await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return

		data = {
			'tg_id': voice['file_id'],
			'mime_type': voice['mime_type']
		}

		await self.redis.last_voice_save(msg.from_user.id)
		await state.update_data(voice=data)

		add_report_util = ExpertAddReportUtil()

		state_data = await state.get_data()

		state_data['expert'] = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		state_data['name'] = await add_report_util.get_report_name(state_data['VIN'])
		state_data['archive_name'] = await add_report_util.get_archive_name(state_data['VIN'])

		report = await AutoReportModel.create_report(state_data)

		archive_path = await add_report_util.add_new_report(msg.from_user.id, state_data['archive_name'])

		if state_data.get('vehicle_condition_text'):
			await add_report_util.add_about_auto_txt(await self.__get_about_auto_text(state_data, with_condition=True))
		elif state_data.get('vehicle_condition_photo_tg_id'):
			await add_report_util.add_file_to_zip(
				self.bot, 'sostoyanie_kuzova', state_data['vehicle_condition_photo_tg_id']
			)
			await add_report_util.add_about_auto_txt(await self.__get_about_auto_text(state_data))
		elif state_data.get('vehicle_condition_voice_tg_id'):

			await add_report_util.add_conver_voice_file_to_zip(self.bot, state_data['vehicle_condition_voice_tg_id']['tg_id'],
															   'sostoyanie_kuzova_ogg.ogg', 'sostoyanie_kuzova.mp3')
			await add_report_util.add_about_auto_txt(await self.__get_about_auto_text(state_data))

		else:
			about_auto_txt_text = MESSAGES['zip_auto_data'].format(
				VIN=state_data['VIN'],
				auto_number=state_data['auto_number'],
				odometer_data=state_data['odometer_data'],
				description=state_data['defects_description']
			)
			await add_report_util.add_about_auto_txt(about_auto_txt_text)

		await add_report_util.add_file_to_zip(self.bot, 'VIN_photo', state_data['VIN_photo_tg_id'])

		await add_report_util.add_conver_voice_file_to_zip(self.bot, state_data['voice']['tg_id'],
														   'sostoyanie_auto_ogg.ogg', 'sostoyanie_auto.mp3')

		await add_report_util.add_files_to_zip_folder(
			self.bot, 'photo_report', 'photo_report', state_data['defects_photos_list']
		)
		await add_report_util.add_files_to_zip_folder(
			self.bot, 'diagnostic_report', 'diagnostic_report', state_data['computer_diagnostics_files']
		)
		await add_report_util.add_files_to_zip_folder(
			self.bot, 'database_report', 'database_report', state_data['checking_databases_files']
		)

		await state.finish()

		await self.delete_state_redis_data(msg.from_user.id)

		await add_report_util.delete_proxy_folder()

		await msg.answer(MESSAGES['report_created'])


		while True:
			try:
				message = await msg.answer_document(InputFile(archive_path, archive_path))
				report.from_chat_id = msg.from_user.id
				report.message_id = message.message_id
				report.save()
				break
			except:
				print('e')
				continue


		# await FindReportState.waiting_VIN_or_autonumber.set()

		key = await self._get_now_user_find_report_key(msg.from_user.id)
		message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.redis.add_report_redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())

	# ------------------------------------------------------------------------



	# Вспомогательные функции
	# ------------------------------------------------------------------------
	async def __expert_is_blocked(self, tg_id, msg, state=None):
		if state:
			await state.finish()

		await msg.answer(MESSAGES['your_account_is_blocked'])

		# await FindReportState.waiting_VIN_or_autonumber.set()
		await msg.answer(MESSAGES['waiting_VIN_or_autonumber'])

		await self.delete_state_redis_data(tg_id)


	async def delete_state_redis_data(self, tg_id):
		await self.redis.add_report_defects_photos_delete(tg_id)
		await self.redis.computer_diagnostic_files_delete(tg_id)
		await self.redis.checking_databases_files_delete(tg_id)
		await self.redis.VIN_photo_tg_id_delete(tg_id)
		await self.redis.test_delete(tg_id)
		await self.redis.voice_delete(tg_id)
		await self.redis.computer_diagnostic_delete(tg_id)
		await self.redis.checking_databases_delete(tg_id)
		await self.redis.only_one_file_delete(tg_id)
		await self.redis.condition_data_delete(tg_id)
		await self.redis.last_voice_delete(tg_id)

	async def __get_my_account_text(self, expert):
		text = MESSAGES['expert_my_account'].format(
			id=expert.id,
			balance=expert.balance,
			rating=round(expert.rating, 1),
			reports_count=expert.auto_reports.count(),
			buy_count=expert.transactions.count()
		)
		return text

	async def __add_report_delete_now_deleted_message(self, user_tg_id):
		deleted_message_id = await self.redis.add_report_redis_get_deleted_message_id(user_tg_id) or 1623
		await self.bot.delete_message(user_tg_id, deleted_message_id)

	async def __delete_now_error_message(self, user_tg_id):
		deleted_message_id = await self.redis.error_msg_get(user_tg_id)
		if not deleted_message_id:
			deleted_message_id = await self.redis.error_msg_get(1677813886)
			await self.bot.delete_message(1677813886, deleted_message_id)
			return
		await self.bot.delete_message(user_tg_id, deleted_message_id)

	async def __get_about_auto_text(self, data, with_condition=False):
		if with_condition:
			about_auto_txt_text = MESSAGES['zip_auto_data_with_vehicle_condition_text'].format(
				VIN=data['VIN'],
				auto_number=data['auto_number'],
				odometer_data=data['odometer_data'],
				vehicle_condition=data['vehicle_condition_text'],
				description=data['defects_description']
			)
		else:
			about_auto_txt_text = MESSAGES['zip_auto_data_text'].format(
				VIN=data['VIN'],
				auto_number=data['auto_number'],
				odometer_data=data['odometer_data'],
				description=data['defects_description']
			)
		return about_auto_txt_text
	# ------------------------------------------------------------------------