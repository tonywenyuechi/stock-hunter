from data_fetcher import StockDataFetcher
import pandas as pd

class StockAnalyzerGUI:
    def __init__(self):
        self.fetcher = StockDataFetcher()
        
    def analyze(self, market_cap, holder_type):
        """执行分析并返回结果"""
        try:
            # 获取全市场股票
            all_stocks = self.fetcher.get_all_stocks()
            
            # 检查并映射列名
            column_mapping = {
                '总市值': '总市值',  # 可能需要改为实际列名如'market_cap'
                '机构持股比例': 'hold_ratio',
                '主力净流入': 'main_net_inflow'
            }
            all_stocks = all_stocks.rename(columns={v:k for k,v in column_mapping.items() if v in all_stocks.columns})
            
            # 市值筛选
            if "小市值" in market_cap:
                filtered = all_stocks[all_stocks['总市值'] < 50]
            elif "中市值" in market_cap:
                filtered = all_stocks[(all_stocks['总市值'] >= 50) & (all_stocks['总市值'] <= 200)]
            else:
                filtered = all_stocks[all_stocks['总市值'] > 200]
            
            # 股东结构筛选（简化示例）
            if "机构" in holder_type:
                filtered = filtered[filtered['机构持股比例'] > 0.3]
            # 其他条件...
            
            # 筹码峰分析
            filtered = self.analyze_chip_distribution(filtered)
            
            # 主力资金分析
            filtered = self.analyze_main_fund(filtered)
            
            # 保存结果
            self.save_results(filtered)
            
            return filtered[['代码', '名称', '总市值', '主力净流入']].to_string(index=False)
            
        except Exception as e:
            return f"分析出错: {str(e)}"
    
    def analyze_chip_distribution(self, df):
        """筹码峰分析"""
        # 实现筹码峰分析逻辑
        return df
    
    def analyze_main_fund(self, df):
        """主力资金分析"""
        # 实现主力资金分析逻辑
        return df
    
    def save_results(self, df):
        """保存结果到文件"""
        with open("c:/Users/Administrator/stock-hunter/results.txt", "w") as f:
            f.write(df.to_string())