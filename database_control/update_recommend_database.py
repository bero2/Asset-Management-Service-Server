from database_control.db_connection import get_connection


async def update_slack_info(
        market_code: str,
        find_date: str,
        first_find_date: str,
        parent_channel_name: str,
        parent_channel_id: str,
        parent_thread_ts: str,
        channel_name: str,
        channel_id: str,
        thread_ts: str
):
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                update recommend_stock_info
                set parent_slack_channel_id = '{parent_channel_id}', parent_slack_channel_name = '{parent_channel_name}', parent_slack_thread_ts = '{parent_thread_ts}',
                    slack_channel_id = '{channel_id}', slack_channel_name = '{channel_name}', slack_thread_ts = '{thread_ts}'
                where
                    market_code = '{market_code}'
                    and find_date = '{find_date}'
                    and first_find_date = '{first_find_date}'
            """)
            conn.commit()
