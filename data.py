import akshare as ak
import pandas as pd

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# 沪A实时行情数据
df = ak.stock_sh_a_spot_em()

# 涨幅 3-5%
df2=df.loc[(df['涨跌幅'] >= 3) & (df['涨跌幅'] <= 5)]
print(df2)

# 量比大于1
df3=df2.loc[(df['量比'] > 1)]
print(df3)