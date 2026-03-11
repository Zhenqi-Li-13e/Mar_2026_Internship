import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import pandas as pd
    import akshare as ak
    from data_fetcher import fetch_stock_data, save_data_to_csv, load_data_from_csv
    from data_cleaner import clean_data
    from data_analysis import calculate_all_metrics
    from technical_indicators import calculate_all_technical_indicators, validate_indicators
    from visualizer import plot_price_and_ma, plot_macd, plot_rsi, plot_combined_chart

    def main():
        """
        主函数：执行完整的Pandas数据处理流程
        """
        print("=== Pandas数据处理入门 - 股票数据分析 ===")

        # 配置参数
        symbol = "000001"  # 平安银行
        start_date = "20230101"
        end_date = "20231231"
        output_file = f"{symbol}_stock_data.csv"

        # 创建results目录（如果不存在）
        results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            print(f"已创建结果目录: {results_dir}")

        # 1. 获取数据
        print("\n1. 获取股票数据...")
        stock_data = fetch_stock_data(symbol, start_date, end_date)

        if stock_data is None:
            print("数据获取失败，请检查AKShare连接或股票代码")
            return

        # 保存原始数据
        save_data_to_csv(stock_data, output_file)

        # 2. 数据清洗
        print("\n2. 数据清洗...")
        cleaned_data, cleaning_record = clean_data(stock_data)

        print("\n清洗记录:")
        for key, value in cleaning_record.items():
            print(f"{key}:")
            print(value)
            print()

        # 3. 数据分析
        print("\n3. 数据分析...")
        analysis_data, analysis_results = calculate_all_metrics(cleaned_data)

        print("分析结果:")
        for key, value in analysis_results.items():
            print(f"{key}: {value:.4f}")

        # 4. 技术指标计算
        print("\n4. 计算技术指标...")
        technical_data = calculate_all_technical_indicators(analysis_data)

        # 验证技术指标
        validation = validate_indicators(technical_data)
        print("\n技术指标验证结果:")
        for key, value in validation.items():
            print(f"{key}: {'通过' if value else '失败'}")

        # 5. 数据可视化
        print("\n5. 生成图表...")
        plot_price_and_ma(technical_data, symbol, os.path.join(results_dir, 'price_ma_chart.png'))
        plot_macd(technical_data, symbol, os.path.join(results_dir, 'macd_chart.png'))
        plot_rsi(technical_data, symbol, os.path.join(results_dir, 'rsi_chart.png'))
        plot_combined_chart(technical_data, symbol, os.path.join(results_dir, 'combined_chart.png'))

        print("\n=== 任务完成 ===")
        print(f"处理后的数据已保存到 {output_file}")
        print("所有图表已生成")

        # 显示处理后的数据前几行
        print("\n处理后的数据预览:")
        print(technical_data.head().to_string())

except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保已安装所有必要的依赖:")
    print("pip install pandas akshare matplotlib")
    sys.exit(1)

if __name__ == "__main__":
    main()