
import json
from redis import StrictRedis

class AdminRedis():
    redis: StrictRedis

    def __init__(self):
        self.redis = StrictRedis(
            host='localhost',
            port=6379,
            charset='utf-8',
            decode_responses=True
        )

    async def redis_save_deleted_message_id(self, user_tg_id, message_id):
        self.redis.set(f"{user_tg_id}_add_report_delete_message_id", message_id, ex=2592000)

    async def redis_get_deleted_message_id(self, user_tg_id: str):
        msg_id = self.redis.get(f"{user_tg_id}_add_report_delete_message_id")
        return msg_id

    async def delete_deleted_message_id(self, user_tg_id):
        self.redis.delete(f"{user_tg_id}_add_report_delete_message_id")


    async def withdrawal_expert_id_save(self, user_tg_id, expert_id):
        self.redis.set(f"{user_tg_id}_withdrawal_expert_id", expert_id, ex=2592000)

    async def withdrawal_expert_id_get(self, user_tg_id):
        return self.redis.get(f"{user_tg_id}_withdrawal_expert_id")

    async def withdrawal_expert_id_delete(self, user_tg_id):
        return self.redis.delete(f"{user_tg_id}_withdrawal_expert_id")


    async def withdrawal_amount_save(self, user_tg_id, expert_id):
        self.redis.set(f"{user_tg_id}_withdrawal_amount", expert_id, ex=2592000)

    async def withdrawal_amount_get(self, user_tg_id):
        return self.redis.get(f"{user_tg_id}_withdrawal_amount")

    async def withdrawal_amount_delete(self, user_tg_id):
        return self.redis.delete(f"{user_tg_id}_withdrawal_amount")