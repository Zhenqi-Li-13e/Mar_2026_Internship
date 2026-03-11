import akshare as ak
import pandas as pd
import os
import numpy as np


def fetch_stock_data(symbol, start_date, end_date, period="daily"):
    """
    从AKShare获取股票历史数据

    参数:
        symbol: 股票代码，如"000002"
        start_date: 开始日期，格式如"20230101"
        end_date: 结束日期，格式如"20231231"
        period: 数据周期，daily/weekly/monthly

    返回:
        pandas DataFrame包含股票数据
    """
    try:
        # 获取A股历史数据
        stock_data = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
            adjust="",  # 不调整价格
        )

        # 重命名列以符合标准
        stock_data = stock_data.rename(
            columns={
                "日期": "date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume",
                "成交额": "amount",
            }
        )

        # 确保日期格式正确
        stock_data["date"] = pd.to_datetime(stock_data["date"])

        return stock_data

    except Exception as e:
        print(f"获取数据时出错: {e}")
        return None


def save_data_to_csv(data, filename):
    """
    将数据保存为CSV文件

    参数:
        data: pandas DataFrame
        filename: 文件名
    """
    if data is not None:
        # 保存到当前目录（pandas-data-processing文件夹）
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        data.to_csv(save_path, index=False)
        print(f"数据已保存到 {save_path}")
    else:
        print("没有数据可保存")


def load_data_from_csv(filename):
    """
    从CSV文件加载数据

    参数:
        filename: 文件名

    返回:
        pandas DataFrame
    """
    # 从当前目录（pandas-data-processing文件夹）加载
    load_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if os.path.exists(load_path):
        return pd.read_csv(load_path)
    else:
        print(f"文件 {load_path} 不存在")
        return None


if __name__ == "__main__":
    # 示例：获取平安银行(000001)的日度数据
    symbol = "000001"
    start_date = "20230101"
    end_date = "20231231"

    # 获取数据
    stock_data = fetch_stock_data(symbol, start_date, end_date)

    if stock_data is not None:
        # 保存数据
        save_data_to_csv(stock_data, f"{symbol}_stock_data.csv")

        # 加载数据验证
        loaded_data = load_data_from_csv(f"{symbol}_stock_data.csv")
        if loaded_data is not None:
            print(loaded_data.head().to_string())
        else:
            print("无法加载数据进行验证")
