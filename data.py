import akshare as ak
import pandas as pd

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)

# 沪A实时行情数据
df_all = ak.stock_sh_a_spot_em()

# 涨幅 3-5%
df_zf = df_all.loc[(df_all['涨跌幅'] >= 3) & (df_all['涨跌幅'] <= 5)]

# 量比大于1
df_lb = df_zf.loc[(df_zf['量比'] > 1)]

# 换手率 5-10%
df_hsl = df_lb.loc[(df_lb['换手率'] >= 5) & (df_lb['换手率'] <= 10)]

# 流通市值 50-200亿
df_ltsz = df_hsl.loc[(df_hsl['流通市值'] >= 50e+08) & (df_hsl['流通市值'] <= 200e+08)]
print(df_ltsz)