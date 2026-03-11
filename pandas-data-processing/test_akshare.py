import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import akshare as ak
    print("akshare导入成功！")

    # 测试AKShare的基本功能
    print("测试获取股票数据...")
    stock_data = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20230105")
    print("数据获取成功！")
    print(stock_data.head().to_string())

except ImportError as e:
    print(f"导入失败: {e}")
    print("请确保已安装akshare:")
    print("pip install akshare --upgrade")

except Exception as e:
    print(f"运行时错误: {e}")