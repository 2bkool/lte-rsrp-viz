from direct_redis import DirectRedis

from app.config import settings


redis = DirectRedis(host=settings.redis_host,
                    port=settings.redis_port,
                    password=settings.redis_password)
