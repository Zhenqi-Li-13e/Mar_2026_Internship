import pandas as pd
import numpy as np

def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9, column='close'):
    """
    计算MACD指标

    参数:
        data: pandas DataFrame
        fast_period: 快速EMA周期
        slow_period: 慢速EMA周期
        signal_period: 信号线周期
        column: 价格列名

    返回:
        包含MACD指标的DataFrame
    """
    data = data.copy()

    # 计算快速EMA和慢速EMA
    fast_ema = data[column].ewm(span=fast_period, adjust=False).mean()
    slow_ema = data[column].ewm(span=slow_period, adjust=False).mean()

    # 计算MACD线
    data['macd'] = fast_ema - slow_ema

    # 计算信号线
    data['signal'] = data['macd'].ewm(span=signal_period, adjust=False).mean()

    # 计算MACD柱状图
    data['macd_histogram'] = data['macd'] - data['signal']

    return data

def calculate_rsi(data, period=14, column='close'):
    """
    计算RSI指标

    参数:
        data: pandas DataFrame
        period: RSI周期
        column: 价格列名

    返回:
        包含RSI指标的DataFrame
    """
    data = data.copy()

    # 计算价格变化
    delta = data[column].diff()

    # 计算上涨和下跌的绝对值
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # 计算平均收益和平均损失
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # 计算相对强度，处理除零情况
    rs = avg_gain / avg_loss
    rs = rs.replace([np.inf, -np.inf], np.nan)  # 处理无穷大

    # 计算RSI，处理NaN情况
    data['rsi'] = 100 - (100 / (1 + rs))
    data['rsi'] = data['rsi'].fillna(50)  # NaN时设为中性值50

    return data

def calculate_all_technical_indicators(data):
    """
    计算所有技术指标

    参数:
        data: pandas DataFrame

    返回:
        包含所有技术指标的DataFrame
    """
    data = data.copy()

    # 计算MACD
    data = calculate_macd(data)

    # 计算RSI
    data = calculate_rsi(data)

    return data

def validate_indicators(data, column='close'):
    """
    验证技术指标计算结果

    参数:
        data: pandas DataFrame
        column: 价格列名

    返回:
        验证结果
    """
    validation_results = {}

    # 检查MACD指标
    if 'macd' in data.columns and 'signal' in data.columns:
        macd_diff = data['macd'] - data['signal']
        histogram_diff = data['macd_histogram']
        macd_validation = np.allclose(macd_diff, histogram_diff, atol=1e-10)
        validation_results['MACD验证'] = macd_validation

    # 检查RSI范围
    if 'rsi' in data.columns:
        rsi_range = data['rsi'].between(0, 100).all()
        validation_results['RSI范围验证'] = rsi_range

    return validation_results

if __name__ == "__main__":
    # 示例数据
    dates = pd.date_range(start='2023-01-01', periods=50)
    prices = np.cumsum(np.random.normal(0, 1, 50)) + 100
    sample_data = pd.DataFrame({
        'date': dates,
        'close': prices
    })

    # 计算技术指标
    result_data = calculate_all_technical_indicators(sample_data)

    print("技术指标计算结果:")
    print(result_data.tail())

    # 验证指标
    validation = validate_indicators(result_data)
    print("\n指标验证结果:")
    for key, value in validation.items():
        print(f"{key}: {'通过' if value else '失败'}")