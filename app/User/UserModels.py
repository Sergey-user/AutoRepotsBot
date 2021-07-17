from peewee import CharField, IntegerField

from database.BaseModel import BaseModel


class UserModel(BaseModel):
    tg_id = IntegerField()
    tg_username = CharField(null=True)


    class Meta:
        db_table = 'users'
