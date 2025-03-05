import requests

def fetch_stock_data(stock_code: str):
    url = f"http://qt.gtimg.cn/q={stock_code}"
    response = requests.get(url)
    response.encoding = "gbk"  # 解决中文乱码
    data = response.text.split("=")[1].strip('"').split("~")
    data = [item for item in data if item.strip()]
    
    return {
        "name": data[1],
        "code": data[2],
        "current_price": float(data[3]),
        "yesterday_close": float(data[4]),
        "today_open": float(data[5]),
        "volume": int(data[6]),
        "turnover": int(data[7]),
        "buy_one": float(data[9]),
        "sell_one": float(data[19]),
        # "price_change": float(data[31]),
        # "price_change_percent": float(data[32]),
        # "highest": float(data[33]),
        # "lowest": float(data[34]),
        # "turnover_rate": float(data[38]),
        # "pe_ratio": float(data[39]),
        # "market_cap": float(data[45]),
    }

def fetch_funds_flow(stock_code: str):
    url = f"http://qt.gtimg.cn/q=ff_{stock_code}"
    response = requests.get(url)
    response.encoding = "gbk"
    data = response.text.split("=")[1].strip('"').split("~")
    
    return {
        "code": data[0],
        "main_inflow": float(data[1]),
        "main_outflow": float(data[2]),
        "main_net_inflow": float(data[3]),
        "retail_inflow": float(data[5]),
        "retail_outflow": float(data[6]),
        "retail_net_inflow": float(data[7]),
        "total_funds_flow": float(data[9]),
        "name": data[12],
        "date": data[13],
    }

def fetch_market_analysis(stock_code: str):
    url = f"http://qt.gtimg.cn/q=s_pk{stock_code}"
    response = requests.get(url)
    response.encoding = "gbk"
    data = response.text.split("=")[1].strip('"').split("~")
    
    return {
        "big_buy_orders": float(data[0]),
        "small_buy_orders": float(data[1]),
        "big_sell_orders": float(data[2]),
        "small_sell_orders": float(data[3]),
    }

def fetch_stock_summary(stock_code: str):
    url = f"http://qt.gtimg.cn/q=s_{stock_code}"
    response = requests.get(url)
    response.encoding = "gbk"
    data = response.text.split("=")[1].strip('"').split("~")
    
    return {
        "name": data[1],
        "code": data[2],
        "current_price": float(data[3]),
        "price_change": float(data[4]),
        "price_change_percent": float(data[5]),
        "volume": int(data[6]),
        "turnover": float(data[7]),
        "market_cap": float(data[9]),
    }

if __name__ == "__main__":
    stock_code = "sz300337"  # 示例股票代码
    print("Stock Data:", fetch_stock_data(stock_code))
    # print("Funds Flow:", fetch_funds_flow(stock_code))
    # print("Market Analysis:", fetch_market_analysis(stock_code))
    print("Stock Summary:", fetch_stock_summary(stock_code))
