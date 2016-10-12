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
    
    driver.set_window_size(600,400)
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
    
        
    #搜索
    q = find_element_by_id(driver, "q")
    form = find_element_by_id(driver, "J_TSearchForm")
    if (q == None or form == None):
        print u"找不到输入表单"
        driver.delete_all_cookies()
        driver.quit()
        return 0
    
    print u"输入关键词: " + conf["kw"]
    q.send_keys(conf["kw"]);
    time.sleep(0.01)
    form.submit()
    
    #等待搜索结果页面加载完成，并点击目标链接
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "J_SearchForm"))
        )
        print u"搜索结果页面加载完成."
    except Exception as e:
        print u"搜索超时."
        driver.delete_all_cookies()
        driver.quit()
        return 0
        
    lk = find_element_by_partial_link_text(driver, conf["link_partial_text"])
    print u"查找目标链接... 包含 " + conf["link_partial_text"]
    if (lk == None):
        print u"找不到目标链接."
        driver.delete_all_cookies()
        driver.quit()
        return 0
        
    print (u"目标链接已找到，链接文字: " + lk.text)
    print (u"点击链接.")
    lk.click()
    
    #等待目标页面结果
    ret = 0
    try:
        element = WebDriverWait(driver, 10).until(
            EC.title_contains(u"淘宝")
        )
        print u"目标页面加载完成."
        ret = 1
        time.sleep(float(conf["target_sleep"]))
    except Exception as e:
        print u"目标页面加载超时."
        
    #退出浏览器
    print u"退出浏览器."
 
    driver.delete_all_cookies()

    driver.quit()
    return ret
    
def init_deiver(ip,port):
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
    url = 'http://www.yun-daili.com/api.asp?key=409747869&getnum=1&anonymoustype=2&filter=1&sarea=1&formats=2&proxytype=1'
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
 
def update_proxy():
    update_proxy_yun_daili()
    print u'代理: ' + proxy['ip'] + ':' + str(proxy['port']) + ' ' + proxy['de']
    #ip138('http://www.ip138.com', str(proxy['ip']), int(proxy['port']))
    
def loop():
    total = int(conf["total"])
    gap = float(conf["gap"])
    suc = 0
    fail = 0
    url ='http://www.taobao.com'
    for i in range(1,total+1):
        print u"第" + str(i) + u"次:"
        update_proxy()
        ret = search(url, str(proxy['ip']), int(proxy['port']))
        result = u"失败"
        if (ret == 1):
            result = u"成功"
            suc = suc + 1
        else:
            fail = fail + 1
        print u"第" + str(i) + u"次结果:" + result
        print u"总成功:" + str(suc) + u",失败:" + str(fail) + u",进度:" + str(i) + u"/" + str(total)
        time.sleep(gap)
    
    
if __name__ == '__main__':
    #a = u"嘿嘿"
    #print (u"测试中文输出: " + a)
         
    readconf()
    proxy['ip'] = "218.244.149.184"
    proxy['port'] = 0 #8888
    proxy['de'] = 'unknow'
           
    loop()
    print u"所有任务完成"
    time.sleep(1000000)
 