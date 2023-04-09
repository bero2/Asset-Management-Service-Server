def recommend_message_formatter(item: dict) -> str:
    return f"""
# *추천 종목*
> *종목 코드* : {item['market_code']}
> *회사 이름* : {item['company_name']}
> *전일 종가* : {item['current_price']}원
> *탐색 날짜* : {item['find_date']}
> *보유 기간* : 마지막 매수일로 부터 최대 {item['max_hold_period']}일
> *목표 수익율* : {item['target_profit_rate']}
> *토스 증권 링크* : <supertoss://securities?url=https%3A%2F%2Fservice.tossinvest.com%2F%3FnextLandingUrl%3D%252Fstocks%252FA{item['market_code']}&clearHistory=true&swipeRefresh=true|{item['company_name']}>   
"""
