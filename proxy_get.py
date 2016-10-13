#coding=utf8
import time
import os
import json
import platform
import httplib
def update_proxy_yun_daili(num):
    print 'update_proxy_yun_daili:' + str(num)
    #http://www.yun-daili.com/api.asp?key=409747869&getnum=1&anonymoustype=2&filter=1&area=1&sarea=1&formats=2
    #[{"Ip":"183.13.78.200","Port":3128,"Country":"广东省深圳市","FullAddres":"","ProxyType":0,"Sec":0,"AnonymousType":2}]   GBK
    httpClient = None
    url = 'http://www.yun-daili.com/api.asp?key=409747869&getnum='+str(num)+'&anonymoustype=2&filter=1&area=1&sarea=1&formats=2'
    ok = 0
    result = []
    try:
        httpClient = httplib.HTTPConnection('www.yun-daili.com', 80, timeout=30)
        httpClient.request('GET', url)
        
        response = httpClient.getresponse()
        #print response.status
        #print response.reason
        data = response.read()
        data = data.decode('gbk')
        print data
        
        obj = json.loads(data)
        for o in obj:
            r = {}
            r['ip'] = o['Ip']
            r['port'] = o['Port']
            r['de'] = o['Country'] + o['FullAddres']
            result.append(r)
        ok = 1
        return result
        
    except Exception, e:
        print e
        print u'代理获取失败'
    finally:
        if httpClient:
            httpClient.close()
        if ok == 0:
            print u'代理获取失败'
    if (ok == 1):
        return result
    return False
            
def update_proxy_82ip(num):
    #http://www.82ip.com/api.asp?key=2199832377464169&getnum=1&anonymoustype=2&filter=1&area=1&sarea=1&formats=2&proxytype=1
    #[{"Ip":"183.13.78.200","Port":3128,"Country":"广东省深圳市","FullAddres":"","ProxyType":0,"Sec":0,"AnonymousType":2}]   GBK
    httpClient = None
    url = 'http://www.82ip.com/api.asp?key=2199832377464169&getnum='+str(num)+'&anonymoustype=2&filter=1&area=1&sarea=1&formats=2&proxytype=1'
    ok = 0
    result = []
    try:
        httpClient = httplib.HTTPConnection('www.82ip.com', 80, timeout=30)
        httpClient.request('GET', url)
        
        response = httpClient.getresponse()
        #print response.status
        #print response.reason
        data = response.read()
        data = data.decode('gbk')
        print data
        
        obj = json.loads(data)
        for o in obj:
            r = {}
            r['ip'] = o['Ip']
            r['port'] = o['Port']
            r['de'] = o['Country'] + o['FullAddres']
            result.append(r)
        return result
        ok = 1
    except Exception, e:
        print e
        print u'代理获取失败'
    finally:
        if httpClient:
            httpClient.close()
        if ok == 0:
            print u'代理获取失败'
    if (ok == 1):
        return result
    return False

def update_proxy_66ip(num):
    #http://www.66ip.cn/getzh.php?getzh=2016091373964&getnum=1&isp=0&anonymoustype=2&start=&ports=&export=&ipaddress=&area=1&proxytype=1&api=https
    #124.193.51.249:3128   GBK
    httpClient = None
    url = 'http://www.66ip.cn/getzh.php?getzh=2016091373964&getnum='+str(num)+'&isp=0&anonymoustype=2&start=&ports=&export=&ipaddress=&area=1&proxytype=1&api=https'
    ok = 0
    try:
        httpClient = httplib.HTTPConnection('www.66ip.cn', 80, timeout=30)
        httpClient.request('GET', url)
        
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        #print response.status
        #print response.reason
        data = response.read()
        data = str(data)
        print data
        s = ''
        for i in range(len(data)):
            if (data[i].isdigit() or data[i] == '.' or data[i] == ':'):
                s = s+ data[i]
            elif (data[i] == '<'):
                break
        
        obj = s.split(':')
        print s

        proxy['ip'] = obj[0]
        proxy['port'] = obj[1]
        proxy['de'] = data
        ok = 1
            
    except Exception, e:
        print e
        ok = 2
        print u'代理获取失败'
    finally:
        if httpClient:
            httpClient.close()
        if ok == 0:
            print u'代理获取失败'
            
def update_proxy_file():
    txt = "proxy.db.txt"
    if not os.path.exists(txt):
        print u"没有代理文件:" + txt
        return False
    fp = open(txt)
    ls = fp.readlines()
    fp.close()
    result = []
    sp = [':', ' ', '\t', '\t\t']
    for l in ls:
        l = l.strip()
        print l
        
        for s in sp:
            obj = l.split(s)
            if (len(obj) > 1):
                break
        if (len(obj) < 2):
            continue
        proxy = {}
        proxy['ip'] = obj[0]
        proxy['port'] = int(obj[1])
        proxy['de'] = l
        result.append(proxy)
    return result
