
import json
from redis import StrictRedis

class UserRedis():
    redis: StrictRedis

    def __init__(self):
        self.redis = StrictRedis(
            host='localhost',
            port=6379,
            charset='utf-8',
            decode_responses=True
        )

    async def redis_save_deleted_message_id(self, user_tg_id, message_id, ex=2592000):
        self.redis.set(f"{user_tg_id}_add_report_delete_message_id", message_id, ex=2592000)

    async def redis_get_deleted_message_id(self, user_tg_id: str):
        msg_id = self.redis.get(f"{user_tg_id}_add_report_delete_message_id")
        return msg_id

    async def delete_deleted_message_id(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_add_report_delete_message_id")


    async def save_expert_complain_expert_id(self, user_tg_id, expert_id, ex=2592000):
        return self.redis.set(f"{user_tg_id}_expert_complain_expert_id", expert_id, ex=2592000)

    async def expert_complain_expert_id_get(self, user_tg_id):
        return self.redis.get(f"{user_tg_id}_expert_complain_expert_id")

    async def expert_complain_expert_id_delete(self, user_tg_id):
        return self.redis.delete(f"{user_tg_id}_expert_complain_expert_id")


    async def save_expert_complain_report_id(self, user_tg_id: str, report_id, ex=2592000):
        msg_id = self.redis.set(f"{user_tg_id}_expert_complain_report_id", report_id, ex=2592000)
        return msg_id

    async def expert_complain_report_id_get(self, user_tg_id):
        return self.redis.get(f"{user_tg_id}_expert_complain_report_id")

    async def expert_complain_report_id_delete(self, user_tg_id):
        return self.redis.delete(f"{user_tg_id}_expert_complain_report_id")

    async def complain_message_id_save(self, user_tg_id, msg_id):
        self.redis.set(f"{user_tg_id}_complain_message_id", msg_id, ex=2592000)

    async def complain_message_id_get(self, user_tg_id):
        return self.redis.get(f"{user_tg_id}_complain_message_id")

    async def complain_message_id_delete(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_complain_message_id")


    async def complain_save(self, user_tg_id):
        self.redis.set(f"{user_tg_id}_complain", user_tg_id, ex=2592000)


    async def complain_get(self, user_tg_id):
        return self.redis.get(f"{user_tg_id}_complain")

    async def complain_delete(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_complain")

