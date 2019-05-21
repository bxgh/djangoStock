import tushare as ts


ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
pro = ts.pro_api()
# df = ts.get_realtime_quotes('000581')
df = pro.pro_bar(ts_code='000001.SZ', adj='qfq',freq='1min', start_date='20180101', end_date='20181011')
print(df)