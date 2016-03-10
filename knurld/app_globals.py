from dogpile.cache import make_region

from config import Configuration

config = Configuration().config

region = make_region().configure('dogpile.cache.memory',
                                 expiration_time=config['TOKEN_EXPIRES'],
                                 )
