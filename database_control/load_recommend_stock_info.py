from datetime import datetime

from database_control.db_connection import get_connection


async def load_recommend_stock_to_buy():
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                select 
                    market_code
                    , company_name
                    , current_price
                    , find_date
                    , first_find_date
                    , max_hold_period
                    , concat(cast(round(target_profit_rate * 100, 2) as char), '%') as target_profit_rate
                from recommend_stock_info
                where
                    buy_try_yn = 'N'
                    and bucket = 1
                    and slack_channel_name is null
                    and find_date >= '{datetime.today().date()}' - interval 30 day
            """)

            rows = await cur.fetchall()
            columns = [x[0] for x in cur.description]

            return [dict(zip(columns, row)) for row in rows]


async def load_recommend_stock_to_additional_buy():
    async with await get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                select 
                    market_code
                    , company_name
                    , current_price
                    , find_date
                    , first_find_date
                    , max_hold_period
                    , concat(cast(round(target_profit_rate * 100, 2) as char), '%') as target_profit_rate
                    , parent_slack_channel_id
                    , parent_slack_channel_name
                    , parent_slack_thread_ts
                from recommend_stock_info
                where
                    buy_try_yn = 'N'
                    and bucket >= 2
                    and slack_channel_name is null
                    and find_date >= '{datetime.today().date()}' - interval 30 day
            """)

            rows = await cur.fetchall()
            columns = [x[0] for x in cur.description]

            return [dict(zip(columns, row)) for row in rows]
