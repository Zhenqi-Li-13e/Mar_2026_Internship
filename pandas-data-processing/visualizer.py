import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import numpy as np

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def calculate_all_technical_indicators(data):
    """
    计算所有技术指标（从technical_indicators模块复制）
    """
    data = data.copy()

    # 计算MACD
    fast_ema = data['close'].ewm(span=12, adjust=False).mean()
    slow_ema = data['close'].ewm(span=26, adjust=False).mean()
    data['macd'] = fast_ema - slow_ema
    data['signal'] = data['macd'].ewm(span=9, adjust=False).mean()
    data['macd_histogram'] = data['macd'] - data['signal']

    # 计算RSI
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    rs = avg_gain / avg_loss
    data['rsi'] = 100 - (100 / (1 + rs))

    # 计算移动平均线
    data['ma_5'] = data['close'].rolling(window=5).mean()
    data['ma_20'] = data['close'].rolling(window=20).mean()

    return data

def plot_price_and_ma(data, symbol, save_path=None):
    """
    绘制价格和移动平均线图表

    参数:
        data: pandas DataFrame
        symbol: 股票代码
        save_path: 保存路径，如果为None则不保存
    """
    plt.figure(figsize=(12, 6))

    # 绘制收盘价
    plt.plot(data['date'], data['close'], label='收盘价', color='blue', linewidth=1.5)

    # 绘制移动平均线
    if 'ma_5' in data.columns:
        plt.plot(data['date'], data['ma_5'], label='MA5', color='red', linewidth=1)
    if 'ma_20' in data.columns:
        plt.plot(data['date'], data['ma_20'], label='MA20', color='green', linewidth=1)

    # 设置图表属性
    plt.title(f'{symbol} 股价与移动平均线')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存或显示图表
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存到 {save_path}")
    else:
        plt.show()

def plot_macd(data, symbol, save_path=None):
    """
    绘制MACD图表

    参数:
        data: pandas DataFrame
        symbol: 股票代码
        save_path: 保存路径，如果为None则不保存
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})

    # 绘制价格和MACD线
    ax1.plot(data['date'], data['close'], label='收盘价', color='blue', linewidth=1.5)
    ax1.plot(data['date'], data['macd'], label='MACD', color='red', linewidth=1)
    ax1.plot(data['date'], data['signal'], label='信号线', color='green', linewidth=1)
    ax1.set_title(f'{symbol} 股价与MACD')
    ax1.set_ylabel('价格')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    ax1.tick_params(axis='x', rotation=45)

    # 绘制MACD柱状图
    ax2.bar(data['date'], data['macd_histogram'], width=0.8, color=['green' if x >= 0 else 'red' for x in data['macd_histogram']])
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax2.set_ylabel('MACD柱状图')
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    # 保存或显示图表
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"MACD图表已保存到 {save_path}")
    else:
        plt.show()

def plot_rsi(data, symbol, save_path=None):
    """
    绘制RSI图表

    参数:
        data: pandas DataFrame
        symbol: 股票代码
        save_path: 保存路径，如果为None则不保存
    """
    plt.figure(figsize=(12, 6))

    # 绘制RSI
    plt.plot(data['date'], data['rsi'], label='RSI', color='purple', linewidth=1.5)

    # 绘制超买超卖线
    plt.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='超买线 (70)')
    plt.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='超卖线 (30)')
    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='中轴线 (50)')

    # 设置图表属性
    plt.title(f'{symbol} 相对强弱指数(RSI)')
    plt.xlabel('日期')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    plt.tight_layout()

    # 保存或显示图表
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"RSI图表已保存到 {save_path}")
    else:
        plt.show()

def plot_combined_chart(data, symbol, save_path=None):
    """
    绘制组合图表（价格、MACD、RSI）

    参数:
        data: pandas DataFrame
        symbol: 股票代码
        save_path: 保存路径，如果为None则不保存
    """
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1])

    # 价格和移动平均线
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(data['date'], data['close'], label='收盘价', color='blue', linewidth=1.5)
    if 'ma_5' in data.columns:
        ax1.plot(data['date'], data['ma_5'], label='MA5', color='red', linewidth=1)
    if 'ma_20' in data.columns:
        ax1.plot(data['date'], data['ma_20'], label='MA20', color='green', linewidth=1)
    ax1.set_title(f'{symbol} 股价与技术指标')
    ax1.set_ylabel('价格')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # MACD
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.plot(data['date'], data['macd'], label='MACD', color='red', linewidth=1)
    ax2.plot(data['date'], data['signal'], label='信号线', color='green', linewidth=1)
    ax2.bar(data['date'], data['macd_histogram'], width=0.8, color=['green' if x >= 0 else 'red' for x in data['macd_histogram']])
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    ax2.set_ylabel('MACD')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # RSI
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.plot(data['date'], data['rsi'], label='RSI', color='purple', linewidth=1.5)
    ax3.axhline(y=70, color='red', linestyle='--', alpha=0.7)
    ax3.axhline(y=30, color='green', linestyle='--', alpha=0.7)
    ax3.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    ax3.set_ylabel('RSI')
    ax3.set_xlabel('日期')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 100)

    # 设置日期格式
    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    # 保存或显示图表
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"组合图表已保存到 {save_path}")
    else:
        plt.show()

if __name__ == "__main__":
    # 示例数据
    dates = pd.date_range(start='2023-01-01', periods=100)
    prices = np.cumsum(np.random.normal(0, 1, 100)) + 100
    sample_data = pd.DataFrame({
        'date': dates,
        'close': prices
    })

    # 添加一些技术指标用于测试
    sample_data = calculate_all_technical_indicators(sample_data)

    # 绘制各种图表
    plot_price_and_ma(sample_data, '示例股票', 'price_ma_chart.png')
    plot_macd(sample_data, '示例股票', 'macd_chart.png')
    plot_rsi(sample_data, '示例股票', 'rsi_chart.png')
    plot_combined_chart(sample_data, '示例股票', 'combined_chart.png')