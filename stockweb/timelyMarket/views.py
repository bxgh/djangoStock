from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
import re
import pandas as pd
import easyquotation
import numpy as np
# Create your views here.

yestclose=0 
def index(request):
    tscode='300654' 
    quotationQq = easyquotation.use('qq')
    result=quotationQq.stocks(tscode)
    data=result[tscode]
    data['pct_chg']=data['涨跌(%)']
    data['amount']=data['成交额(万)']/10000  
    global yestclose
    yestclose=data['close']  
    # user_dict1 = model_to_dict(data)
    return render(request,'timelyMarket/index1.html',data)

def ajax_dict(request):
    quotationQq = easyquotation.use('qq')
    result=quotationQq.stocks('300654')
    data=result['300654']
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
    return JsonResponse(data)

def klineData(request):  #k线图数据从本地文件读取
    # h5 = pd.HDFStore('D:/h5qfqdata/kday_SZ300654','r')
    h5 = pd.HDFStore('/home/ontimeKdayData/h5qfqdata/kday_SZ300654','r')
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
    data['yestclose']=yestclose 
    return JsonResponse(data, safe=False)


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