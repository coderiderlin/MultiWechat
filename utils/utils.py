import os
import subprocess
import threading
import time

import chardet
import sys


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
    appendStrToFile(msg, filepath)


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
    msg=str(msg)
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