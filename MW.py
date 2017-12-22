import frida
import sys
from utils.utils import *

reload(sys)
sys.setdefaultencoding('utf8')

class ProcessHooker:
    def __init__(self,cmd):
        self.pid=frida.spawn(cmd)
        self.session=frida.attach(self.pid)


    def _process_message(self, message, data):
        """
            Frida COMMS
        """
        if message['type'] == 'send':
            stanza = message['payload']
            if stanza['name'] == '+log':
                msg=str(stanza["payload"])
                logl("["+str(self.pid)+"]\t"+msg)
                try:
                    self.extract.post({ 'type': '+log-ack' })
                except Exception as e:
                    pass

            elif stanza['name'] == '+pkill':
                logl( "Kill Sub-Process: " + str(stanza['payload']))

        else:
            logl( "==========ERROR==========")
            logl(message)
            logl("=========================")

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


def main():
    cmd=[r"F:\projects\C++\win32\Release\win32.exe"]
    jsfile="mw.js"
    Hooker=ProcessHooker(cmd)
    logl("process spwnded.");
    Hooker.inject_script(jsfile)
    logl("js injected.");
    Hooker.go()
    logl("go!");

if __name__ == '__main__':
    main()
