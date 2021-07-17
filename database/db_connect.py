from peewee import MySQLDatabase

from settings import db_settings

db = MySQLDatabase(
	database=db_settings.DB_NAME,
	user=db_settings.USER_LOGIN,
	password=db_settings.USER_PASSWORD,
	host=db_settings.HOST
)
