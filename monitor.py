import time
import os
from datetime import datetime
from fetcher import fetch_stock_data
from notifier import send_email


from dotenv import load_dotenv


from fetcher import fetch_stock_data
from notifier import send_email

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量获取收件人的邮箱地址
recipient_email = os.getenv("RECIPIENT_EMAIL")

# 如果未设置收件人邮箱，则抛出错误
if not recipient_email:
    raise ValueError("Recipient email not set in environment variables.")

# 定义要监控的股票列表
stocks_to_monitor = [
    # {
    #     "stock_code": "sz123252",  # 股票代码
    #     "cost_price": 130.814,       # 成本价
    #     "increase_threshold": 10.0, # 涨幅度阈值（百分比）
    #     "decrease_threshold": 10.0  # 跌幅度阈值（百分比）
    # },
    {
        "stock_code": "sz123252",  # 股票代码
        "cost_price": 136,       # 成本价
        "increase_threshold": 3.0, # 涨幅度阈值（百分比）
        "decrease_threshold": 2.0  # 跌幅度阈值（百分比）
    }
    # 可以添加更多股票
]


def is_market_open():
    now = datetime.now()
    # 9:30 AM - 11:30 AM or 1:00 PM - 3:00 PM
    if (now.hour == 9 and now.minute >= 30) or (now.hour >= 10 and now.hour < 11) or (now.hour == 11 and now.minute < 30):
        return True
    elif (now.hour == 13 and now.minute >= 0) or (now.hour > 13 and now.hour < 15):
        return True
    return False



def check_price_changes(stock_data, stock_info):
    current_price = stock_data["current_price"]
    cost_price = stock_info["cost_price"]
    increase_threshold = stock_info["increase_threshold"]
    decrease_threshold = stock_info["decrease_threshold"]

    # 计算涨幅和跌幅
    price_change_percent = ((current_price - cost_price) / cost_price) * 100
    print(f'{datetime.now():%Y-%m-%d %H:%M:%S}, name: {stock_data["name"]}, ' +
          f'current price: {current_price:.2f}, price change percent:  {price_change_percent:+.2f}%')

    if price_change_percent >= increase_threshold:
        subject = f"Stock Alert: {stock_data['name']} ({stock_data['code']})"
        body = f"The stock has increased by {price_change_percent:.2f}%.\nCurrent Price: {current_price}.\nCost Price: {cost_price}."
        send_email(subject, body, recipient_email)
        print(f"Sent increase alert for {stock_data['name']}.")
    elif price_change_percent <= -decrease_threshold:
        subject = f"Stock Alert: {stock_data['name']} ({stock_data['code']})"
        body = f"The stock has decreased by {price_change_percent:.2f}%.\nCurrent Price: {current_price}.\nCost Price: {cost_price}."
        send_email(subject, body, recipient_email)
        print(f"Sent decrease alert for {stock_data['name']}.")


def monitor_stocks():
    while True:
        if is_market_open():
            for stock_info in stocks_to_monitor:
                stock_data = fetch_stock_data(stock_info["stock_code"])
                check_price_changes(stock_data, stock_info)
            time.sleep(60)  # 每分钟检查一次
        else:
            print("Stock market is closed. Waiting for market hours...")
            time.sleep(60)  # 每分钟检查一次，直到市场开盘
            

if __name__ == "__main__":
    data = fetch_stock_data(stocks_to_monitor[0]['stock_code']) 
    check_price_changes(data, stocks_to_monitor[0])