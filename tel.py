# -*- coding: utf8 -*-
import requests
import time
from pyquery import PyQuery as pq


surl = "http://www.104.com.tw/jobbank/custjob/index.php?r=cust&j=44424a733c3e466f383a426b40463e2193131312c4a4e647109j52&jobsource=checkc"

binds = ["?",";","'","-","(",")","學校","有限公司","公司","股份","股"]

def search(session, key):
    for b in binds:
        key = key.replace(b, "");
    
    keyurl = 'http://www.104.com.tw/cust/list/index/?page=1&order=1&mode=s&jobsource=checkc&keyword=' + key
    result = session.get(keyurl)
    s = pq(result.text)
    link = s('.info').find('a').attr['href']

    return link

def getInfo(session, link):
    r = session.get(link)
    r.encoding='utf8'

    d = pq(r.text)
    Name = d('.comp_name').eq(0).text()
    Address = d('.intro').find('dd').eq(5).text()
    tel = d('.intro').find('dd').eq(6).find('img').attr['src']
    if tel != None:
        Telephone = tel[tel.index('Text')+5:]
    else:
        Telephone = ''
    
    Extension = d('.intro').find('dd').eq(6).text()

    return Name, Telephone, Extension, Address[:-3]
    

if __name__ == '__main__':
    try:
        res = []
        for keyword in open('data.txt', 'r'):   
            session = requests.session()
            link = search(session, keyword)
            print keyword
            if(link != None):
                #print link
                info = getInfo(session, link)

                Name = info[0]
                if unicode(keyword[:6],'utf8') not in Name:
                    print 'wrong'
                    info = '暫不提供','暫不提供','','暫不提供'

                
                print Name,'\n\n'
                
            else:
                print "Not Found!"
                info = '暫不提供','暫不提供','','暫不提供'
            res.append(info)

            print '______________________________________________________\n'
        print '##############'
        for r in res:
            Name, Telephone, Extension, Address = r
            print Telephone + Extension,'\t\t' ,Address, '\t', Name
        
            
    except Exception,e:
        print e
