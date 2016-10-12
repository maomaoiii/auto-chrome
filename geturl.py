#coding=utf8
import time
import os
import json
import sys 

    
#sys.agrv[1] : url
#         2  : ip
#         3  : port
#         4  : timeout
if __name__ == '__main__':
    url = 'https://www.baidu.com'
    ip = ''
    port = 0
    timeout = 10
    proxy = ''
    if (len(sys.argv) > 1):
        url = str(sys.argv[1])
    if (len(sys.argv) > 3):
        ip = sys.argv[2]
        port = int(sys.argv[3])
    if (len(sys.argv) > 4):
        timeout = int(sys.argv[4])
    if (len(ip) > 5 and port > 0):
        proxy = '--proxy "%s:%d"' % (ip, port)
    bf = "tmpbody.txt"
    hf = "tmphead.txt"
    ff = "tmpfail.txt"
    cmd='curl --silent --connect-timeout %d --max-time %d "%s" %s --dump-header %s >%s --stderr %s' % (timeout, timeout, url, proxy, hf, bf, ff)
    start = int(time.time())
    ret = os.system(cmd)
    end = int(time.time())
    bodyf = open(bf,"r")
    body = bodyf.read()
    bodyf.close()
    headf = open(hf,"r")
    head = headf.read()
    headf.close()
    failf = open(ff,"r")
    fail = failf.read()
    failf.close()
    result = {'retcode':0, 'msg':'', 'body':'', 'head':'','usedtime':10}
    if (ret == 0 and len(fail)>1):
        ret = 1
    result["retcode"] = ret
    if (len(fail)>1):
        result["msg"] = fail
    result["body"] = body
    result["head"] = head
    result["usedtime"] = end-start
    print result

