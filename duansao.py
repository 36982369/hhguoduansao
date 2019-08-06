#导包
from optparse import OptionParser
import socket
import re
import threading
import queue
from colorama import init
init(autoreset=True)


#定义字体颜色
RED = '\033[1;31m'
GREE = '\033[1;32m'
YLLO = '\033[1;33m'


que = queue.Queue()
USAGE = '''
Usage: python pscan.py 8.8.8.8
       python pscan.py 8.8.8.8 -p 21,80,8080
       python pscan.py 8.8.8.8 -p 21,80,8080 -n 50

'''

class Scanner(object):
    def __init__(self, target,port,threadum = 100):
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", target):
            self.target = target
        else:
            print(RED+"[*] Ip Invalid !!")
            exit()

        self.port= port
        self.threadum = threadum


    def start(self):
        if self.port == 65535:
            for i in range(0,65536):
                que.put(i)

        else:
            for i in self.port:
                if int(i) < 0 or int(i) > 65535:
                    print(RED+'\n[-] 端口错误，请指定0~65535之间的端口')
                    exit()
                    quit.put(i)
            

        try:
            print(RED+"[*] 正在扫描%s"%self.target)
            thread_poll = []
            for i in range(0,int(self.threadum)):
                th = threading.Thread(target=self.run,args=())
                thread_poll.append(th)
            for th in thread_poll:
                th.setDaemon(True)
                th.start()
            que.join()
            print(RED+"[*] 完成扫描!!")

        except Exception as e:
            pass
        except KeyboardInterrupt:
            print(RED+"用户退出扫描")

    def run(self):
        while not que.empty():
            port=int(que.get())
            if self.portScan(port):
                banner=self.getSockertBanner(port)
                if banner:
                    print(GREE+"%d--- open    "%(port)+banner)
                else:
                    print(GREE+"%d--- open    "%(port))
                que.task_done()


    def portScan(self,port):
        try:
            sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sk.settimeout(5)
            if sk.connect_ex((self.target,port)) == 0:
                return True
            else:
                return False
        except Exception as e:
            print("partscan:error",e)
            pass
        except KeyboardInterrupt:
            print(RED+"[*] 用户自行退出扫描")
            exit()
        finally:
            sk.close()

    def getSockertBanner(self,port):
        try:
            sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sk.settimeout(0.5)
            sk.connect((self.target,port))
            sk.send("Hello\r\n".encode("utf-8"))
            return sk.recv(2048).decode("utf-8")
        except Exception as e:
            pass
        finally:
            sk.close()

#工具提示
parser = OptionParser()
#提示-p -n
parser.add_option('-p','--port',action="store",type="str",dest="port",help="All ports to be scanned default All port")
parser.add_option('-n','--num',action="store",type="int",dest="threadum",help="Thrude num default 100")
(option,args)=parser.parse_args()
#根据用户操作来判断程序执行
if option.port == None and option.threadum == None and len(args) == 1:
    scanner = Scanner(args[0],65535)
    scanner.start()
#if 用户没指定端口只指定ip就扫描全端口0-65535
elif option.port != None and option.threadum == None and len(args) == 1:
    port = option.port.split(',')
    scanner = Scanner(args[0],port)
    scanner.start()
elif option.port == None and option.threadum != None and len(args) == 1:
    scanner = Scanner(args[0],65535,option.threadum)
    scanner.start()
elif option.port != None and option.threadum != None and len(args) == 1:
    port = option.port.split(',')
    scanner = Scanner(args[0],port,option.threadum)
    scanner.start()
else:
    print(GREE+USAGE+GREE)
    parser.print_help()




