import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_module_import():
    """测试所有模块是否能正常导入"""
    try:
        print("测试模块导入...")

        # 测试基础模块
        import pandas as pd
        print("✓ pandas 导入成功")

        # 测试akshare
        import akshare as ak
        print("✓ akshare 导入成功")

        # 测试自定义模块
        from data_fetcher import fetch_stock_data, save_data_to_csv, load_data_from_csv
        print("✓ data_fetcher 导入成功")

        from data_cleaner import clean_data
        print("✓ data_cleaner 导入成功")

        from data_analysis import calculate_all_metrics
        print("✓ data_analysis 导入成功")

        from technical_indicators import calculate_all_technical_indicators, validate_indicators
        print("✓ technical_indicators 导入成功")

        from visualizer import plot_price_and_ma, plot_macd, plot_rsi, plot_combined_chart
        print("✓ visualizer 导入成功")

        print("\n所有模块导入成功！")
        return True

    except ImportError as e:
        print(f"模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"运行时错误: {e}")
        return False

def test_akshare_basic():
    """测试akshare的基本功能"""
    try:
        import akshare as ak

        print("\n测试AKShare基本功能...")
        # 获取少量数据测试
        stock_data = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20230105")

        if stock_data is not None and not stock_data.empty:
            print("✓ AKShare数据获取成功")
            print("数据预览:")
            print(stock_data.head().to_string())
            return True
        else:
            print("✗ AKShare数据获取失败")
            return False

    except Exception as e:
        print(f"AKShare测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 模块测试 ===")

    # 测试模块导入
    if not test_module_import():
        print("\n请先解决模块导入问题，然后重试。")
        sys.exit(1)

    # 测试AKShare基本功能
    test_akshare_basic()

    print("\n测试完成！")