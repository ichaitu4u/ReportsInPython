import requests
import re
from configparser import ConfigParser
import time
import os
import logging
import sys
#properties values..
url=''
url2 =''
url1=''
url0=''
saledId= ''
saleName=''
revision=''
regionId=''
datevalue=''
reportLocation=''
s = requests.Session()
def response1(strvalue):
        #print1(strvalue)
        a=re.compile('JSON\.parse\(\"(.*)\"\)\;')
        ln=a.findall(strvalue)[0].replace("\\","")
        x=re.sub('\]\,',"]\n",ln)
        return x
    
    
def response0(strVale): 
        
        strVale.replace("UtilId","\nUtilId")
        x=re.sub('UtilId',"\nUtilId",strVale)
        #print(x)
        exp='UtilId\"\:\"(.*)\.*\"Acronym\"\:\"'+saledId+'\"\,'
        b=re.compile(exp)
        ln=b.findall(x)[0].split('\"')[0]
        print1('salesid: '+ln)
        return ln   


def xmloutput(bx,typechar):
        b=re.compile('\[\".*\"\,\".*\"\,(.*)\,\".*\"\]\n')
        ft = b.findall(bx)
        i=-1
        sg="<"+typechar+">\n"
        for line in ft:
                i=i+1
                if i>=1 :
                    sg =sg+"<Block"+str(i)+">"+line.replace("\"","")+"</Block"+str(i)+">\n"
        sg=sg+"</"+typechar+">"

        
        #print (sg)
        return sg

def response2( txt ):
        a=re.compile('\:\[(.*)\]\}')
        ln=a.findall(txt)[0].replace("\\","")
        x=re.sub('\]\,',"]\n",ln)
        return x



def readProperties():
        parser = ConfigParser()
        properties_path = os.path.dirname(os.path.realpath(__file__))+"\\"+'report.properties'
        parser.read(properties_path)
        global url1,url2,url0,saledId,revision,regionId,datevalue,reportLocation,saleName
        urlip=parser.get('reports', 'urlip')
        url1=urlip+parser.get('reports', 'url1')
        url2=urlip+parser.get('reports', 'url2')
        url0=urlip+parser.get('reports', 'url0')
        saledId=parser.get('reports', 'saleName')
        saleName=saledId
        revision=parser.get('reports', 'revision')
        regionId=parser.get('reports', 'regionId')
        datevalue=parser.get('reports','datevalue')
        reportLocation=parser.get('reports','reportLocation')
        print1(reportLocation)
        print1("salename::"+saleName)
        return;

def getDate():
        if (datevalue == 'todayDate'):
            todaytime=time.strftime("%d-%m-%Y")
        else:
            todaytime =datevalue
        return todaytime;



def getReportLocation():
    global reportLocation
    if (reportLocation.find('Desktop')!=-1):
        reportLocation=os.path.join(os.path.expanduser("~"), "Desktop")
    reportLocation=reportLocation+"\\report_"+saleName+"_"+regionId+"_"+str(getDate())+"_"+str(time.strftime("%H-%M-%S"))+"_"+".xml";
    print1("reportloc:: "+reportLocation)
    return 
    

def getFileName(): 
        getReportLocation()
        

def writeToFile(xmlValue):
    
    getReportLocation()
    print(reportLocation)
    text_file = open(reportLocation,'w')
    text_file.write(xmlValue)
    text_file.close()
    return


def prepareHeadRequest():
        cookie = {'ASP.NET_SessionId': '17ab96bd8ffbe8ca58a78657a918558'}
        s.headers.update({'Upgrade-Insecure-Requests': '1'})
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'})
        return cookie

def getFullSchedule():
        global url1        
        url1=url1+"?"+"scheduleDate="+getDate()+'&sellerId='+saledId+'&revisionNumber='+revision+'&regionId='+regionId+'&byDetails=0&isDrawer=0&isBuyer=0'
        #print('this is >>>>>>>>>>')
        print1(url1)
        print('this is >>>>>>>>>>')
        return url1

def getUtilUrl():
        global url0
        url0=url0+"?regionId="+regionId
        print1(url0)
        return url0
    
        
#url2 ='http://103.7.130.121/WBES/Report/GetDeclarationReport?regionId=2&date=23-09-2016&revision=27&utilId=f9b9e90c-1380-4eb1-bb00-8a0ea85f059c&isBuyer=0&byOnBar=0'
#url1 = 'http://103.7.130.121/WBES/ReportFullSchedule/GetFullInjSummary?scheduleDate=21-09-2016&sellerId=f9b9e90c-1380-4eb1-bb00-8a0ea85f059c&revisionNumber=62&regionId=2&byDetails=0&isDrawer=0&isBuyer=0'

def getGetDeclarationUrl():
        global url2
        
        url2=url2+"?"+"date="+getDate()+'&utilId='+saledId+'&revision='+revision+'&regionId='+regionId+'&byDetails=0&isDrawer=0&isBuyer=0&byOnBar=0'

        #url2=url2+'?regionId='+regionId+'&date='+getDate()+'&revision='+27+'&utilId='+saledId+'&isBuyer=0&byOnBar=0''
        print1(url2)
        return url2
    
def print1(strva):
    d=str(time.strftime("%d-%m-%Y"))
    t=str(time.strftime("%H-%M-%S"))
    logging.info(d+"::"+t+":>>    "+strva)
    print(d+"::"+t+":>>    "+strva)    
       
    
if __name__ == "__main__":
    print('started executing')
    log_path = os.path.dirname(os.path.realpath(__file__))+"\\"+'logfile.log'

    
    logging.basicConfig(filename=log_path, level=logging.INFO)
    try:

        print1('stated'+log_path)
    
        readProperties()
        print1('Time'+getDate()+str(time.strftime("%H-%M-%S")))
        cookie=prepareHeadRequest()
        
        print1(url1)
        print1(url2)
        
        r0 = s.get(getUtilUrl(),cookies=cookie)
        saledId=response0(r0.text)
        print1("success1:"+ url0)
        r1 = s.get(getFullSchedule(), cookies=cookie)
        txt1=response1(r1.text)
        xml1=xmloutput(txt1,'SG')
        print1("sucess2:"+url1)
        r2=s.get(getGetDeclarationUrl(),cookies=cookie)
        txt2=response2(r2.text)
        xml2=xmloutput(txt2,'DC')
        print1("sucess3:"+url2)
        
        
        xml=xml1+'\n'+ xml2
        print1(xml)
        writeToFile(xml)
        print1('Finished')
        
    except Exception as e:
        print1("error Oops try again !")
        print("error dOops  try again !")       
        print(e,sys.exc_info()[0])
        
        logging.exception(e)
        errrova=sys.exc_info()[0]
        print1("error Oops try again !")
        print("error dOops  try again***************************** !")
        print("********************************************************error dOops!")
        
    print('finished executing')    