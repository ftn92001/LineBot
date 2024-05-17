from django_redis import get_redis_connection

class RedisService:
    def __init__(self):
        self.con = get_redis_connection("default")

    def set_value(self, key, value, expire_time=None):
        self.con.set(key, value)
        if expire_time:
            self.con.expire(key, expire_time)

    def get_value(self, key):
        return self.con.get(key)

    def check_exists(self, key):
        return self.con.exists(key)

    def delete_value(self, key):
        return self.con.delete(key)
