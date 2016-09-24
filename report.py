import requests
import re
from configparser import ConfigParser
import time



s = requests.Session()
url2 =''
url1=''
def response1(str):
        a=re.compile('var\sdata\s\=\sJSON\.parse\(\"(.*)\"\)\;')
        ln=a.findall(str)[0].replace("\\","")
        x=re.sub('\]\,',"]\n",ln)
        return x


def xmloutput(bx):
        b=re.compile('\[\".*\"\,\".*\"\,(.*)\,\".*\"\]\n')
        ft = b.findall(bx)
		#ft.pop(0)
        i=-1
        sg="<SG>\n"
        for line in ft:
                i=i+1
				if i > 1:
					sg =sg+"<Block"+str(i)+">"+line.replace("\"","")+"</Block1>\n"
        sg=sg+"</SG>"

        sg.replace('\<Block0\>MOUDA\<\/Block0\>','')
        print (sg)
        return sg

def response2( txt ):
        a=re.compile('\:\[(.*)\]\}')
        ln=a.findall(txt)[0].replace("\\","")
        x=re.sub('\]\,',"]\n",ln)
        return x



def readProperties():
        parser = ConfigParser()
        parser.read('report.properties')
        global url1,url2
        url1=parser.get('reports', 'url1')
        url2=parser.get('reports', 'url2')
        return;

def getDate():
        todaytime=time.strftime("%d-%m-%Y")
        return todaytime;
def getFileName():
        return "report"+getDate()+".xml";

def writeToFile(xmlValue):
    text_file = open(getFileName(),'w')
    text_file.write(xmlValue)
    text_file.close()
    return


def prepareHeadRequest():
        cookie = {'ASP.NET_SessionId': '17ab96bd8ffbe8ca58a78657a918558'}
        sec ={'Upgrade-Insecure-Requests': '1'}
        s.headers.update({'Upgrade-Insecure-Requests': '1'})
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'})
        return cookie


#url2 ='http://103.7.130.121/WBES/Report/GetDeclarationReport?regionId=2&date=23-09-2016&revision=27&utilId=f9b9e90c-1380-4eb1-bb00-8a0ea85f059c&isBuyer=0&byOnBar=0'
#url1 = 'http://103.7.130.121/WBES/ReportFullSchedule/GetFullInjSummary?scheduleDate=21-09-2016&sellerId=f9b9e90c-1380-4eb1-bb00-8a0ea85f059c&revisionNumber=62&regionId=2&byDetails=0&isDrawer=0&isBuyer=0'


readProperties()
cookie=prepareHeadRequest()

print(url1)
print(url2)
r1 = s.get(url1, cookies=cookie)
txt1=response1(r1.text)
xml1=xmloutput(txt1)

r2=s.get(url2,cookies=cookie)
txt2=response2(r2.text)
xml2=xmloutput(txt2)


xml=xml1+'\n'+ xml2
writeToFile(xml)
