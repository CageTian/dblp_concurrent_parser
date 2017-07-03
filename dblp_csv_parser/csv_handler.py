#coding: utf-8
#将三个文件的需要的字段组合到一起并输出到另一个文件
import io
import codecs
import re
import linecache
f1=codecs.open("D:\\Dowloads\\advisee_condition1.csv","r", "utf-8")
fN=codecs.open("D:\\Dowloads\\adviseeNet_condition1.csv","r", "utf-8")
fD=codecs.open("D:\\Dowloads\\advisee_advisor_condition1.csv","r", "utf-8")
f2=codecs.open("D:\\condition_parse2.csv", "w", "utf-8")
done = 0

def parse_f1(line=""):
    parse_line=''
    index=line.find(',')
    u_line=line.split(',',3)
    for u in u_line:
        parse_line+='\"'+u+'\",'
    line1=re.sub(r'(?<=\d{4}),(?=\d{1,3}(?!\d))',':',parse_line)
    return ',\"'+line1[index+4:-4]+'\",'

def parse_f2(line=''):
    parse_line=''
    line1=re.sub(r'(?<=,\d{4}),(?=\d{1,3}(?!\d))',':',line)
    u_line=line1.split(',',5)
    for u in u_line:
        parse_line+='\"'+u+'\",'
    return parse_line[:-3]+'\"\r\n'

def parse_f3(line=''):
    parse_line=''
    u_line=line.split(',',2)
    for u in u_line:
        parse_line+='\"'+u+'\",'
    line1=re.sub(r'(?<!\"),(?=\d{1,3}(?!\d))',':',parse_line)
    return line1[:-3]+'\"\r\n'




# while not done:
#      line = f.readline()
#      line.find(',')
#      if(line!=''):
#         #print(line)
#         f2.write(parse_line1(line))
#      else:
#         print("done!")
#         done=1;

while not done:
     line = f1.readline()
     if(line!=''):
        #print(line)
        print(parse_f1(line))
     else:
        print("done!")
        done=1;

f1.close
fN.close
fD.close
f2.close