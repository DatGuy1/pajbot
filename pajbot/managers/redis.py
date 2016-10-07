import logging
from contextlib import contextmanager

import redis

log = logging.getLogger(__name__)


class RedisManager:
    """
    Responsible for making sure exactly one instance of Redis
    is initialized with the right arguments, and returns when the
    get-method is called.
    """

    redis = None

    def init(**options):
        default_options = {
                'decode_responses': True,
                'db': 3,
                }
        default_options.update(options)
        RedisManager.redis = redis.Redis(**default_options)

    def get():
        return RedisManager.redis

    @contextmanager
    def pipeline_context():
        try:
            pipeline = RedisManager.get().pipeline()
            yield pipeline
        except:
            log.exception('Exception caught during RedisManager::pipeline_context')
            pipeline.reset()
        finally:
            pipeline.execute()
