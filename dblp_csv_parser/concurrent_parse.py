#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : CageTian (cagetian@outlook.com)
#将三个文件的需要的字段组合到一起并输出到另一个文件

import io
import codecs
import threading
import time
import re
import queue

f1=codecs.open("D:\\Dowloads\\advisee_advisor_condition.csv","r", "utf-8")
f2=codecs.open("D:\\Dowloads\\advisee_condition.csv","r", "utf-8")
f3=codecs.open("D:\\Dowloads\\adviseeNet_condition.csv","r", "utf-8")
f_in=codecs.open("D:\\condition_parse.csv", "w", "utf-8")


str_tmp=['advisee','advisor','time']#用来储存三个文件合并后的字符串数组
str_tmp2=['','','']

def parse_f1(line=''):
    parse_line=''
    line1=re.sub(r'(?<=,\d{4}),(?=\d{1,3}(?!\d))',':',line)
    u_line=line1.split(',',5)
    for u in u_line:
        parse_line+='\"'+u+'\",'
    return parse_line[:-4]+'\"'

def parse_f2(line=""):
    parse_line=''
    index=line.find(',')
    u_line=line.split(',',3)
    for u in u_line:
        parse_line+='\"'+u+'\",'
    line1=re.sub(r'(?<=\d{4}),(?=\d{1,3}(?!\d))',':',parse_line)
    return ',\"'+line1[index+4:-4]+'\",'


def parse_f3(line=''):
    parse_line=''
    u_line=line.split(',',2)
    for u in u_line:
        parse_line+='\"'+u+'\",'
    line1=re.sub(r'(?<!\"),(?=\d{1,3}(?!\d))',':',parse_line)
    index=line1.find(',')
    return line1[index+1:-4]+'\"\r\n'



class Reader(threading.Thread):#读文件的线程
    def __init__(self, cond, name,que,func,*arg):
        super(Reader, self).__init__()
        self.cond = cond
        self.name = name
        self.que=que
        self.func=func
        self.arg=arg
    def run(self):
        done=0
        while not done:
            self.cond.acquire()
            line = self.arg[0].readline()
            if(line!=''):
                self.que.put(self.func(line))
                self.cond.notify()
            else:
                print(self.name+":done!")
                done=1;
                self.cond.notify()

            #print (self.name )
            #time.sleep(2)

            self.cond.release()
        self.arg[0].close
        print(self.name+"fuck---------------------------------------------------------------")

class Writer(threading.Thread):
    def __init__(self, cond1,cond2,cond3,name,file):
        super(Writer, self).__init__()
        self.cond1 = cond1
        self.cond2 = cond2
        self.cond3 = cond3
        self.name = name
        self.file=file
    def run(self):
        done=0
        time.sleep(2)
        global que1,que2,que3
        global f_in
        while not done:
            if(self.cond1.acquire() and self.cond2.acquire() and self.cond3.acquire()):
                if que2.qsize()==0 or que1.qsize()==0 or que3.qsize()==0:
                    print('ssdd')
                    done=1;
                else:
                    #print(self.name+':'+que1.get()+que2.get()+que3.get(),que3.qsize())
                    f_in.write(que1.get()+que2.get()+que3.get())
            self.cond1.release()
            self.cond2.release()
            self.cond3.release()
        f_in.close
        print("finished")

cond1 = threading.Condition()
cond2 = threading.Condition()
cond3 = threading.Condition()

que1=queue.Queue()
que2=queue.Queue()
que3=queue.Queue()

reader1 = Reader(cond1,'reader1',que1,parse_f1,f1)
reader2 = Reader(cond2,'reader2',que2,parse_f2,f2)
reader3 = Reader(cond3,'reader3',que3,parse_f3,f3)
writer = Writer(cond1,cond2,cond3, 'writer',f_in)

# reader1.setDaemon(True)
# reader2.setDaemon(True)
# reader3.setDaemon(True)
# writer.setDaemon(True)

reader1.start()
reader2.start()
reader3.start()
writer.start()
writer.join()