import akshare as ak

df = ak.stock_zh_a_spot()
print("获取到的列名:", df.columns.tolist())
print("获取到的数据量:", len(df))
print("\n前5行数据预览:")
print(df.head())