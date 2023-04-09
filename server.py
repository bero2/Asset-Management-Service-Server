from typing import Dict, Optional

import asyncio
from fastapi import FastAPI
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web import SlackResponse

from async_retrying import retry
from utils.message_formatter import recommend_message_formatter as rmf
import database_control.load_recommend_stock_info as db_load
import database_control.update_recommend_database as db_update
import logging
import configparser


config = configparser.ConfigParser()
config.read(['./server.conf', '../server.conf'])
slack_bot_token = dict(config['slack'])['token']

client = WebClient(token=slack_bot_token)

app = FastAPI()

logger = logging.getLogger(__name__)


@retry(attempts=10)
async def send_slack_message(channel: str, text: str, thread_ts: Optional[str] = None, reply_broadcast: Optional[bool] = None) -> SlackResponse:
    return client.chat_postMessage(
            channel=f"#{channel}",
            text=text,
            thread_ts=thread_ts,
            reply_broadcast=reply_broadcast
     )


@app.get("/recommend")
async def recommend(channel: str) -> Dict:
    first_buy_info, additional_buy_info = await asyncio.gather(
        db_load.load_recommend_stock_to_buy(),
        db_load.load_recommend_stock_to_additional_buy()
    )

    # 최초 매수
    for item in first_buy_info:
        text = rmf(item)
        try:
            response = await send_slack_message(channel=channel, text=text)
            await db_update.update_slack_info(
                market_code=item['market_code'],
                find_date=item['find_date'],
                first_find_date=item['first_find_date'],
                parent_channel_name=channel,
                parent_channel_id=response['channel'],
                parent_thread_ts=response['ts'],
                channel_name=channel,
                channel_id=response['ts'],
                thread_ts=response['channel']
            )
        except SlackApiError as e:
            logger.error("Error sending message: {}".format(e))

    # 추가 매수의 경우 쓰레드로 발송
    for item in additional_buy_info:
        text = rmf(item)
        try:
            response = await send_slack_message(channel=channel, text=text, thread_ts=item["parent_slack_thread_ts"], reply_broadcast=True)
            await db_update.update_slack_info(
                market_code=item['market_code'],
                find_date=item['find_date'],
                first_find_date=item['first_find_date'],
                parent_channel_name=item['parent_slack_channel_name'],
                parent_channel_id=item['parent_slack_channel_id'],
                parent_thread_ts=item['parent_slack_thread_ts'],
                channel_name=channel,
                channel_id=response['channel'],
                thread_ts=response['ts']
            )
        except SlackApiError as e:
            logger.error("Error sending message: {}".format(e))

    return {}



