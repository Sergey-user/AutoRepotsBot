
import json
from redis import StrictRedis

class ExpertRedis():
    redis: StrictRedis

    def __init__(self):
        self.redis = StrictRedis(
            host='localhost',
            port=6379,
            charset='utf-8',
            decode_responses=True
        )

    async def add_report_redis_save_deleted_message_id(self, user_tg_id, message_id):
        self.redis.set(f"{user_tg_id}_add_report_delete_message_id", message_id, ex=2592000)

    async def add_report_redis_get_deleted_message_id(self, user_tg_id: str):
        msg_id = self.redis.get(f"{user_tg_id}_add_report_delete_message_id")
        return msg_id

    async def delete_deleted_message_id(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_add_report_delete_message_id")

    # async def add_report_delete_now_deleted_message(self, user_tg_id):
    #     deleted_message_id = await self.add_report_redis_get_deleted_message_id(user_tg_id)
    #     await self.bot.delete_message(user_tg_id, deleted_message_id)

    async def add_report_defects_photos_redis_save(self, user_tg_id, defect_photo_data):
        # self.redis.lpush(f"{user_tg_id}_defects_photos_save", json.dumps(defect_photo_data))
        self.redis.set(f"{user_tg_id}_defects_photos_save", json.dumps(defect_photo_data), ex=2592000)

    async def add_report_defects_photos_get(self, user_tg_id):
        # return json.loads(self.redis.lrange(f"{user_tg_id}_defects_photos_save", 0, -1)) or []
        try:
            return json.loads(self.redis.get(f"{user_tg_id}_defects_photos_save"))
        except TypeError:
            return []

    async def add_report_defects_photos_delete(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_defects_photos_save")

    async def computer_diagnostic_file_save(self, user_tg_id, files):
        # self.redis.lpush(f"{user_tg_id}_computer_diagnostics_save", json.dumps(file_id))
        self.redis.set(f"{user_tg_id}_computer_diagnostics_save", json.dumps(files), ex=2592000)

    async def computer_diagnostic_files_get(self, user_tg_id):
        try:
            return json.loads(self.redis.get(f"{user_tg_id}_computer_diagnostics_save"))
        except TypeError:
            return []

    async def computer_diagnostic_files_delete(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_computer_diagnostics_save")


    async def checking_databases_files_save(self, user_tg_id, files):
        # self.redis.lpush(f"{user_tg_id}_computer_diagnostics_save", json.dumps(file_id))
        self.redis.set(f"{user_tg_id}_checking_databases_files_save", json.dumps(files), ex=2592000)

    async def checking_databases_files_get(self, user_tg_id):
        try:
            return json.loads(self.redis.get(f"{user_tg_id}_checking_databases_files_save"))
        except TypeError:
            return []

    async def checking_databases_files_delete(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_checking_databases_files_save")

    async def VIN_photo_tg_id_save(self, user_tg_id):
        self.redis.set(f"{user_tg_id}_VIN_photo_tg_id_sv", user_tg_id, ex=2592000)
        # self.redis.set(f"{user_tg_id}_VIN_photo_tg_id", photo_tg_id)

    async def VIN_photo_tg_id_get(self, user_tg_id):
        return self.redis.get(f"{user_tg_id}_VIN_photo_tg_id_sv")
        # return self.redis.get(f"{user_tg_id}_VIN_photo_tg_id")

    async def VIN_photo_tg_id_delete(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_VIN_photo_tg_id_sv")

    async def test_save(self, tg_id, msg):
        self.redis.set(f"{tg_id}_test", json.dumps(msg), ex=2592000)

    async def test_get(self, tg_id):
        try:
            return json.loads(self.redis.get(f"{tg_id}_test"))
        except TypeError:
            return []

    async def test_delete(self, tg_id):
        self.redis.delete(f"{tg_id}_test")


    async def voice_save(self, tg_id, msg):
        self.redis.set(f"{tg_id}_voice", json.dumps(msg), ex=2592000)

    async def voice_get(self, tg_id):
        try:
            return json.loads(self.redis.get(f"{tg_id}_voice"))
        except TypeError:
            return []

    async def voice_delete(self, tg_id):
        self.redis.delete(f"{tg_id}_voice")


    async def computer_diagnostic_save(self, tg_id, msg):
        self.redis.set(f"{tg_id}_computer_diagnostic", json.dumps(msg), ex=2592000)

    async def computer_diagnostic_get(self, tg_id):
        try:
            return json.loads(self.redis.get(f"{tg_id}_computer_diagnostic"))
        except TypeError:
            return []

    async def computer_diagnostic_delete(self, tg_id):
        self.redis.delete(f"{tg_id}_computer_diagnostic")


    async def checking_databases_save(self, tg_id, msg):
        self.redis.set(f"{tg_id}_checking_databases", json.dumps(msg), ex=2592000)

    async def checking_databases_get(self, tg_id):
        try:
            return json.loads(self.redis.get(f"{tg_id}_checking_databases"))
        except TypeError:
            return []

    async def checking_databases_delete(self, tg_id):
        self.redis.delete(f"{tg_id}_checking_databases")

    async def only_one_file_save(self, id, msg):
        self.redis.set(f"{id}_VIN_delete", msg, ex=2592000)

    async def only_one_file_get(self, id):
        id = self.redis.get(f"{id}_VIN_delete")
        return id

    async def only_one_file_delete(self, id):
        self.redis.delete(f"{id}_VIN_delete")


    async def condition_data_save(self, id):
        self.redis.set(f"{id}_condition_data", id, ex=2592000)

    async def condition_data_get(self, id):
        id = self.redis.get(f"{id}_condition_data")
        return id

    async def condition_data_delete(self, id):
        self.redis.delete(f"{id}_condition_data")


    async def last_voice_save(self, id):
        self.redis.set(f"{id}_last_voice", id, ex=2592000)

    async def last_voice_get(self, id):
        id = self.redis.get(f"{id}_last_voice")
        return id

    async def last_voice_delete(self, id):
        self.redis.delete(f"{id}_last_voice")


    async def error_msg_save(self, user_tg_id, message_id):
        self.redis.set(f"{user_tg_id}_error_msg", message_id, ex=2592000)

    async def error_msg_get(self, user_tg_id: str):
        msg_id = self.redis.get(f"{user_tg_id}_error_msg")
        return msg_id

    async def error_msg_delete(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_error_msg")


