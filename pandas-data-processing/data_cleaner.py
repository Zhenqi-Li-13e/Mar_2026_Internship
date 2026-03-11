import pandas as pd
import numpy as np

def check_missing_values(data):
    """
    检查数据中的缺失值

    参数:
        data: pandas DataFrame

    返回:
        缺失值统计信息
    """
    missing_info = data.isnull().sum()
    missing_percent = (missing_info / len(data)) * 100
    return pd.DataFrame({
        '缺失值数量': missing_info,
        '缺失值百分比': missing_percent
    })

def handle_missing_values(data, method='ffill'):
    """
    处理缺失值

    参数:
        data: pandas DataFrame
        method: 填充方法，ffill(前向填充)/bfill(后向填充)/interpolate(插值)

    返回:
        处理后的DataFrame
    """
    if method == 'ffill':
        return data.fillna(method='ffill')
    elif method == 'bfill':
        return data.fillna(method='bfill')
    elif method == 'interpolate':
        return data.interpolate()
    else:
        return data.fillna(method='ffill')

def detect_outliers(data, column, method='iqr', threshold=1.5):
    """
    检测异常值

    参数:
        data: pandas DataFrame
        column: 要检测的列名
        method: 检测方法，iqr/zscore
        threshold: 阈值

    返回:
        异常值索引和统计信息
    """
    if method == 'iqr':
        # IQR方法
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        return outliers, {
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            '下限': lower_bound,
            '上限': upper_bound,
            '异常值数量': len(outliers)
        }
    elif method == 'zscore':
        # Z-score方法
        z_scores = np.abs((data[column] - data[column].mean()) / data[column].std())
        outliers = data[z_scores > threshold]
        return outliers, {
            '均值': data[column].mean(),
            '标准差': data[column].std(),
            '阈值': threshold,
            '异常值数量': len(outliers)
        }
    else:
        return pd.DataFrame(), {}

def handle_outliers(data, column, method='clip', threshold=1.5):
    """
    处理异常值

    参数:
        data: pandas DataFrame
        column: 要处理的列名
        method: 处理方法，clip(截断)/remove(删除)/replace(替换为均值)
        threshold: 阈值

    返回:
        处理后的DataFrame
    """
    if method == 'clip':
        # IQR方法检测异常值
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        data[column] = data[column].clip(lower_bound, upper_bound)
        return data
    elif method == 'remove':
        # IQR方法检测异常值
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    elif method == 'replace':
        # IQR方法检测异常值
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        # 替换异常值为边界值
        data.loc[data[column] < lower_bound, column] = lower_bound
        data.loc[data[column] > upper_bound, column] = upper_bound
        return data
    else:
        return data

def clean_data(data):
    """
    完整的数据清洗流程

    参数:
        data: pandas DataFrame

    返回:
        清洗后的DataFrame和清洗记录
    """
    cleaning_record = {}

    # 检查并处理缺失值
    missing_info = check_missing_values(data)
    cleaning_record['缺失值检查'] = missing_info.to_dict()

    # 处理缺失值（前向填充）
    data_cleaned = handle_missing_values(data)
    cleaning_record['缺失值处理'] = '前向填充'

    # 检测异常值（以收盘价为例）
    outliers, outlier_info = detect_outliers(data_cleaned, 'close', method='iqr', threshold=1.5)
    cleaning_record['异常值检测'] = outlier_info

    # 处理异常值（截断方法）
    data_cleaned = handle_outliers(data_cleaned, 'close', method='clip', threshold=1.5)
    cleaning_record['异常值处理'] = '截断方法'

    return data_cleaned, cleaning_record

if __name__ == "__main__":
    # 示例数据
    sample_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=30),
        'open': np.random.normal(10, 1, 30),
        'close': np.random.normal(10, 1, 30),
        'high': np.random.normal(10, 1, 30),
        'low': np.random.normal(10, 1, 30),
        'volume': np.random.normal(1000000, 200000, 30)
    })

    # 添加一些缺失值和异常值用于测试
    sample_data.loc[5, 'close'] = np.nan
    sample_data.loc[10, 'volume'] = np.nan
    sample_data.loc[15, 'close'] = 20  # 异常值

    # 清洗数据
    cleaned_data, record = clean_data(sample_data)

    print("清洗记录:")
    for key, value in record.items():
        print(f"{key}:")
        print(value)
        print()

    print("\n清洗后的数据:")
    print(cleaned_data.head())