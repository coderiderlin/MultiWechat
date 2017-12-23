# https://checkapi.aliyun.com/check/checkdomain?callback=result&domain=azzzz.shop&token=check-web-hichina-com%3A7s88yvbgwterj87mk5llo6k6owagkw4u

import urllib2
import sys
import array

import msvcrt

from utils.proxyManager import ProxyManager
from utils.utils import *
from multiprocessing.dummy import Pool as ThreadPool

man=ProxyManager()
class config:
        MAX_THREAD_COUNT = 30
        FailedRetryTimes = 20
        DomainNamesList = "DomainNamesList.txt"
        resultFilename = "DomainCheck_result.txt"

def checkWithBaiduWhois(name):
    #http://whois.bj.baidubce.com/whois?format=javascript&domain=whatthesdfksdjf.com
    domainName = name + ".com"
    url = r"http://whois.bj.baidubce.com/whois?format=javascript&domain=" + domainName
    # url=r"https://checkapi.aliyun.com/check/checkdomain?callback=result&domain=azzzz.shop&token=check-web-hichina-com%3A7s88yvbgwterj87mk5llo6k6owagkw4u"
    return GetUrlContent2(url,proxies=man.popProxies())
def checkWithBaiduApi(name):
    # https://cloud.baidu.com/api/bcd/search/status
    # {"domainNames":[{"label":"sz","tld":"com"}]}
    domainName = name
    url = r"https://cloud.baidu.com/api/bcd/search/status"

    header = {
        'Connection': 'keep-alive',
        'Content-Length': '44',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://cloud.baidu.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Content-Type': 'application/json',
        'Referer': 'https://cloud.baidu.com/product/bcd/search.html?keyword=sz',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'BAIDUID=ABDF12D91049CBD5AA0895DAFCA1144D:FG=1; PSTM=1491968808; BIDUPSID=D0C77823B4F11112E550D605C212D8D9; BDUSS=DVpUlk5eUZnWmdkM09WUHE3VmJQNVhCekY2bE9Wd0tRNmFBMnpCR3RKQ202d3RhTVFBQUFBJCQAAAAAAAAAAAEAAADG3h0rY29kZXJsaW4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKZe5FmmXuRZW; MCITY=-340%3A; BCLID=10955523308864486684; BDSFRCVID=5G_sJeC62Ra1LkRAhCCwhM3RN2K2PtoTH6aopK_Jf9Dcn3ODE-HlEG0PJU8g0KubVI2-ogKK3gOTH4nP; H_BDCLCKID_SF=tbAjVIPaf-3bfTrTKb55-P_3qxby26nfMmJeaJ5nJD_BSl6q5TJNqJ8Vjf7uJbkjWgcXKqTOQpP-HqTYLp3b2h-ghJoKah5eKjREKl0MLPbYbb0xyn_VKP_bDfnMBMPe52OnaIb8LIF-MK8xejK2en-W5gT0tC62aKDX3buQJlIMqpcNLTDK2Mty2R393CrWBmr32COytn5ZjnTIylO1j4_e3bjw54vmWmO0bRIEtfTbJh5jDh3Ub6ksD-Rte4on-6Ry0hvctb3cShPmhl00Djb-jN0qJ6FsKKJ03bk8KRREJt5kq4bohjn0QnneBtQmJJrN3Cj12MoNjhOJ5P7YDpDND44HQn3yQg-q3R7MWM7keCTe-PI5XU0kqt7Q0x-jLgQPVn0MW-5DSlI4qtnJyUnybPnnBT3XLnQ2QJ8BJDtKMCQP; PSINO=6; H_PS_PSSID=25245_1423_13289_21097_20697_25439_25178_20719; CAMPAIGN_TRACK=cp%3Aaladdin%7Ckw%3A139; CAMPAIGN_TRACK_TIME=2017-12-23+18%3A15%3A11; Hm_lvt_28a17f66627d87f1d046eae152a1c93d=1513070462,1514024132; Hm_lpvt_28a17f66627d87f1d046eae152a1c93d=1514024141',
    }
    data = "{\"domainNames\":[{\"label\":\"" + domainName + "\",\"tld\":\"com\"}]}"
    return PostUrlWithDataAndHeader(url, data, header)


def checkWithAliyunApi(name):
    domainName = name + ".com"
    url = r"https://checkapi.aliyun.com/check/checkdomain?callback=result&domain=" + domainName + r"&token=check-web-hichina-com%3A7s88yvbgwterj87mk5llo6k6owagkw4u"
    # url=r"https://checkapi.aliyun.com/check/checkdomain?callback=result&domain=azzzz.shop&token=check-web-hichina-com%3A7s88yvbgwterj87mk5llo6k6owagkw4u"
    return GetUrlContent2(url)


def checkDomain(name):
    reprint("checking " + name + " ...")
    retryCount = 0
    while True:
        try:
            # response= checkWithAliyunApi(name)
            # response = checkWithBaiduApi(name)
            response = checkWithBaiduWhois(name)
            if "\"status\":0" in response:
                break;
        except BaseException as e:
            pass
        retryCount += 1
        if retryCount > config.FailedRetryTimes:
            response = "Failed:" + e.message
            break
        reprint("checking %s ... retry #%d"%(name,retryCount))
    loglToFile("%s\t%d\t--->\t" % (name, retryCount) + response, config.resultFilename)
    # logl(response)
    return "ok"


def strPlusOne(t):
    arr = array.array('B', t)
    bitCount = len(t)
    for bit in range(bitCount - 1, -1, -1):
        curChr = arr[bit] + 1
        if curChr > ord('z'):
            curChr = ord('a')
            arr[bit] = curChr
        else:
            arr[bit] = curChr
            break
    t = arr.tostring()
    return t


def BuildDomainList(fileName):
    startName = 'aa'
    endName = 'zz'
    # nameList = []
    logl("Building name list:%s to %s..." % (startName, endName))
    while startName != endName:
        # nameList.append(startName)
        startName = strPlusOne(startName)
        reprint(startName)
        appendStrToFile(startName + "\n", fileName)


def LoadDomainList(fileName):
    nameList = []
    f = open(fileName, 'r')
    for line in f.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        nameList.append(line)
    return nameList


def CheckAllDomains(nameList):
    pool = ThreadPool(config.MAX_THREAD_COUNT)
    logl(pool._processes)
    pool.map(checkDomain, nameList)
    pool.close()
    pool.join()
    logl('All done.')


def usage():
    logl("usage:%s DOMAIN_NAMES_FILE")


def raise_test():
    raise BaseException("test")


def test():
    try:
        raise_test()
    except BaseException as a:
        logl("Exception:" + a.message)


def main():
    # test()
    # return
    logl("test end.")
    if len(sys.argv) == 2:
        config.DomainNamesListFile = sys.argv[1]
        config.resultFilename = "result_" + config.DomainNamesListFile
    else:
        usage()
        return
    logl("Loading domain names from %s .." % config.DomainNamesListFile)
    nameList = LoadDomainList(config.DomainNamesListFile)
    logl("%d names loaded." % len(nameList))
    logl("Checking...")
    CheckAllDomains(nameList)
    logl("All done.")


if __name__ == '__main__':
    # BuildDomainList(DOMAIN_NAMES_FILE)
    main()
    logl("<<")
    msvcrt.getch()
    # checkDomain("as")
