from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage


from settings import bot_settings
from database.db_connect import db

storage = RedisStorage('localhost', port=6379, db=5)

bot = Bot(bot_settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

def bot_start():
	# from app.BaseHandler import BaseHandler
	from app.StandartHandler import StandartHandler
	from app.User.UserHandler import UserHandler
	from app.Expert.ExpertHandler import ExpertHandler
	from app.Admin.AdminHandler import AdminHandler

	# from app.Expert import ExpertModels
	# from app.Admin import AdminModels

	# BaseHandler.register_handlers(dp)
	AdminHandler.register_handlers(dp)
	ExpertHandler.register_handlers(dp)

	StandartHandler.register_handlers(dp)
	UserHandler.register_handlers(dp)

async def on_shutdown(dp):
	db.close()

if __name__ == '__main__':
	# db.close()
	print(db.is_closed())
	bot_start()
	executor.start_polling(dp, on_shutdown=on_shutdown)