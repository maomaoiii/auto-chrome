#coding=utf8
import time
import os
import ConfigParser
import string, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import httplib
import json

#conf
conf = {}

#proxy
proxy = {}



def find_element_by_id(driver,str):
    try:
        r = driver.find_element_by_id(str)
        return r
    except Exception as e:
        print (u"no such id: " + str)
    return None

def find_element_by_partial_link_text(driver,str):
    try:
        r = driver.find_element_by_partial_link_text(str)
        return r
    except Exception as e:
        print (u"no such partial_link_text: " + str)
    return None

def ip138(url, proxy_ip, proxy_port):
    #firefoxBin = os.path.abspath(r"d:\Program Files (x86)\Mozilla Firefox\firefox.exe")
    #os.environ["webdriver.firefox.bin"] = firefoxBin
    
    driver = init_deiver(proxy_ip, proxy_port)
    
    driver.delete_all_cookies()    
    
    driver.set_window_size(600,400)
    print u"打开浏览器..."
    print u"获取url: " + url
    driver.get(url)
    print u"打开完成. "
    
def search(url, proxy_ip, proxy_port):
    #firefoxBin = os.path.abspath(r"d:\Program Files (x86)\Mozilla Firefox\firefox.exe")
    #os.environ["webdriver.firefox.bin"] = firefoxBin
    
    driver = init_deiver(proxy_ip, proxy_port)
    
    driver.delete_all_cookies()    
    
    #driver.set_window_size(600,400)
    print u"打开浏览器..."
    print u"获取url: " + url
    try:
        driver.get(url)
    except Exception as e:
        print e
        print u"打开失败. "
        driver.quit()
        return 0
    print u"打开完成. "

    time.sleep(10000)
 
    driver.delete_all_cookies()

    driver.quit()
    return ret
    
def init_deiver2(ip,port):
    if (ip == "" or port == 0):
        driver = webdriver.Firefox()
        return driver

    profile = webdriver.FirefoxProfile()
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', ip)
    profile.set_preference('network.proxy.http_port', port)
    profile.set_preference('network.proxy.ssl',ip)
    profile.set_preference('network.proxy.ssl_port', port)
    profile.update_preferences()
    driver = webdriver.Firefox(profile)
    return driver

def init_deiver(ip,port):
    if (ip == "" or port == 0):
        driver = webdriver.Chrome()
        return driver

    PROXY = str(ip)+":"+str(port) # IP:PORT or HOST:PORT
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_options.add_argument('--test-type=%s' % '--ignore-certificate-errors')
    chrome_options.add_argument( '--incognito')
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    return chrome 

def readconf():
    global conf
    cf = ConfigParser.ConfigParser()
    cf.read("conf.ini")
    
    print u"================配置===================="
    kw = cf.get("link", "kw").decode("utf8")
    conf["kw"] = kw
    print (u"搜索关键词: " + kw)
    
    target_sleep = cf.get("link", "target_sleep")
    conf["target_sleep"] = target_sleep
    print (u"目标网页停留时间: " + str(target_sleep) + u"秒")
    
    link_partial_text = cf.get("link", "partial_text").decode("utf8")
    conf["link_partial_text"] = link_partial_text
    print (u"链接文字包含: " + link_partial_text)
    
    link_src = cf.get("link", "src").decode("utf8")
    conf["link_src"] = link_src
    print (u"链接地址包含: " + link_src)
    
    total = cf.get("count", "total")
    conf["total"] = total
    print (u"总共执行次数: " + str(total))
    
    gap = cf.get("count", "gap")
    conf["gap"] = gap
    print (u"每次间隔时间: " + str(gap))
    print u"========================================"

def update_proxy_yun_daili():
    #http://www.yun-daili.com/api.asp?key=409747869&getnum=1&anonymoustype=2&filter=1&area=1&sarea=1&formats=2
    #[{"Ip":"183.13.78.200","Port":3128,"Country":"广东省深圳市","FullAddres":"","ProxyType":0,"Sec":0,"AnonymousType":2}]   GBK
    httpClient = None
    url = 'http://www.yun-daili.com/api.asp?key=409747869&getnum=1&anonymoustype=2&filter=1&area=1&sarea=1&formats=2'
    ok = 0
    try:
        httpClient = httplib.HTTPConnection('www.yun-daili.com', 80, timeout=30)
        httpClient.request('GET', url)
        
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        #print response.status
        #print response.reason
        data = response.read()
        data = data.decode('gbk')
        print data
        
        obj = json.loads(data)

        proxy['ip'] = obj[0]['Ip']
        proxy['port'] = obj[0]['Port']
        proxy['de'] = obj[0]['Country'] + obj[0]['FullAddres']
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
            
def update_proxy_82ip():
    #http://www.82ip.com/api.asp?key=2199832377464169&getnum=1&anonymoustype=2&filter=1&area=1&sarea=1&formats=2&proxytype=1
    #[{"Ip":"183.13.78.200","Port":3128,"Country":"广东省深圳市","FullAddres":"","ProxyType":0,"Sec":0,"AnonymousType":2}]   GBK
    httpClient = None
    url = 'http://www.82ip.com/api.asp?key=2199832377464169&getnum=1&anonymoustype=2&filter=1&area=1&sarea=1&formats=2&proxytype=1'
    ok = 0
    try:
        httpClient = httplib.HTTPConnection('www.82ip.com', 80, timeout=30)
        httpClient.request('GET', url)
        
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        #print response.status
        #print response.reason
        data = response.read()
        data = data.decode('gbk')
        print data
        
        obj = json.loads(data)

        proxy['ip'] = obj[0]['Ip']
        proxy['port'] = obj[0]['Port']
        proxy['de'] = obj[0]['Country'] + obj[0]['FullAddres']
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

def update_proxy_66ip():
    #http://www.66ip.cn/getzh.php?getzh=2016091373964&getnum=1&isp=0&anonymoustype=2&start=&ports=&export=&ipaddress=&area=1&proxytype=1&api=https
    #124.193.51.249:3128   GBK
    httpClient = None
    url = 'http://www.66ip.cn/getzh.php?getzh=2016091373964&getnum=1&isp=0&anonymoustype=2&start=&ports=&export=&ipaddress=&area=1&proxytype=1&api=https'
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
    line = 0
    tmp = "proxy.tmp"
    txt = "proxy.data.txt"
    if os.path.exists(tmp):
        fp = open(tmp)
        a = fp.readline()
        fp.close()
        line = int(a)
        print "line=" + str(line)
    if not os.path.exists(txt):
        print u"没有代理文件:" + txt
        return
    fp = open(txt)
    ls = fp.readlines()
    fp.close()
    if (line >= len(ls)):
        line = 0
    l = ls[line].strip()
    print "l:" + l
    obj = l.split(':')
    print obj
    proxy['ip'] = obj[0]
    proxy['port'] = obj[1]
    proxy['de'] = l
    
    #回写
    fp = open(tmp, "w")
    fp.write(str(line+1))
    fp.close()
    
def update_proxy():
    update_proxy_yun_daili()
    print u'代理: ' + proxy['ip'] + ':' + str(proxy['port']) + '. ' + proxy['de']
    #ip138('http://www.ip138.com', str(proxy['ip']), int(proxy['port']))
    
def loop():
    url ='http://www.taobao.com'
    update_proxy()
    ret = search(url, str(proxy['ip']), int(proxy['port']))

    
    
if __name__ == '__main__':
    #a = u"嘿嘿"
    #print (u"测试中文输出: " + a)
         
    #readconf()
    proxy['ip'] = "121.40.108.76"
    proxy['port'] = 80#80
    proxy['de'] = 'unknow'
           
    loop()
    print u"所有任务完成"
    time.sleep(1000000)
 
