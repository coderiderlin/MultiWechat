# https://checkapi.aliyun.com/check/checkdomain?callback=result&domain=azzzz.shop&token=check-web-hichina-com%3A7s88yvbgwterj87mk5llo6k6owagkw4u

import urllib2
import sys
import array

from utils.utils import *
from multiprocessing.dummy import Pool as ThreadPool

DOMAIN_NAMES_FILE = "DomainNamesFile.txt"
DomainCheckResult = "DomainCheckResult.txt"


def checkDomain(name):
    domainName = name + ".com"
    reprint("checking "+domainName+" ...")
    url = r"https://checkapi.aliyun.com/check/checkdomain?callback=result&domain=" + domainName + r"&token=check-web-hichina-com%3A7s88yvbgwterj87mk5llo6k6owagkw4u"
    # url=r"https://checkapi.aliyun.com/check/checkdomain?callback=result&domain=azzzz.shop&token=check-web-hichina-com%3A7s88yvbgwterj87mk5llo6k6owagkw4u"
    response = GetUrlContent2(url)
    appendStrToFile(response + "\n", DomainCheckResult)
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
    startName = 'aaaaa'
    endName = 'zzzzz'
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
    pool = ThreadPool()
    pool.map(checkDomain, nameList)
    pool.close()
    pool.join()
    logl('All done.')


def main():
    logl("Loading domain names from %s .." % DOMAIN_NAMES_FILE)
    nameList = LoadDomainList(DOMAIN_NAMES_FILE)
    logl("%d names loaded."%len(nameList))
    logl("Checking...")
    CheckAllDomains(nameList)
    logl("All done.")


if __name__ == '__main__':
    # BuildDomainList(DOMAIN_NAMES_FILE)
    main()
    # checkDomain("aaaaa")
