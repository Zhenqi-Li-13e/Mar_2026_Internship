import pandas as pd
import numpy as np

def calculate_daily_returns(data, column='close'):
    """
    计算日收益率

    参数:
        data: pandas DataFrame
        column: 价格列名

    返回:
        包含日收益率的DataFrame
    """
    data = data.copy()
    data['daily_return'] = data[column].pct_change()
    return data

def calculate_cumulative_returns(data, column='close'):
    """
    计算累计收益率

    参数:
        data: pandas DataFrame
        column: 价格列名

    返回:
        包含累计收益率的DataFrame
    """
    data = data.copy()
    data['cumulative_return'] = (1 + data['daily_return']).cumprod() - 1
    return data

def calculate_moving_average(data, window, column='close'):
    """
    计算移动平均线

    参数:
        data: pandas DataFrame
        window: 移动窗口大小
        column: 价格列名

    返回:
        包含移动平均线的DataFrame
    """
    data = data.copy()
    data[f'ma_{window}'] = data[column].rolling(window=window).mean()
    return data

def calculate_exponential_moving_average(data, span, column='close'):
    """
    计算指数移动平均线

    参数:
        data: pandas DataFrame
        span: 指数平滑窗口
        column: 价格列名

    返回:
        包含指数移动平均线的DataFrame
    """
    data = data.copy()
    data[f'ema_{span}'] = data[column].ewm(span=span, adjust=False).mean()
    return data

def calculate_all_metrics(data):
    """
    计算所有分析指标

    参数:
        data: pandas DataFrame

    返回:
        包含所有指标的DataFrame和分析结果
    """
    data = data.copy()

    # 计算日收益率
    data = calculate_daily_returns(data)

    # 计算累计收益率
    data = calculate_cumulative_returns(data)

    # 计算移动平均线
    data = calculate_moving_average(data, 5)  # MA5
    data = calculate_moving_average(data, 20)  # MA20
    data = calculate_exponential_moving_average(data, 12)  # EMA12
    data = calculate_exponential_moving_average(data, 26)  # EMA26

    # 计算分析结果
    analysis_results = {
        '总收益率': data['cumulative_return'].iloc[-1],
        '平均日收益率': data['daily_return'].mean(),
        '收益率标准差': data['daily_return'].std(),
        '最大日收益率': data['daily_return'].max(),
        '最小日收益率': data['daily_return'].min(),
        '正收益天数': (data['daily_return'] > 0).sum(),
        '负收益天数': (data['daily_return'] < 0).sum()
    }

    return data, analysis_results

if __name__ == "__main__":
    # 示例数据
    dates = pd.date_range(start='2023-01-01', periods=100)
    prices = np.cumsum(np.random.normal(0, 1, 100)) + 100
    sample_data = pd.DataFrame({
        'date': dates,
        'close': prices
    })

    # 计算所有指标
    result_data, results = calculate_all_metrics(sample_data)

    print("分析结果:")
    for key, value in results.items():
        print(f"{key}: {value:.4f}")

    print("\n计算后的数据:")
    print(result_data.tail())