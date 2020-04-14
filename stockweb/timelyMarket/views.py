from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from datetime import datetime as dt
import time 
import re
import pandas as pd
import easyquotation
import numpy as np
import tushare as ts
from dwebsocket.decorators import accept_websocket,require_websocket
import pymysql
from sqlalchemy import create_engine


@accept_websocket
def test_websocket(request):
     if request.is_websocket():
        zdycode= request.websocket.wait().decode()          
        # print(zdycode)         
        # tscode=['sh000001' ,'sz399001','sz399006',zdycode]
        quotationQq = easyquotation.use('sina')
        result=quotationQq.stocks(zdycode, prefix=True)
        # print(result)
        data=result['sz300654']
        # print(data)
        while 1:
        # time.sleep(1) ## 向前端发送时间
        # data=stockMarket('sz300654')
        # print(data)
         if  request.websocket.count_messages()>0:
          zdycode= request.websocket.read ().decode() 
          print(zdycode)
          request.websocket.send(zdycode)
         else:
            pass   
          
        # request.websocket.send(json.dumps(data))

@accept_websocket
def stockmline_ws(request):            #websocket 传送实时行情数据
#    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5') #设置tushare.token    
#    pro = ts.pro_api() 
#    #沪深A股股票代码转list供easyquotation调用
#    tscodeData = pro.query('stock_basic', exchange='', list_status='L', fields='symbol')
#    stockList  = tscodeData['symbol'].tolist()       
   quotation = easyquotation.use("timekline")   #声明quotation 
   quotationQq = easyquotation.use('qq')    
   tscode= request.websocket.wait().decode()   #分时个股代码
   if request.is_websocket():
     while True :        
       try: 
        tradeTime={'tradeTime':dt.now().strftime('%H:%M:%S') }   
        marketTime=dt.now().strftime('%H%M%S')    
        tradeDate= dt.now().strftime('%Y%m%d') 
        time.sleep(2)    
        if  request.websocket.count_messages()>0:    #接收分时个股代码
          tscode= request.websocket.read ().decode()         
        # print(tscode)
        shtscode='sh000001'
        tsdm=tscode+'.js'
        shdm='sh000001.js'        
        df = quotation.real([tscode,'sh000001'], prefix=True) 
        stockData =df[tsdm]       
        stockData["data"] = stockData.pop("time_data")
        stockData['yestclose']=getyestClose(quotationQq,tscode)  #分时图获取昨日收盘价
        zhishuData=df[shdm] 
        zhishuData["data"] = zhishuData.pop("time_data")
        zhishuData['yestclose']=getyestClose(quotationQq,shtscode)  #上证指数分时图获取昨日收盘价
        MarketData=stockMarket(quotationQq,tscode)  #获取个股实时行情数据
        upRatio= watchMarket(tradeDate)  #获取看盘数据
        


        # print(upRatio)
        data=dict()                                  #打包所有即时数据，生成字典类型
        data['stockMline']=stockData                 #分时个股分时数据 
        data['shzsMline']=zhishuData                 #上证指数分时数据
        data['tradeTime']=tradeTime                  #当前时间
        data['MarketData']=MarketData                #个股实时行情数据
        data['watchMarket']={'upRatio':upRatio}           #看盘数据：上涨个股比例
        # print(data)
        request.websocket.send(json.dumps(data))
       except:
        pass       
#     return JsonResponse(data, safe=False)    
    

def getyestClose(quotationQq,tsCode):
    result=quotationQq.stocks(tsCode, prefix=True) 
    yestclose=result[tsCode]['close'] 
    return yestclose

def index(request):
    tscode='sz300654' 
    quotationQq = easyquotation.use('qq')
    result=quotationQq.stocks([tscode,'sh000001'], prefix=True) 
    data=result[tscode]
    data['pct_chg']=data['涨跌(%)']
    data['amount']=data['成交额(万)']/10000  
    global yestclose,shzsyestclose
    yestclose=data['close']  
    # user_dict1 = model_to_dict(data)
    return render(request,'timelyMarket/index1.html',data)

def stockMarket(quotationQq,zdycode):   #实时个股行情(含指数行情)  zdycode:股票代码    
    tscode=['sh000001' ,'sz399001','sz399006',zdycode] 
    result=quotationQq.stocks(tscode, prefix=True)
    data=result[zdycode]
    data['pct_chg']=data['涨跌(%)']
    data['amount']=data['成交额(万)']/10000
    #处理逐笔数据
    pattern = r'[\|]'                      # 定义分隔符      
    url = data['最近逐笔成交'] # 需要拆分的字符串
    zhubis = re.split(pattern, url) # 以pattern的值 分割字符串
    pattern = r'[\/]' 
    details=re.split(pattern, zhubis[0])
    data['zbtime1']=details[0]
    data['zbprice1']=details[1]
    data['zbvol1']=details[2]
    data['zbbs1']=details[3]
    data['zbamount1']=details[4]
    details=re.split(pattern, zhubis[1])
    data['zbtime2']=details[0]
    data['zbprice2']=details[1]
    data['zbvol2']=details[2]
    data['zbbs2']=details[3]
    data['zbamount2']=details[4]
    details=re.split(pattern, zhubis[2])
    data['zbtime3']=details[0]
    data['zbprice3']=details[1]
    data['zbvol3']=details[2]
    data['zbbs3']=details[3]
    data['zbamount3']=details[4]
    details=re.split(pattern, zhubis[3])
    data['zbtime4']=details[0]
    data['zbprice4']=details[1]
    data['zbvol4']=details[2]
    data['zbbs4']=details[3]
    data['zbamount4']=details[4]
    details=re.split(pattern, zhubis[4])
    data['zbtime5']=details[0]
    data['zbprice5']=details[1]
    data['zbvol5']=details[2]
    data['zbbs5']=details[3]
    data['zbamount5']=details[4] 
    shzs= result['sh000001']
    szzs= result['sz399001']
    cyzs= result['sz399006']
    data['shzs']=shzs['now']
    data['shzsClose']=shzs['close']
    data['shzsZf']=shzs['涨跌']
    data['shzsAmount']=shzs['成交额(万)']/100000000
    data['szzs']=szzs['now']
    data['szzsClose']=szzs['close']
    data['szzsZf']=szzs['涨跌']
    data['szzsAmount']=szzs['成交额(万)']/100000000
    data['cyzs']=cyzs['now']
    data['cyzsClose']=cyzs['close']
    data['cyzsZf']=cyzs['涨跌']
    data['cyzsAmount']=cyzs['成交额(万)']/100000000 
    data['datetime']=data['datetime'].strftime('%Y-%m-%d %H:%M:%S')

    return data

def watchMarket(tradeDate):
    engine=create_engine("mysql+pymysql://toshare1:toshare1@192.168.151.216:3306/statistics?charset=utf8",echo=True)    
    readSql = "SELECT  trade_time, ups/(ups+draws+downs)*100 as upRatio from watch_market where trade_time>'"+tradeDate+"' order by trade_time "
    data = pd.read_sql_query(readSql,con = engine)
    data['trade_time']=data['trade_time'].dt.strftime('%H%M') 
    data=data.drop_duplicates(subset=['trade_time'],keep='last')
    upRatio=data.to_dict(orient= 'split' )    
    return upRatio['data']



def klineData(request):  #k线图数据从本地文件读取
    h5 = pd.HDFStore('D:/h5qfqdata/kday_SZ300654','r')
    # h5 = pd.HDFStore('/home/ontimeKdayData/h5qfqdata/kday_SZ300654','r')
    df=h5['data']
    df=df.sort_values('trade_date', ascending=True)  
    df=df.tail(250)
    order = ['trade_date',  'open', 'close', 'low', 'high', 'amount']    
    df = df[order]
    df['trade_date']=df.apply(lambda x : x['trade_date'][0:4]+'-'+x['trade_date'][4:6]+'-'+x['trade_date'][6:8],axis=1)
    train_data = np.array(df)
    data=train_data.tolist()    
    h5.close()
    # data=df.to_dict(orient='records')
    # result=json.dumps(data)
    return JsonResponse(data, safe=False)
    # return HttpResponse(data)

def mlineData(request):  #个股实时走势图从easyquotation实时获取
    tscode='300654' 
    tsdm='sz'+tscode+'.js'
    quotation = easyquotation.use("timekline")
    df = quotation.real([tscode], prefix=True) 
    data =df[tsdm]       
    data["data"] = data.pop("time_data")
#     data['yestclose']=yestclose 
    return JsonResponse(data, safe=False)

def stockStaticData(request): #个股静态数据，比如股本、利润、板块。。。
    # tsCode='300654.SZ'
    tsCode=request.GET['tsCode']    
    tradeDate='20190531'
    endDate='20181231'
    ts.set_token('38bb3cd1b6af2d75a7d7e506db8fd60354168642b400fa2104af81c5')
    pro = ts.pro_api()
    data=pro.daily_basic(ts_code=tsCode, trade_date=tradeDate, fields='ts_code,total_share,float_share,free_share') #ts每日指标,总股本，流通股本
    data=data.set_index(['ts_code'])
    df = pro.fina_indicator(ts_code=tsCode)   #ts财务指标数据，每股盈利
    df=df[df['end_date']==endDate]    
    df=df.set_index(['ts_code'])
    data['eps']=df['eps']
    data=data.to_json(orient='records')       #dataframe 转json [{}]
    return JsonResponse(data,safe=False)

# quotationQq = easyquotation.use('qq')
# data=quotationQq.stocks('300654')
# print(data)
# # data=data['300654']

# # user_dict1 = model_to_dict(data)
# print(data['300654'])
# h5 = pd.HDFStore('D:\\h5qfqdata\\kday_SH603039','r')
# df = h5['data']
# print(df)

# h5 = pd.HDFStore('D:/h5qfqdata/kday_SH601038','r')
# df=h5['data']
# df=df.head(100)
# order = ['trade_date',  'open', 'close', 'low', 'high', 'amount']    
# df = df[order]
# df['trade_date']=df.apply(lambda x : x['trade_date'][0:4]+'-'+x['trade_date'][4:6]+'-'+x['trade_date'][6:8],axis=1)
# train_data = np.array(df)
# data=train_data.tolist()    
# h5.close()
# print(data)

# tscode='603039' 
# tsdm='sh'+tscode+'.js'
# quotation = easyquotation.use("timekline")
# df = quotation.real([tscode], prefix=True) 
# data =df[tsdm]       
# data["mdata"] = data.pop("time_data")
# data['yestclose']=65.4 
# print(data)
# print(JsonResponse(data, safe=False))