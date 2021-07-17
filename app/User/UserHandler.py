import re
import time

from aiogram.types import Message, CallbackQuery, ContentType, LabeledPrice, PreCheckoutQuery, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from main import bot

from app.BaseHandler import BaseHandler

from settings.bot_settings import PAYMENTS_PROVIDER_TOKEN
# from app.Expert.ExpertModels import AutoReportModel
from app.texts import MESSAGES
from app.User.UserKeyboard import UserKeyboard
from app.User.UserStates import FindReportState, ExpertComplaintState
from app.User.UserRedis import UserRedis

from app.Expert.ExpertModels import *
from app.Expert.ExpertHandler import ExpertHandler
# from app.User.Utils.QiwiPayment import Payment
from settings.bot_settings import PROJECT_PATH
from database.db_connect import db
from app.Expert.ExpertFilters import AddReportFilter, InvalidAutoNumberFormat
from app.User.Utils.YooKassaPayment import YookassaPayment


class UserHandler(BaseHandler):
	bot = ''
	keyboard = ''

	def __init__(self):
		self.bot = bot
		self.keyboard = UserKeyboard()
		self.redis = UserRedis()


	@classmethod
	def register_handlers(cls, dp):
		handler = cls()

		dp.register_message_handler(handler.start, commands=['start'], state='*')
		dp.register_message_handler(handler.find_report,
									# state=FindReportState.waiting_VIN_or_autonumber
									)
		# dp.register_callback_query_handler(
		# 	handler.back,
		# 	handler.keyboard.back_cd.filter(),
		# 	state=
		# )
		# dp.register_pre_checkout_query_handler(lambda query: True, handler.buy_report_pre_checkout_query, state='*')
		# dp.register_message_handler(handler.buy_report_successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT, state='*')
		dp.register_callback_query_handler(
			handler.download_report,
			handler.keyboard.download_report_cd.filter(),
			# state=FindReportState.waiting_VIN_or_autonumber
		)
		dp.register_callback_query_handler(
			handler.buy_report_start,
			handler.keyboard.buy_report_cd.filter(),
			# state=FindReportState.waiting_VIN_or_autonumber
		)
		dp.register_callback_query_handler(
			handler.check_buy_report,
			handler.keyboard.check_report_buy_cd.filter(),
			# state=FindReportState.waiting_VIN_or_autonumber
		)

		dp.register_callback_query_handler(
			handler.expert_estimation,
			handler.keyboard.expert_estimation_cd.filter(),
			state='*'
		)

		dp.register_callback_query_handler(
			handler.expert_complaint_start,
			handler.keyboard.expert_complaint_cd.filter(),
			state='*'
		)
		dp.register_message_handler(
			handler.expert_complaint_text,
			state=ExpertComplaintState.waiting_complaint_text,
			content_types=ContentType.ANY
		)
		dp.register_message_handler(
			handler.expert_complaint_phone,
			state=ExpertComplaintState.waiting_phone,
			content_types=ContentType.ANY
		)
		dp.register_callback_query_handler(
			handler.expert_buy_report_from_balance,
			handler.keyboard.expert_buy_from_balance_cd.filter(),
			# state=FindReportState.waiting_VIN_or_autonumber
		)

	async def back(self, call: CallbackQuery, callback_data: dict, state=None):

		if state:
			state_data = await state.get_data()
			if len(state_data) <= 1:
				await state.finish()

		function_start = callback_data.get('function_start')

		functions = {
			'start': self.start
		}
		# print(str(call.from_user.id) + 'backbackback')
		function = functions[function_start]
		if function_start in ['add_report_start']:
			await function(call, state=state, is_back=True, call_back_tg_id=call.from_user.id)
		else:
			await function(call.message, state=state, is_back=True, call_back_tg_id=call.from_user.id)

		await call.message.delete()

		print(db.is_closed())


	async def start(self, msg: Message, state=None, is_back=False, call_back_tg_id=None):
		expert_handler = ExpertHandler()
		await expert_handler.delete_state_redis_data(msg.from_user.id)

		if is_back:
			if state:
				await state.finish()
			# await FindReportState.waiting_VIN_or_autonumber.set()

			key = await self._get_now_user_find_report_key(call_back_tg_id)
			message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

			# await self.__delete_now_deleted_message(msg.from_user.id)
			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

			# await self.__delete_now_deleted_message(msg.from_user.id)

		if state:
			await state.finish()

		# await FindReportState.waiting_VIN_or_autonumber.set()

		if msg.reply_markup:
			rm_key = await self.keyboard.remove_kb()
			m = await msg.answer('a', reply_markup=rm_key)
			await m.delete()

		key = await self._get_now_user_find_report_key(msg.from_user.id)
		message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		try:
			await self.__delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def find_report(self, msg: Message):
		try:
			await AddReportFilter.VIN_filter(msg.text.upper())
		except:
			try:
				auto_number = msg.text

				auto_number = auto_number.upper()
				intab = 'ABEKMHOPCTYX'
				outtab = 'АВЕКМНОРСТУХ'
				number = auto_number.maketrans(intab, outtab)

				auto_number = auto_number.translate(number).lower()

				await AddReportFilter.auto_number_filter(auto_number.upper())
			except InvalidAutoNumberFormat:
				await msg.answer('Неверный формат VIN (гос.номера)')
				key = await self._get_now_user_find_report_key(msg.from_user.id)
				message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

				try:
					await self.__delete_now_deleted_message(msg.from_user.id)
				except:
					pass
				await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
				db.close()
				print(db.is_closed())
				return



		reports = (await AutoReportModel.find_reports_by_auto_number_or_none(msg.text) or
			 await AutoReportModel.get_by_VIN_or_none(msg.text))

		if not reports:
			await msg.answer(MESSAGES['report_does_not_exist'])

			key = await self._get_now_user_find_report_key(msg.from_user.id)
			message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

			try:
				await self.__delete_now_deleted_message(msg.from_user.id)
			except:
				pass
			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			db.close()
			print(db.is_closed())
			return

		try:
			await msg.answer(f"По данному VIN (гос.номеру) найдено отчётов: {reports.count()}")
		except:
			count = len(reports)

			await msg.answer(f"По данному VIN (гос.номеру) найдено отчётов: {count}")

		report_price = await ReportPriceModel.get_now_commission()
		print(reports)

		expert = await ExpertModel.get_by_tg_id_or_none(msg.from_user.id)
		for report in reports:
			if expert and expert.is_admin:
				report_text = MESSAGES['user_report_for_admin'].format(
				name=report.name,
				VIN=report.VIN,
				auto_number=report.auto_number,
				create_date=report.create_date.strftime('%d.%m.%Y'),
				rating=round(report.expert.rating, 1),
				FIO=report.expert.FIO,
				phone=report.expert.phone,
				price=report_price.amount
				)
			else:
				report_text = MESSAGES['user_report'].format(
					name=report.name,
					VIN=report.VIN,
					auto_number=report.auto_number,
					create_date=report.create_date.strftime('%d.%m.%Y'),
					rating=round(report.expert.rating, 1),
					price=report_price.amount
				)


			if expert and expert.is_admin:
				key = await self.keyboard.download_report_kb(report.id)
			elif await report.check_expert(msg.from_user.id):
				key = await self.keyboard.download_report_kb(report.id)
			elif await TransactionModel.check_user_buy_report(report, msg.from_user.id):
				key = await self.keyboard.download_report_kb(report.id)
			else:
				if expert and expert.balance >=report_price.amount:
					key = await self.keyboard.expert_buy_from_balance(expert.id, report.id, report_price.amount)
				else:
					# payment = Payment()
					# await payment.create(amount=report_price.amount)
					payment = await YookassaPayment.create_payment(report.name, report_price.amount)
					payment_link = payment.confirmation.confirmation_url
					# TransactionCheckModel.create(
					# 	pay_id=payment.id,
					# 	client_tg_id=msg.from_user.id,
					# 	report_from_user_tg_id=report.from_chat_id,
					# 	report_message_id=report.message_id
					# )

					key = await self.keyboard.waiting_buy_report(report.id, payment.id, payment_link, report_price.amount)

				# key = await self.keyboard.buy_report_kb(report.id, report_price.amount)

			await msg.answer(report_text, reply_markup=key)

		await msg.answer_document(InputFile(PROJECT_PATH+'/dogovor.pdf', 'Пользовательское_соглашение.pdf'), caption=MESSAGES['user_agreement'])

		key = await self._get_now_user_find_report_key(msg.from_user.id)
		message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		try:
			await self.__delete_now_deleted_message(msg.from_user.id)
		except:
			pass
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())

	async def download_report(self, call: CallbackQuery, callback_data: dict):
		report_id = callback_data.get('report_id')
		report = await AutoReportModel.get_by_id_or_none(report_id)

		await call.message.answer('<b>Скачайте файл с отчётом 👇</b>')
		try:
			await self.bot.copy_message(call.from_user.id, report.from_chat_id, report.message_id)
		except:
			await call.message.answer_document(InputFile(PROJECT_PATH+'/archives/'+report.archive_name, report.name))

		key = await self._get_now_user_find_report_key(call.from_user.id)
		message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)
		await self.__delete_now_deleted_message(call.from_user.id)
		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)


		await call.answer()

		db.close()
		print(db.is_closed())


	# Логика покупки отчёта
	# ---------------------------------------------------------------------
	async def expert_buy_report_from_balance(self, call: CallbackQuery, callback_data):
		expert_id = callback_data.get('expert_id')
		report_id = callback_data.get('report_id')

		expert = await ExpertModel.get_by_id_or_none(expert_id)
		report = await AutoReportModel.get_by_id_or_none(report_id)

		now_report_price = await ReportPriceModel.get_now_commission()
		now_commission = await CommissionModel.get_now_commission()

		if expert.balance < now_report_price.amount:
			await call.message.answer('Не хватает средств на балансе❗️')
			return

		transaction = await TransactionModel.create_transaction(
			client=call.from_user.id,
			expert=report.expert,
			auto_report=report.name,
			amount=int(now_report_price.amount - now_commission.amount)
		)

		await report.expert.update_balance(report.expert.balance + (now_report_price.amount - now_commission.amount))
		await expert.update_balance(expert.balance - now_report_price.amount)

		key = await self.keyboard.download_report_kb(report.id)
		await self.bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=key)

		await call.message.answer('<b>Скачайте файл с отчётом 👇</b>')

		try:
			await self.bot.copy_message(call.from_user.id, report.from_chat_id, report.message_id)
		except:
			await call.message.answer_document(InputFile(PROJECT_PATH+'/archives/'+report.archive_name, report.name))

		time.sleep(0.5)
		key = await self.keyboard.expert_estimation_or_complaint(report.expert.id, report.id)
		await call.message.answer(MESSAGES['expert_estimation_or_complaint'], reply_markup=key)
		time.sleep(0.5)
		key = await self._get_now_user_find_report_key(call.from_user.id)
		message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)
		time.sleep(0.5)
		await self.__delete_now_deleted_message(call.from_user.id)
		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)
		await call.answer()


	async def buy_report_start(self, call: CallbackQuery, callback_data: dict):
		amount = callback_data.get('price')

		report_id = callback_data.get('report_id')
		report = await AutoReportModel.get_by_id_or_none(report_id)

		payment = Payment()
		await payment.create(amount=amount)

		report_price = await ReportPriceModel.get_now_commission()

		report_text = MESSAGES['user_report'].format(
			name=report.name,
			VIN=report.VIN,
			auto_number=report.auto_number,
			create_date=report.create_date,
			rating=report.expert.rating,
			price=report_price.amount
		)

		key = await self.keyboard.waiting_buy_report(report.id, payment.id, await payment.get_invoice_link(), report_price.amount)
		await call.message.answer(report_text, reply_markup=key)


		db.close()
		print(db.is_closed())


		# await msg.answer(MESSAGES['deposit'].format(link=await payment.get_invoice_link()), reply_markup=key)

	async def check_buy_report(self, call: CallbackQuery, callback_data: dict):
		payment_id = callback_data.get('payment_id')
		amount = int(callback_data.get('amount'))
		payment_status = await YookassaPayment.check_payment_status(payment_id)


		report_id = callback_data.get('report_id')
		report = await AutoReportModel.get_by_id_or_none(report_id)
		now_commission = await CommissionModel.get_now_commission()
		now_report_price = await ReportPriceModel.get_now_commission()

		# if await payment.check_payment():
		if payment_status == 'succeeded':


			transaction = await TransactionModel.create_transaction(
				client=call.from_user.id,
				expert=report.expert,
				auto_report=report.name,
				amount=int(now_report_price.amount-now_commission.amount)
			)
			# await self.bot.send_document()

			await report.expert.update_balance(report.expert.balance + (now_report_price.amount-now_commission.amount))

			key = await self.keyboard.download_report_kb(report.id)
			await self.bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=key)

			await call.message.answer('<b>Скачайте файл с отчётом 👇</b>')

			try:
				await self.bot.copy_message(call.from_user.id, report.from_chat_id, report.message_id)
			except:
				await call.message.answer_document(
					InputFile(PROJECT_PATH + '/archives/' + report.archive_name, report.name))

			time.sleep(0.5)
			key = await self.keyboard.expert_estimation_or_complaint(report.expert.id, report.id)
			await call.message.answer(MESSAGES['expert_estimation_or_complaint'], reply_markup=key)
			time.sleep(0.5)
			key = await self._get_now_user_find_report_key(call.from_user.id)
			message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)
			time.sleep(0.5)
			await self.__delete_now_deleted_message(call.from_user.id)
			await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)
			await call.answer()
		else:
			await call.message.answer('Оплата не прошла❗️')

			# await FindReportState.waiting_VIN_or_autonumber.set()

			key = await self._get_now_user_find_report_key(call.from_user.id)
			message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

			await self.__delete_now_deleted_message(call.from_user.id)
			await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)
			await call.answer()

		db.close()
		print(db.is_closed())

	async def expert_estimation(self, call: CallbackQuery, callback_data: dict, state: FSMContext):
		expert_id = callback_data.get('expert_id')
		expert = await ExpertModel.get_by_id_or_none(expert_id)

		estimation = int(callback_data.get('estimation'))
		await EstimationModel.add_expert_estimataion(expert, estimation)

		await expert.update_rating()

		await state.finish()

		# await FindReportState.waiting_VIN_or_autonumber.set()

		await call.message.answer(MESSAGES['expert_estimation_success'])

		key = await self._get_now_user_find_report_key(call.from_user.id)
		message = await call.message.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.__delete_now_deleted_message(call.from_user.id)
		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		await call.message.delete()

		db.close()
		print(db.is_closed())



	async def expert_complaint_start(self, call: CallbackQuery, callback_data, state=None):
		await state.finish()

		report_id = callback_data.get('report_id')

		await self.redis.save_expert_complain_report_id(call.from_user.id, report_id)

		await ExpertComplaintState.waiting_complaint_text.set()

		key = await self.keyboard.cancel_kb('start')
		message = await call.message.answer(MESSAGES['expert_complaint'], reply_markup=key)

		await self.redis.complain_message_id_save(call.from_user.id, call.message.message_id)

		await self.__delete_now_deleted_message(call.from_user.id)
		await self.redis.redis_save_deleted_message_id(call.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def expert_complaint_text(self, msg: Message, state: FSMContext):
		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.cancel_kb('start')
			message = await msg.answer(MESSAGES['expert_complaint'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return

		if not msg.from_user.username:
			await state.update_data(text=msg.text)

			await ExpertComplaintState.waiting_phone.set()

			key = await self.keyboard.cancel_kb('start')
			message = await msg.answer(MESSAGES['expert_complaint_client_not_tg_username'], reply_markup=key)

			await self.__delete_now_deleted_message(msg.from_user.id)
			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			db.close()
			print(db.is_closed())
			return

		report_id = await self.redis.expert_complain_report_id_get(msg.from_user.id)
		report = await AutoReportModel.get_by_id_or_none(report_id)

		if report.expert.tg_username:
			text = MESSAGES['expert_complaint_admin'].format(
				complaint_text=msg.text,
				report_name=report.name,
				expert_data=f"@{report.expert.tg_username}",
				client_data=f"@{msg.from_user.username}"
			)
		else:
			text = MESSAGES['expert_complaint_admin'].format(
				complaint_text=msg.text,
				report_name=report.name,
				expert_data=f"{report.expert.phone}",
				client_data=f"@{msg.from_user.username}"
			)

		super_admin = await ExpertModel.get_super_admin()

		await state.finish()
		await self.redis.expert_complain_report_id_delete(msg.from_user.id)

		await self.bot.send_message(super_admin.tg_id, text)
		await self.bot.copy_message(super_admin.tg_id, report.from_chat_id, report.message_id)

		await msg.answer(MESSAGES['expert_complaint_success_send'])

		# await FindReportState.waiting_VIN_or_autonumber.set()

		key = await self._get_now_user_find_report_key(msg.from_user.id)
		message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.bot.delete_message(
			msg.from_user.id,
			await self.redis.complain_message_id_get(msg.from_user.id)
		)
		await self.redis.complain_message_id_delete(msg.from_user.id)

		await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())


	async def expert_complaint_phone(self, msg: Message, state: FSMContext):
		if not msg.text:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_text_msg'])

			key = await self.keyboard.cancel_kb('start')
			message = await msg.answer(MESSAGES['expert_complaint_client_not_tg_username'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)


		phone = msg.text
		try:
			int(phone)
		except:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer(MESSAGES['only_int_msg'])

			key = await self.keyboard.cancel_kb('start')
			message = await msg.answer(MESSAGES['expert_complaint_client_not_tg_username'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

			return


		if len(phone) > 12:
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer('Неверный формат номера телефона')

			key = await self.keyboard.cancel_kb('start')
			message = await msg.answer(MESSAGES['expert_complaint_client_not_tg_username'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return


		if not re.match('[+, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]{11,12}', phone):
			await self.__delete_now_deleted_message(msg.from_user.id)

			await msg.answer('Неверный формат номера телефона')

			key = await self.keyboard.cancel_kb('start')
			message = await msg.answer(MESSAGES['expert_complaint_client_not_tg_username'], reply_markup=key)

			await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)
			return


		report_id = await self.redis.expert_complain_report_id_get(msg.from_user.id)
		report = await AutoReportModel.get_by_id_or_none(report_id)

		state_data = await state.get_data()
		text = state_data.get('text')

		if report.expert.tg_username:
			text = MESSAGES['expert_complaint_admin'].format(
				complaint_text=text,
				report_name=report.name,
				expert_data=f"@{report.expert.tg_username or report.expert.phone}",
				client_data=phone
			)
		else:
			text = MESSAGES['expert_complaint_admin'].format(
				complaint_text=text,
				report_name=report.name,
				expert_data=f"{report.expert.phone}",
				client_data=phone
			)

		super_admin = await ExpertModel.get_super_admin()

		await state.finish()

		await self.bot.send_message(super_admin.tg_id, text)
		await self.bot.copy_message(super_admin.tg_id, report.from_chat_id, report.message_id)

		await msg.answer(MESSAGES['expert_complaint_success_send'])

		# await FindReportState.waiting_VIN_or_autonumber.set()

		key = await self._get_now_user_find_report_key(msg.from_user.id)
		message = await msg.answer(MESSAGES['waiting_VIN_or_autonumber'], reply_markup=key)

		await self.bot.delete_message(
			msg.from_user.id,
			await self.redis.complain_message_id_get(msg.from_user.id)
		)
		await self.redis.complain_message_id_delete(msg.from_user.id)
		await self.redis.expert_complain_report_id_delete(msg.from_user.id)

		await self.__delete_now_deleted_message(msg.from_user.id)
		await self.redis.redis_save_deleted_message_id(msg.from_user.id, message.message_id)

		db.close()
		print(db.is_closed())

	# ---------------------------------------------------------------------



	# Вспомогательные функции
	# ---------------------------------------------------------------------

	async def __delete_now_deleted_message(self, user_tg_id):
		now_deleted_message_id = await self.redis.redis_get_deleted_message_id(user_tg_id)
		await self.bot.delete_message(user_tg_id, now_deleted_message_id)
		await self.redis.delete_deleted_message_id(user_tg_id)

	# ---------------------------------------------------------------------
