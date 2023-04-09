import aiomysql
from typing import *
import configparser

config = configparser.ConfigParser()
config.read(['./server.conf', '../server.conf'])
db_config: MutableMapping[str, str] = dict(config['mysql'])


async def get_connection():
    conn = await aiomysql.connect(
        host=db_config['host'],
        port=int(db_config['port']),
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['db'],
        autocommit=True,
    )
    return conn
