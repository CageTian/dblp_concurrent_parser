#coding: utf-8
import io
import codecs
import re
import linecache
f=codecs.open("D:\\111.csv","r", "utf-8")
f2=codecs.open("D:\\112.csv", "w", "utf-8")
done=0
count=0;

def deal(matched):
    value1=matched.group('value1')
    value2=matched.group('value2')
    value3=matched.group('value3')
    num=matched.group('num')
    return str(value1+':'+num+','+value2+':'+num+','+value3+':'+num)


def sub_line(line=''):
    print(re.sub(r'(?<=\d,)\"(?P<value1>.+)\s(\"\"(?P<value2>.+))+\"\"\s(?P<value3>.+)\",(?P<num>\d*)',deal,line))



def check_lines(line=''):
    global count
    if(line.count('\"')>18):
        count+=1
        print('someting wrong',count)
        #f2.write(line)
        print(re.search(r'\".+\s(\"\".+)+\"\"\s.+\"(?=,\d)',line))

while not done:
     line = f.readline()
     if(line!=''):
        check_lines(line)
     else:
        print("done!")
        done=1;
f.close
f2.close
