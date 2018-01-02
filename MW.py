import frida
import sys
import time
from utils.utils import *


class ProcessHooker:
    def __init__(self,cmd):
        self.pid=frida.spawn(cmd)
        self.session=frida.attach(self.pid)


    def _process_message(self, message, data):
        """
            Frida COMMS
        """
        try:
            if message['type'] == 'send':
                stanza = message['payload']
                if stanza['name'] == '+log':
                    msg = str(stanza["payload"])
                    logl("[" + str(self.pid) + "]\t" + msg)
                    # try:
                    #     self.extract.post({'type': '+log-ack'})
                    # except Exception as e:
                    #     pass

                elif stanza['name'] == '+pkill':
                    logl("Kill Sub-Process: " + str(stanza['payload']))

            else:
                logl("==========ERROR==========")
                logl(message)
                logl("=========================")
        except Exception as ae:
            #logl("exception on _process_message")
            pass


    def inject_script(self,jsfile):
        # TODO: upgade to use frida-compile
        with open(jsfile) as fp:
            script_js = fp.read()
        self.extract = self.session.create_script(script_js, name="mw.js")
        self.extract.on('message', self._process_message)
        self.extract.load()
        logl("js loaded.")

    def go(self):
        logl("resume pid:"+str(self.pid))
        frida.resume(self.pid)

    def waitToDie(self):
        sys.stdin.read()
        self.session.detach()





def main():
    #cmd=[r"F:\projects\C++\win32\Release\win32.exe"]
    cmd=[r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe"]
    jsfile="mw.js"
    Hooker=ProcessHooker(cmd)
    logl("process spwnded.");
    Hooker.inject_script(jsfile)
    logl("js injected.");
    #time.sleep(1)
    Hooker.go()
    logl("go!");
    Hooker.waitToDie()
    logl("end")




if __name__ == '__main__':
    main()
