#coding=utf8
import time
import os
import json
import platform
import multiprocessing
import httplib

from proxy_get import *

g_suc = 0

def isWindowsSystem():
    return 'Windows' in platform.system()
 
def isLinuxSystem():
    return 'Linux' in platform.system()

def get_url(url, proxy_ip, proxy_port):
    if (isWindowsSystem()):
        return windows_get_url(url, proxy_ip, proxy_port)
    return linux_get_url(url, proxy_ip, proxy_port)

#retcode,msg,httpcode,body,head,usetime    
def linux_get_url(url, proxy_ip, proxy_port):
    #TODO
    return False
    
#retcode,msg,httpcode,body,head,usetime
def windows_get_url(url, proxy_ip, proxy_port):
    cmd = 'HttpsClient.exe "%s" "%s" %u 20' % (url, proxy_ip, proxy_port)
    f = os.popen(cmd, "r")
    res = f.readline()
    res = res.decode('gbk')
    jok = False
    try:
        jok = True
        obj = json.loads(res)
    except Exception as e:
        jok = False
    if ((not jok) or obj["retcode"] != 0):
        print "["+proxy_ip+":"+str(proxy_port)+"@@"+url+"]run cmd error:" + res
        return False
    return obj

def send_to_db(info):
    global g_suc
    print "send_to_db:" + str(info)
    url = "http://p.chensanpang.com/input.php?req=" + str(json.dumps(info))
    print url
    try:
        httpClient = httplib.HTTPConnection('p.chensanpang.com', 80, timeout=30)
        httpClient.request('GET', url)
        response = httpClient.getresponse()
        data = response.read()
        data = data.decode('utf8')
        print data
        obj = json.loads(data)
        if (obj["ret"] != 0):
            print u"录入失败:" + obj["msg"]
        else:
            tip = u"录入成功."
            for d in obj["data"]:
                if (obj["data"][d]["retcode"] != 0):
                    tip = u"录入失败:" + str(obj["data"][d])
                else:
                    g_suc = g_suc + 1
                print str(d) +":" + tip
            
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()
    
    
def check(proxy_ip, proxy_port):
    result = {'validate':1, 'anonymous':0, 'ip':proxy_ip, 'port':proxy_port, 'delay':10000, 'https':0}
    obj = get_url("http://p.chensanpang.com/echo_head.php", proxy_ip, proxy_port)
    if (not obj or len(obj["body"]) < 10):
        result['validate'] = 0
        print "head get error " + str(obj) +"\r\n"
        #print "check:" + str(result)
        return result
    
    if ("Via:" not in obj["body"]):
        result['anonymous'] = 1
    result['delay'] = obj['usetime']
    obj = get_url("https://www.baidu.com", proxy_ip, proxy_port)
    if (not obj or len(obj["body"]) < 10):
        result['https'] = 0
    else:
        result['https'] = 1
    #print "check:" + str(result)
    return result
    
def multi_check(list):
    pool = multiprocessing.Pool(processes=10)
    result = []
    for l in list:
        print l
        result.append(pool.apply_async(check,(l["ip"], l["port"] ,) ))
    pool.close()
    pool.join()
    ok = []
    #print "all multi_check res:" + str(result)
    for res in result:
        #print "multi_check res:" + str(res.get())
        if res.get()["validate"] == 1:
            ok.append(res.get())
    if (len(ok) > 0):
        send_to_db(ok)
        
    
if __name__ == '__main__':
    type = 'file' #url
    if (type=='file'):
        list = update_proxy_file()
        if (len(list) > 0):
            multi_check(list)
            print u'成功' + str(g_suc) + u'个'
            
    if (type == 'url'):
        for i in range(0, 100):
            time.sleep(5)
            list = update_proxy_yun_daili(10)
            if (not list):
                continue
        
            multi_check(list)
            if (g_suc >= 10):
                print u'成功' + str(g_suc) + u'个'
                break
    