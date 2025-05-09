import pandas as pd
import akshare as ak
from datetime import datetime, time
import schedule
import time
from data_fetcher import StockDataFetcher
from pattern_analyzer import MonsterStockAnalyzer

class StockAnalyzer:
    def __init__(self):
        self.hot_industries = []
        self.candidate_stocks = []
        self.pattern_analyzer = MonsterStockAnalyzer()
    
    def find_monster_stocks(self):
        """寻找潜在妖股"""
        all_stocks = StockDataFetcher.get_all_stocks()
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        monster_stocks = []
        for code in all_stocks['代码'].head(100):  # 示例只检查前100只
            try:
                hist_data = StockDataFetcher.get_history_data(code, start_date, end_date)
                if self.pattern_analyzer.analyze_stock(hist_data):
                    monster_stocks.append(code)
            except Exception as e:
                print(f"分析{code}时出错: {e}")
        return monster_stocks
    
    def get_market_data(self):
        """获取最新市场数据"""
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        print("实际获取到的列名:", stock_zh_a_spot_df.columns.tolist())  # 调试信息
        return stock_zh_a_spot_df

    def analyze_stocks(self):
        """按条件分析股票"""
        try:
            df = self.get_market_data()
            print(f"获取到{len(df)}条股票数据")
            
            # 映射列名（根据AKShare实际返回的列名修改）
            column_mapping = {
                '5min_change': '涨速',  # 可能需要改为'涨速'或其他AKShare返回的列名
                '10day_change': '10日涨幅', 
                'main_net_inflow': '主力净流入',
                'industry': '所属行业',
                'turnover_rate': '换手率',
                '代码': '代码',
                '名称': '名称'
            }
            
            # 重命名列
            df = df.rename(columns={v:k for k,v in column_mapping.items() if v in df.columns})
            
            # 检查数据列是否存在
            required_columns = ['5min_change', '10day_change', 'main_net_inflow', 'industry', 'turnover_rate']
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                print(f"缺少必要列: {missing_cols}")
                return

            # 5分钟涨速>7%
            df = df[df['5min_change'] > 7]
            print(f"5分钟涨速>7%后剩余{len(df)}只股票")
            
            # 十日内涨幅<20%
            df = df[df['10day_change'] < 20]
            print(f"十日内涨幅<20%后剩余{len(df)}只股票")
            
            # 当日大资金净流入
            df = df[df['main_net_inflow'] > 0]
            print(f"大资金净流入后剩余{len(df)}只股票")
            
            # 筛选热门板块股票
            if not self.hot_industries:
                print("无热门板块数据")
                return
                
            df = df[df['industry'].isin(self.hot_industries)]
            print(f"热门板块筛选后剩余{len(df)}只股票")
            
            # 筹码峰阻力小 (换手率高)
            df = df[df['turnover_rate'] > 5]
            print(f"换手率>5%后剩余{len(df)}只股票")
            
            if len(df) == 0:
                print("没有股票满足所有条件")
                return
                
            # 按综合评分排序
            df['score'] = df['5min_change'] * 0.3 + df['main_net_inflow'] * 0.4 + df['turnover_rate'] * 0.3
            self.candidate_stocks = df.sort_values('score', ascending=False).head(3)
            
        except Exception as e:
            print(f"分析股票时出错: {str(e)}")
    
    def get_hot_industries(self):
        """获取当日热门板块"""
        industry_df = ak.stock_board_industry_spot_em()
        self.hot_industries = industry_df.nlargest(5, '涨跌幅')['板块名称'].tolist()
    
    def run_daily(self):
        """每日定时执行"""
        try:
            print("开始获取热门板块...")
            self.get_hot_industries()
            print("开始分析股票...")
            self.analyze_stocks()
            self.send_results()
        except Exception as e:
            print(f"分析过程中出错: {str(e)}")
    
    def send_results(self):
        """发送分析结果到控制台和文件"""
        result_file = "stock_recommendations.txt"
        
        if self.candidate_stocks is None or len(self.candidate_stocks) == 0:
            output = "今日无符合条件股票推荐"
        else:
            output = "今日推荐股票:\n"
            output += self.candidate_stocks[['代码', '名称', 'score']].to_string(index=False)
        
        # 打印到控制台
        print(output)
        
        # 写入文件
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(output + "\n")
            f.write("生成时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        print(f"\n结果已保存到: {result_file}")