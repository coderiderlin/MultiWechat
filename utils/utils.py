import os
import random
import subprocess
import threading
import time
import urllib
import urllib2

import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
from requests import ConnectionError

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def appendStrToFile(sstr, filepath):
    f = open(filepath, "a+")
    try:
        sstr = sstr.encode('utf-8')
    except Exception, e:
        pass
    f.write(sstr)
    f.close()


def logToFile(msg, filepath):
    prefix = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]"
    logtext = prefix + "\t" + msg
    appendStrToFile(logtext, filepath)


def loglToFile(msg, filepath):
    logToFile(msg + "\n", filepath)


def logBase(msg):
    sys.stdout.write(msg)
    appendStrToFile(msg, r"f:\bciBuild.log")


def log(msg):
    prefix = "[" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]"
    logtext = prefix + "\t" + msg
    logBase(logtext)


def loglplus(msg):
    log("[+] " + msg + "\n")


def loglminer(msg):
    log("[-] " + msg + "\n")


def logldot(msg):
    log("[.] " + msg + "\n")


def logldebug(msg):
    log("[D] " + msg + "\n")


def logl(msg):
    msg = str(msg)
    log("[.] " + msg + "\n")


def GetEncoding(data):
    chardit1 = chardet.detect(data)
    encoding = chardit1['encoding']
    # logd("encode:"+encoding)
    return encoding


def DoCmd_pexpect(cmd):
    logldebug("DoCmd_pexpect:[" + cmd + "]")
    # print("spawn..%d")%(threading._get_ident())
    # deadlock here sometimes,inside the ReadFile.
    spawn = 0  # winpexpect.winspawn("cmd.exe /c "+cmd)
    # print("spawn..done")
    text = ""
    bEmpty = True
    while True:
        out = spawn.read(16);
        if out != "":
            bEmpty = False
            text += out

        # print("empty:%d isalive:%d")%(bEmpty,spawn.isalive())
        if bEmpty and not spawn.isalive():
            break
        bEmpty = True

    # print(text)
    if text == "":
        ret = ""
    else:
        encoding = GetEncoding(text)
        ret = text.decode(encoding)
    ret = ret.strip()
    logldebug("result_pexpect:[" + ret + "]")
    return ret


def DoCmd_OsPopen(cmd):
    cmdLogFile = r"d:\bcicmd.log"
    msg = "DoCmd_system:[" + cmd + "]"
    loglToFile(msg, cmdLogFile)
    ret = os.popen("%s 2>&1" % cmd).read()
    msg = "result:[" + ret + "]"
    loglToFile(msg, cmdLogFile)
    return ret


def DoCmd_popen(cmd):
    logldebug("DoCmd_popen:[" + cmd + "]")
    process = subprocess.Popen("cmd.exe /c " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    text = ""
    bEmpty = True;
    while True:
        # print("reading... stdout")
        out = process.stdout.read(16)
        # print("reading... stderr")

        # deadlock here sometimes
        err = process.stderr.read(16)
        # print("reading... done")

        if out != '':
            text += out
            bEmpty = False
            # print(out)
        if err != '':
            text += err
            bEmpty = False
            # print(err)
        if bEmpty and process.poll() != None:
            break
        bEmpty = True
        # print("poll..\n");
    # print(text)
    if text == "":
        ret = ""
    else:
        encoding = GetEncoding(text)
        ret = text.decode(encoding)
    ret = ret.strip()
    logldebug("result_popen:[" + ret + "]")
    return ret


def DoCmd(cmd, use_expect=False):
    return DoCmd_OsPopen(cmd)
    if not use_expect:
        return DoCmd_popen(cmd)
    return DoCmd_pexpect(cmd)


# write "data" to file-filename
def writeFile(filename, data):
    f = open(filename, "w")
    f.write(data)
    f.close()


def getFileMd5(filepath):
    return DoCmd("md5sum " + filepath + "|grep -oE '[a-zA-Z0-9]{32}'").strip()
    pass


def reprint(msg):
    sys.stdout.write("\r" + msg)


def urlencode(val):
    if isinstance(val, unicode):
        return urllib.quote(str(val), safe='/:?=')
    return urllib.quote(val, safe='/:?=')


def GetUrlContent(url):
    request = urllib2.Request(urlencode(url))
    response = urllib2.urlopen(request)
    page = response.read()
    logl(page)
    encoding = GetEncoding(page)
    return page.decode(encoding)


def get_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }


TIMEOUT = 5


def GetUrlContent2(url,proxies=None):
    try:
        if proxies is None:
            r = requests.get(url=url, headers=get_header(), timeout=TIMEOUT)
        else:
            r = requests.get(url=url, headers=get_header(), timeout=TIMEOUT,proxies=proxies)
        r.encoding = chardet.detect(r.content)['encoding']
    except Exception as e:
        raise BaseException("#ConnectionException:"+str(e.message))
    if not r.ok:
        # raise ConnectionError
        raise BaseException("#ConnectionError:"+str(r.reason))
    else:
        return r.text


def PostUrlWithDataAndHeader(url, data, header,proxies=None):
    try:
        if proxies is None:
            r = requests.post(url=url, data=data, headers=header, timeout=TIMEOUT)
        else:
            r = requests.post(url=url, data=data, headers=header, timeout=TIMEOUT,proxies=proxies)
        r.encoding = chardet.detect(r.content)['encoding']
    except Exception as e:
        raise BaseException("#ConnectionException:"+e.message)
    if not r.ok:
        # raise ConnectionError
        raise BaseException("#ConnectionError"+str(r.reason))
    else:
        return r.text
