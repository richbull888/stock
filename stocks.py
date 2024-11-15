import akshare as ak
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import mplfinance.original_flavor as mpf

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

# 按成交量排序
df_final = df_ltsz.sort_values(by='成交量', ascending=False)
print(df_final)

# K line
def kLine(code, securityName):
    now = datetime.datetime.now()
    yyyymmdd = '%04d%02d%02d'%(now.year,now.month,now.day)
    last_month = datetime.datetime.today()-datetime.timedelta(days=30)
    l_yyyymmdd = '%04d%02d%02d'%(last_month.year,last_month.month,last_month.day)

    df = ak.stock_zh_a_hist(symbol=code, start_date=f'{l_yyyymmdd}', end_date=f'{yyyymmdd}', adjust="qfq")

    df2 = df.reset_index().iloc[-30:, :7]  # 取过去30天数据
    df2 = df2.dropna(how='any').reset_index(drop=True)  # 去除空值且从零开始编号索引
    df2 = df2.sort_values(by='日期', ascending=True)

    # 均线数据
    df2['5'] = df2["收盘"].rolling(5).mean()
    df2['10'] = df2["收盘"].rolling(10).mean()
    df2['20'] = df2["收盘"].rolling(20).mean()

    plt.style.use("ggplot")
    fig, ax = plt.subplots(1, 1, figsize=(8, 3), dpi=200)
    # 绘制 K线
    mpf.candlestick2_ohlc(ax,
                      opens=df2['开盘'].values,
                      highs=df2['最高'].values,
                      lows=df2['最低'].values,
                      closes=df2['收盘'].values,
                      width=0.75, colorup="r", colordown="g")

    # 显示最高点和最低点
    ax.text(df2["最高"].idxmax(), df2["最高"].max(), s=df2["最高"].max(), fontsize=8)
    ax.text(df2["最高"].idxmin(), df2["最高"].min() - 2, s=df2["最高"].min(), fontsize=8)
    # 显示中文
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    ax.set_facecolor("white")
    ax.set_title(securityName)

    # 画均线
    plt.plot(df2['5'].values, alpha=0.5, label='MA5')
    plt.plot(df2['10'].values, alpha=0.5, label='MA10')
    plt.plot(df2['20'].values, alpha=0.5, label='MA20')

    ax.legend(facecolor='white', edgecolor='white', fontsize=6)
    # date 为 object 数据类型，通过 pd.to_datetime将该列数据转换为时间类型，即datetime
    df2["日期"] = pd.to_datetime(df2["日期"], format='%Y-%m-%d')
    # 修改x轴坐标
    plt.xticks(ticks=np.arange(0, len(df2)), labels=df2["日期"].dt.strftime('%Y-%m-%d').to_numpy())
    plt.xticks(rotation=90, size=8)
    # 修改y轴坐标
    ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.2f'))
    # x轴坐标显示不全，整理
    plt.subplots_adjust(bottom=0.25)
    plt.show()

print("Today's number of stocks:", len(df_final))
for ind in df_final.index:
    kLine(df_final['代码'][ind], df_final['名称'][ind])