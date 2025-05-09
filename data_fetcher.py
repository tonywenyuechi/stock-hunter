import akshare as ak
from datetime import datetime, timedelta
import pandas as pd
import time

class StockDataFetcher:
    """
    股票数据获取器，封装AKShare接口调用
    功能：
    1. 获取实时行情数据
    2. 获取历史K线数据
    3. 数据缓存和节流控制
    """
    
    def __init__(self):
        self.cache = {}  # 数据缓存
        self.last_fetch_time = datetime.now()
    
    @staticmethod 
    def get_all_stocks(self):
        """获取全市场股票列表"""
        try:
            df = ak.stock_zh_a_spot()
            print("实际获取到的列名:", df.columns.tolist())  # 调试信息
            return df
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            return pd.DataFrame()
    
    def get_history_data(self, stock_code, start_date, end_date):
        """
        获取个股历史行情数据(带缓存和节流控制)
        参数:
            stock_code: 股票代码(如: '600519')
            start_date: 开始日期(格式: 'YYYYMMDD')
            end_date: 结束日期(格式: 'YYYYMMDD')
        返回:
            DataFrame: 包含日期、开盘价、最高价、最低价、收盘价、成交量等
        """
        cache_key = f"{stock_code}_{start_date}_{end_date}"
        
        # 检查缓存
        if cache_key in self.cache:
            return self.cache[cache_key]
            
        # API节流控制(防止请求过快)
        elapsed = (datetime.now() - self.last_fetch_time).seconds
        if elapsed < 1:  # 每秒最多1次请求
            time.sleep(1 - elapsed)
        
        try:
            data = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust="hfq"  # 前复权
            )
            self.cache[cache_key] = data  # 写入缓存
            self.last_fetch_time = datetime.now()
            return data
        except Exception as e:
            print(f"获取{stock_code}历史数据失败: {e}")
            return pd.DataFrame()
    
    def get_realtime_quote(self, stock_code):
        """
        获取个股实时行情
        参数:
            stock_code: 股票代码
        返回:
            dict: 包含最新价、涨跌幅、成交量等实时数据
        """
        try:
            df = ak.stock_zh_a_spot()
            return df[df['代码'] == stock_code].iloc[0].to_dict()
        except Exception as e:
            print(f"获取{stock_code}实时行情失败: {e}")
            return {}