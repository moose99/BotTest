'''
Created on Nov 22, 2017

@author: moose-home
'''
#!/bin/env python2.7
# -*- coding: utf-8 -*-
 
import requests
import time
import json
from bs4 import BeautifulSoup
import datetime
import adidasProfiles
import threading
 
#############################################
##             LOAD PROFILES               ##
#############################################
 
profiles = {'AidanSZN':adidasProfiles.aidanszn,'Buyansellkickz':adidasProfiles.buyandsellkickz}
 
#############################################
##            GLOBAL FUNCTIONS             ##
#############################################
 
def printTime():
    return str(datetime.datetime.now())
 
def statusTime(int):
    return printTime()+': Bot ('+str(int)+') '
 
def getValue(data,content):
    temp = content
    for idk in str(temp).split('<input'):
        if 'name="'+str(data) in str(idk):
            idk = idk.replace('name','')
            idk = idk.replace('type','')
            idk = idk.replace('value','')
            idk = idk.replace('>','')
            idk = idk.replace('\n','')
            idk = idk.split('=')
            dog = idk[3]
            return str(dog.replace('"',''))
 
def getCardType(cardnumber):
    firstDigit = str(cardnumber)[0]
    if firstDigit == '4':
        return '001'
    elif firstDigit == '5':
        return '002'
    elif firstDigit == '3':
        return '003'
    elif firstDigit == '6':
        return '004'
 
 
#############################################
##            GLOBAL VARIABLES             ##
#############################################
global proxyFile
proxyFile = ['http://173.246.189.212:4342', 'http://173.246.189.213:4343', 'http://173.246.189.214:4344', 'http://173.246.189.215:4345', 'http://173.246.189.216:4346', 'http://173.246.189.217:4347', 'http://173.246.189.218:4348', 'http://173.246.189.219:4349', 'http://173.246.189.22:4152', 'http://173.246.189.220:4350', 'http://173.246.189.221:4351', 'http://173.246.189.222:4352', 'http://173.246.189.223:4353', 'http://173.246.189.224:4354', 'http://173.246.189.225:4355', 'http://173.246.189.226:4356', 'http://173.246.189.227:4357', 'http://173.246.189.228:4358', 'http://173.246.189.229:4359', 'http://173.246.189.23:4153', 'http://173.246.189.230:4360', 'http://173.246.189.231:4361', 'http://173.246.189.232:4362', 'http://173.246.189.233:4363', 'http://173.246.189.234:4364', 'http://173.246.189.235:4365', 'http://173.246.189.236:4366', 'http://173.246.189.237:4367', 'http://173.246.189.238:4368', 'http://173.246.189.239:4369', 'http://173.246.189.24:4154', 'http://173.246.189.240:4370', 'http://173.246.189.241:4371', 'http://173.246.189.242:4372', 'http://173.246.189.243:4373', 'http://173.246.189.244:4374', 'http://173.246.189.245:4375', 'http://173.246.189.246:4376', 'http://173.246.189.247:4377', 'http://173.246.189.248:4378', 'http://173.246.189.249:4379', 'http://173.246.189.25:4155', 'http://173.246.189.250:4380', 'http://173.246.189.251:4381', 'http://173.246.189.252:4382', 'http://173.246.189.253:4383', 'http://173.246.189.254:4384', 'http://173.246.189.26:4156', 'http://173.246.189.27:4157', 'http://173.246.189.28:4158', 'http://173.246.189.29:4159', 'http://173.246.189.3:4133', 'http://173.246.189.30:4160', 'http://173.246.189.31:4161', 'http://173.246.189.32:4162', 'http://173.246.189.33:4163', 'http://173.246.189.34:4164', 'http://173.246.189.35:4165', 'http://173.246.189.36:4166', 'http://173.246.189.37:4167', 'http://173.246.189.38:4168', 'http://173.246.189.39:4169', 'http://173.246.189.4:4134', 'http://173.246.189.40:4170', 'http://173.246.189.41:4171', 'http://173.246.189.42:4172', 'http://173.246.189.43:4173', 'http://173.246.189.44:4174', 'http://173.246.189.45:4175', 'http://173.246.189.46:4176', 'http://173.246.189.47:4177', 'http://173.246.189.48:4178', 'http://173.246.189.49:4179', 'http://173.246.189.5:4135', 'http://173.246.189.50:4180', 'http://173.246.189.51:4181', 'http://173.246.189.52:4182', 'http://173.246.189.53:4183', 'http://173.246.189.54:4184', 'http://173.246.189.55:4185', 'http://173.246.189.56:4186', 'http://173.246.189.57:4187', 'http://173.246.189.58:4188', 'http://173.246.189.59:4189', 'http://173.246.189.6:4136', 'http://173.246.189.60:4190', 'http://173.246.189.61:4191', 'http://173.246.189.62:4192', 'http://173.246.189.63:4193', 'http://173.246.189.64:4194', 'http://173.246.189.65:4195', 'http://173.246.189.66:4196', 'http://173.246.189.67:4197', 'http://173.246.189.68:4198', 'http://173.246.189.69:4199', 'http://173.246.189.7:4137', 'http://173.246.189.70:4200', 'http://173.246.189.71:4201', 'http://173.246.189.72:4202', 'http://173.246.189.73:4203', 'http://173.246.189.74:4204', 'http://173.246.189.75:4205', 'http://173.246.189.76:4206', 'http://173.246.189.77:4207', 'http://173.246.189.78:4208', 'http://173.246.189.79:4209', 'http://173.246.189.8:4138', 'http://173.246.189.80:4210', 'http://173.246.189.81:4211', 'http://173.246.189.82:4212', 'http://173.246.189.83:4213', 'http://173.246.189.84:4214', 'http://173.246.189.85:4215', 'http://173.246.189.86:4216', 'http://173.246.189.87:4217', 'http://173.246.189.88:4218', 'http://173.246.189.89:4219', 'http://173.246.189.9:4139', 'http://173.246.189.90:4220', 'http://173.246.189.91:4221', 'http://173.246.189.92:4222', 'http://173.246.189.93:4223', 'http://173.246.189.94:4224', 'http://173.246.189.95:4225', 'http://173.246.189.96:4226', 'http://173.246.189.97:4227', 'http://173.246.189.98:4228', 'http://173.246.189.99:4229']
 
global i
i = 0
 
global sizes
sizes = {
    '9K':'330','4':'530','4.5':'540','5':'550','5.5':'560','6':'570','6.5':'580','7':'590','7.5':'600','8':'610','8.5':'620','9':'630',
    '9.5':'640','10':'650','10.5':'660','11':'670','11.5':'680','12':'690','12.5':'700','13':'710','13.5':'720','14':'730','15':'750',
    '16':'770','17':'790','18':'810'
}
 
global clientID
clientID = '4d8e6ee8-3654-4c89-8a18-1473c459b9a9'
 
#############################################
##              DEFINE CLASS               ##
#############################################
 
class AdidasBot(threading.Thread):
    def __init__(self,username,password,PID,size,profile):
        threading.Thread.__init__(self)
        self.startTime = datetime.datetime.now()
        global i
        http_proxy = proxyFile[i]
        self.index = i+1
        i = i + 1
        print statusTime(self.index)+'Initializing session...'
        self.proxy = {'http': http_proxy}
        self.profile = profiles[profile]
        self.session = requests.session()
        self.session.cookies.clear()
        self.username = str(username)
        self.password = str(password)
        self.PID = str(PID)
        self.size = str(size)
 
    def login(self):
        print statusTime(self.index) + 'Attempting login...'
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'cp.adidas.com',
            'Origin':'https://cp.adidas.com',
            'Referer':'https://cp.adidas.com/web/eCom/en_US/loadsignin?target=account',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        payload = {
            'username':self.username,
            'password':self.password,
            'signinSubmit':'Sign in',
            'IdpAdapterId':'adidasIdP10',
            'SpSessionAuthnAdapterId':'https://cp.adidas.com/web/',
            'PartnerSpId':'sp:demandware',
            'remembermeParam':'',
            'validator_id':'adieComDWus',
            'TargetResource':'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MyAccount-ResumeLogin?target=account&target=account',
            'InErrorResource':'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/null',
            'loginUrl':'https://cp.adidas.com/web/eCom/en_US/loadsignin',
            'cd':'eCom|en_US|cp.adidas.com|null',
            'app':'eCom',
            'locale':'en_US',
            'domain':'cp.adidas.com',
            'email':'',
            'pfRedirectBaseURL_test':'https://cp.adidas.com',
            'pfStartSSOURL_test':'https://cp.adidas.com/idp/startSSO.ping',
            'resumeURL_test':'',
            'FromFinishRegistraion':''
            # 'CSRFToken':'81f57a1f-f105-477e-813b-f955ad398f34'
        }
 
        url = 'https://cp.adidas.com/idp/startSSO.ping'
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        #print res.status_code
        #print res.content
        content = BeautifulSoup(res.content,"html.parser")
        idk = str(content.find_all('script')[0])
        idk = idk.replace('<script>','')
        idk = idk.replace('/*<![CDATA[*/','')
        idk = idk.replace('var','')
        idk = idk.replace('resURL','')
        idk = idk.replace('=','')
        idk = idk.replace("'",'')
        idk = idk.replace(' ','')
        idk = idk.split(';')
        reqUrl = idk[0].replace('\n','')
        resume = idk[0].replace('\n','').replace('https://cp.adidas.com','')
 
        query = {
            'resume':resume,
            'cd':'eCom|en_US|cp.adidas.com|null'
        }
 
        url = 'https://cp.adidas.com/web/ssoCookieCreate'
        res = self.session.get(url,params=query,headers=headers,proxies=self.proxy)
        # print res.status_code
        # print res.content
        # print res.url
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Host':'cp.adidas.com',
            'Referer':res.url,
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
 
        url = reqUrl
        res = self.session.get(url,headers=headers,proxies=self.proxy)
        # print res.status_code
        content = BeautifulSoup(res.content,"html.parser")
        content = content.find_all('input')[0]
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'cp.adidas.com',
            'Origin':'https://cp.adidas.com',
            'Referer':reqUrl,
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        payload = {
            'SAMLResponse':getValue('SAMLResponse',content),
            'RelayState':getValue('RelayState',content)
        }
        url = 'https://cp.adidas.com/sp/ACS.saml2'
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        # print res.status_code
        content = BeautifulSoup(res.content,"html.parser")
        content = content.find_all('input')[0]
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.adidas.com',
            'Origin':'https://cp.adidas.com',
            'Referer':'https://cp.adidas.com/sp/ACS.saml2',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
 
        payload = {
            'TargetResource':'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MyAccount-ResumeLogin?target=account&target=account',
            'REF':getValue('REF',content).replace('<noscript','')
        }
 
        url = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/MyAccount-ResumeLogin'
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        # print res.status_code
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.adidas.com',
            'Referer':'https://www.adidas.com/us/myaccount-create-or-login',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        query = {'fromlogin':'true'}
        url = 'https://www.adidas.com/us/myaccount-show'
        res = self.session.get(url,headers=headers,params=query,proxies=self.proxy)
        # print res.status_code
        content = BeautifulSoup(res.content,"html.parser")
        content = content.find_all('a')[0]
        accountName = str(content.get('title')).replace('My','').replace('Account','').lstrip(' ')
        endTime = datetime.datetime.now()
        print statusTime(self.index) + 'Login Successful for '+accountName+'...'
 
    def addToCart(self):
        url = 'http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'
        print statusTime(self.index)+'Injecting replacement product id:',self.PID
        headers={
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.adidas.com',
            'Origin':'http://www.adidas.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
 
        # Change pid key's value with 3 digit size code
        # 670 equates to size 11US
        payload={
            'layer':'Add To Bag overlay',
            'pid':self.PID+'_'+sizes[self.size],
            'Quantity':'1',
            #'g-recaptcha-response':new_token_value,
            'masterPid':self.PID,
            'ajax':'true'
        }
        query = {
            'clientId':clientID
        }
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy,params=query)
        while str(res.status_code) != '200':
            res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy,params=query)
            time.sleep(2)
        response = res.content
        while 'Successfully added to bag' not in response:
            response = json.loads(response)
            print statusTime(self.index)+str(response['error'])+' Add to cart unsuccessful, trying again...'
            time.sleep(1)
            res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy,params=query)
            response = res.content
        print statusTime(self.index)+'Add to cart successful!!!'
    def hypeAddToCart(self):
        captcha = str(raw_input('Enter valid captcha token: '))
        headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.adidas.com',
            'Origin':'http://www.adidas.com',
            'Referer':'http://www.adidas.com/yeezy',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
        query = {
            'clientId':clientID
        }
        payload = {
            'g-recaptcha-response':captcha,
            'pid':self.PID+'_'+sizes[self.size],
            'Quantity':'1',
            'request':'ajax',
            'responseformat':'json',
            'x-PrdRtt':captcha
        }
        url = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'
        res = self.session.post(url,params=query,data=payload,headers=headers)
        print res.content
        print res.status_code
 
    def checkCart(self):
        headers={
                'Accept':'*/*',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.8',
                'Connection':'keep-alive',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':'www.adidas.com',
                'Origin':'http://www.adidas.com',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                'X-Requested-With':'XMLHttpRequest'
            }
        url = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show'
        res = self.session.get(url,headers=headers,proxies=self.proxy)
        content = BeautifulSoup(res.content,"html.parser")
        # print content
        qty = str(content.find_all('div')[209].text).replace('\n','').replace(' ','').replace('product','').replace(' ','')
        if int(qty) < 1:
            print statusTime(self.index) + 'Cart empty... Reattempting ATC'
 
    def enterBillingShipping(self):
        print statusTime(self.index)+'Enter Billing/Shipping info...'
        headers={
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.adidas.com',
            'Origin':'http://www.adidas.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        }
        url = 'https://www.adidas.com/us/delivery-start'
        res = self.session.get(url,headers = headers,proxies=self.proxy)
        content = BeautifulSoup(res.content,"html.parser")
        # print res.content
        secureKey =  str(content.find_all('input')[17].get('value'))
        # dwcont = str(content.find_all('form')[0].get('action')).lstrip('https://www.adidas.com/us/delivery-start?dwcont=')
        # print secureKey
 
        url = str(content.find_all('form')[0].get('action'))
        # print url
        payload = {
            'dwfrm_delivery_shippingOriginalAddress':'false',
            'dwfrm_delivery_shippingSuggestedAddress':'false',
            'dwfrm_delivery_singleshipping_shippingAddress_isedited':'false',
            'dwfrm_delivery_singleshipping_shippingAddress_addressFields_firstName':self.profile['shipping_firstName'],
            'dwfrm_delivery_singleshipping_shippingAddress_addressFields_lastName':self.profile['shipping_lastName'],
            'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address1':self.profile['shipping_address1'],
            'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address2':self.profile['shipping_address2'],
            'dwfrm_delivery_singleshipping_shippingAddress_addressFields_city':self.profile['shipping_city'],
            'dwfrm_delivery_singleshipping_shippingAddress_addressFields_countyProvince':self.profile['shipping_countyProvince'],
            'state':self.profile['shipping_state'],
            'dwfrm_delivery_singleshipping_shippingAddress_addressFields_zip':self.profile['shipping_zip'],
            'dwfrm_delivery_singleshipping_shippingAddress_addressFields_phone':self.profile['shipping_phone'],
            'dwfrm_delivery_securekey':secureKey,
            'dwfrm_delivery_billingOriginalAddress':'false',
            'dwfrm_delivery_billingSuggestedAddress':'false',
            'dwfrm_delivery_billing_billingAddress_isedited':'false',
            'dwfrm_delivery_billing_billingAddress_addressFields_country':self.profile['billing_country'],
            'dwfrm_delivery_billing_billingAddress_addressFields_firstName':self.profile['billing_firstName'],
            'dwfrm_delivery_billing_billingAddress_addressFields_lastName':self.profile['billing_lastName'],
            'dwfrm_delivery_billing_billingAddress_addressFields_address1':self.profile['billing_address1'],
            'dwfrm_delivery_billing_billingAddress_addressFields_address2':self.profile['billing_address2'],
            'dwfrm_delivery_billing_billingAddress_addressFields_city':self.profile['billing_city'],
            'dwfrm_delivery_billing_billingAddress_addressFields_countyProvince':self.profile['billing_countyProvince'],
            'state':self.profile['billing_countyProvince'],
            'dwfrm_delivery_billing_billingAddress_addressFields_zip':self.profile['billing_zip'],
            'dwfrm_delivery_billing_billingAddress_addressFields_phone':self.profile['billing_phone'],
            'dwfrm_delivery_singleshipping_shippingAddress_email_emailAddress':self.profile['emailAddress'],
            'signup_source':'shipping',
            'dwfrm_delivery_singleshipping_shippingAddress_ageConfirmation':'true',
            'shipping-group-0':'2ndDay',
            'dwfrm_cart_shippingMethodID_0':'2ndDay',
            'shippingMethodType_0':'inline',
            'dwfrm_cart_selectShippingMethod':'ShippingMethodID',
            'referer':'Cart-Show',
            'dwfrm_delivery_singleshipping_shippingAddress_agreeForSubscription':'true',
            'dwfrm_delivery_savedelivery':'Review and Pay',
            'format':'ajax'
        }
 
        headers={
            'Accept':'text/html, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.adidas.com',
            'Origin':'http://www.adidas.com',
            'Referer':'https://www.adidas.com/us/delivery-start',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
 
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        while str(res.status_code) != '200':
            print statusTime(self.index) + 'Entering Billing/Shipping info failed... Reattempting...'
            res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
            time.sleep(1)
        # print res.status_code
        # print res.content
        print statusTime(self.index) + 'Entering Billing/Shipping info successful...'
 
 
    def enterPayment(self):
        print statusTime(self.index) + 'Entering Payment info...'
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            # 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.adidas.com',
            # 'Origin':'http://www.adidas.com',
            'Referer':'https://www.adidas.com/us/delivery-start',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            # 'X-Requested-With':'XMLHttpRequest'
        }
        url = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start'
        res = self.session.get(url,headers=headers,proxies=self.proxy)
        content = BeautifulSoup(res.content,"html.parser")
        url = content.find_all('form')[2].get('action')
        # print content
        # print content.find_all('input')
        paymentSecureKey = content.find_all('input')[11].get('value')
        # print url
        # print paymentSecureKey
        # print 'PASSED ERROR'
 
        headers={
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Length':'2038',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.adidas.com',
            'Origin':'http://www.adidas.com',
            'Referer':'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }
 
        payload = {
            'dwfrm_payment_creditCard_type':getCardType(self.profile['creditCard_number']),
            'dwfrm_payment_creditCard_owner':self.profile['creditCard_owner'],
            'dwfrm_payment_creditCard_number':self.profile['creditCard_number'],
            'dwfrm_payment_creditCard_month':self.profile['creditCard_month'],
            'dwfrm_payment_creditCard_year':self.profile['creditCard_year'],
            'dwfrm_payment_creditCard_cvn':self.profile['creditCard_cvn'],
            'dwfrm_payment_securekey':paymentSecureKey,
            'dwfrm_payment_signcreditcardfields':'sign'
        }
 
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        # print res.status_code
        content = json.loads(res.content)
        # print content['fieldsToSubmit']
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'2769',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'secureacceptance.cybersource.com',
            'Origin':'https://www.adidas.com',
            'Referer':'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.3'
        }
 
        content = content['fieldsToSubmit']
 
        payload = {
            'access_key':content['access_key'],
            'amount':content['amount'],
            'bill_to_address_city':content['bill_to_address_city'],
            'bill_to_address_country':content['bill_to_address_country'],
            'bill_to_address_line1':content['bill_to_address_line1'],
            'bill_to_email':content['bill_to_email'],
            'bill_to_forename':content['bill_to_forename'],
            'bill_to_surname':content['bill_to_surname'],
            'card_expiry_date':content['card_expiry_date'],
            'card_type':content['card_type'],
            'currency':content['currency'],
            'locale':content['locale'],
            'payment_method':content['payment_method'],
            'profile_id':content['profile_id'],
            'reference_number':content['reference_number'],
            'signed_date_time':content['signed_date_time'],
            'transaction_uuid':content['transaction_uuid'],
            'transaction_type':content['transaction_type'],
            'unsigned_field_names':content['unsigned_field_names'],
            'override_custom_receipt_page':content['override_custom_receipt_page'],
            'bill_to_phone':content['bill_to_phone'],
            'bill_to_address_state':content['bill_to_address_state'],
            'bill_to_address_postal_code':content['bill_to_address_postal_code'],
            'device_fingerprint_id':content['device_fingerprint_id'],
            'customer_ip_address':content['customer_ip_address'],
            'merchant_defined_data1':content['merchant_defined_data1'],
            'merchant_defined_data2':content['merchant_defined_data2'],
            'merchant_defined_data4':content['merchant_defined_data4'],
            'merchant_defined_data6':content['merchant_defined_data6'],
            'merchant_defined_data7':content['merchant_defined_data7'],
            'ship_to_address_city':content['ship_to_address_city'],
            'ship_to_address_country':content['ship_to_address_country'],
            'ship_to_address_line1':content['ship_to_address_line1'],
            'ship_to_address_line2':content['ship_to_address_line2'],
            'ship_to_address_postal_code':content['ship_to_address_postal_code'],
            'ship_to_address_state':content['ship_to_address_state'],
            'ship_to_forename':content['ship_to_forename'],
            'ship_to_phone':content['ship_to_phone'],
            'ship_to_surname':content['ship_to_surname'],
            'item_0_quantity':content['item_0_quantity'],
            'item_0_unit_price':content['item_0_unit_price'],
            'item_0_code':content['item_0_code'],
            'item_0_name':content['item_0_name'],
            'item_0_sku':content['item_0_sku'],
            'item_0_tax_amount':content['item_0_tax_amount'],
            'item_1_quantity':content['item_1_quantity'],
            'item_1_unit_price':content['item_1_unit_price'],
            'item_1_code':content['item_1_code'],
            'item_1_name':content['item_1_name'],
            'item_1_sku':content['item_1_sku'],
            'item_1_tax_amount':content['item_1_tax_amount'],
            'tax_amount':content['tax_amount'],
            'line_item_count':content['line_item_count'],
            'signed_field_names':content['signed_field_names'],
            'signature':content['signature'],
            'card_cvn':self.profile['creditCard_cvn'],
            'card_number':self.profile['creditCard_number']
        }
 
        url = 'https://secureacceptance.cybersource.com/silent/pay'
 
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        # print res.status_code
        content = BeautifulSoup(res.content,"html.parser")
 
        url = 'https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/redirect'
 
        # print content.find_all('input')
 
        payload = {
            'utf8':'✓',
            'authenticity_token':content.find_all('input')[1].get('value'),
            'PaReq':content.find_all('input')[2].get('value'),
            'TermUrl':content.find_all('input')[3].get('value'),
            'MD':content.find_all('input')[4].get('value')
        }
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'0eaf.cardinalcommerce.com',
            'Origin':'https://secureacceptance.cybersource.com',
            'Referer':'https://secureacceptance.cybersource.com/silent/pay',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
 
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        # print res.status_code
        content = BeautifulSoup(res.content,"html.parser")
 
        url = content.find_all('form')[0].get('action')
 
        payload = {
            'PaReq':content.find_all('input')[0].get('value'),
            'TermUrl':content.find_all('input')[1].get('value'),
            'MD':content.find_all('input')[2].get('value')
        }
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'cap.attempts.securecode.com',
            'Origin':'https://0eaf.cardinalcommerce.com',
            'Referer':'https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/redirect',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
 
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        # print res.status_code
        content = BeautifulSoup(res.content,"html.parser")
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'0eaf.cardinalcommerce.com',
            'Origin':'https://cap.attempts.securecode.com',
            'Referer':url,
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
 
        # print content.find_all('form')[0].find_all('input')
        newContent = BeautifulSoup("<html>\n"+str(content.find_all('input')[2])+"\n</html>","html.parser")
 
        payload = {
            'PaRes':getValue('PaRes',newContent),
            'MD':getValue('MD',newContent),
            'PaReq':getValue('PaReq',newContent),
            'ABSlog':'GPP',
            'deviceDNA':'',
            'executionTime':'',
            'dnaError':'',
            'mesc':'',
            'mescIterationCount':'0',
            'desc':'',
            'isDNADone':'false',
            'arcotFlashCookie':''
        }
 
        url = 'https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/term'
 
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        # print res.status_code
        content = BeautifulSoup(res.content,"html.parser")
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'secureacceptance.cybersource.com',
            'Origin':'https://0eaf.cardinalcommerce.com',
            'Referer':'https://0eaf.cardinalcommerce.com/EAFService/jsp/v1/term',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
 
        payload = {
            'PaRes':content.find_all('input')[0].get('value'),
            'MD':content.find_all('input')[1].get('value')
        }
 
        url = 'https://secureacceptance.cybersource.com/silent/complete_payer_authentication'
 
        res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
        # print res.status_code
        content = BeautifulSoup(res.content,"html.parser")
        # print content
        content = content.find_all('input')
 
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.adidas.com',
            'Origin':'https://secureacceptance.cybersource.com',
            'Referer':'https://secureacceptance.cybersource.com/silent/complete_payer_authentication',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        payload = {
            'utf8':'✓',
            'auth_cv_result':content[1].get('value'),
            'req_locale':content[2].get('value'),
            'req_tax_amount':content[5].get('value'),
            'payer_authentication_enroll_veres_enrolled':content[59].get('value'),
            'req_item_0_sku':content[6].get('value'),
            'req_item_0_code':content[60].get('value'),
            'req_bill_to_surname':content[7].get('value'),
            'req_item_0_unit_price':content[61].get('value'),
            'payer_authentication_proof_xml':content[62].get('value'),
            'req_item_0_quantity':content[8].get('value'),
            'req_item_1_name':content[9].get('value'),
            'req_card_expiry_date':content[63].get('value'),
            'req_bill_to_phone':content[66].get('value'),
            'req_merchant_defined_data6':content[11].get('value'),
            'req_merchant_defined_data7':content[13].get('value'),
            'auth_response':content[67].get('value'),
            'req_payment_method':content[68].get('value'),
            'decision_early_return_code':content[15].get('value'),
            'req_item_1_sku':content[69].get('value'),
            'transaction_id':content[16].get('value'),
            'req_card_type':content[70].get('value'),
            'payer_authentication_pares_status':content[17].get('value'),
            'req_item_1_code':content[71].get('value'),
            'req_override_custom_receipt_page':content[19].get('value'),
            'req_merchant_defined_data1':content[20].get('value'),
            'req_merchant_defined_data2':content[21].get('value'),
            'req_merchant_defined_data4':content[22].get('value'),
            'auth_avs_code':content[73].get('value'),
            'req_ship_to_address_postal_code':content[24].get('value'),
            'req_bill_to_address_country':content[43].get('value'),
            'req_ship_to_address_state':content[26].get('value'),
            'auth_cv_result_raw':content[27].get('value'),
            'req_profile_id':content[78].get('value'),
            'req_ship_to_address_city':content[28].get('value'),
            'payer_authentication_uad':content[29].get('value'),
            'signed_date_time':content[80].get('value'),
            'req_bill_to_address_line1':content[32].get('value'),
            'req_ship_to_surname':content[81].get('value'),
            'payer_authentication_validate_e_commerce_indicator':content[82].get('value'),
            'req_card_number':content[33].get('value'),
            'req_ship_to_forename':content[84].get('value'),
            'signature':content[34].get('value'),
            'req_bill_to_address_city':content[88].get('value'),
            'req_bill_to_address_postal_code':content[89].get('value'),
            'reason_code':content[91].get('value'),
            'req_bill_to_forename':content[92].get('value'),
            'req_item_1_unit_price':content[36].get('value'),
            'request_token':content[38].get('value'),
            'req_device_fingerprint_id':content[93].get('value'),
            'req_amount':content[39].get('value'),
            'req_bill_to_email':content[95].get('value'),
            'payer_authentication_reason_code':content[40].get('value'),
            'auth_avs_code_raw':content[96].get('value'),
            'decision_velocity_info':content[41].get('value'),
            'req_currency':content[97].get('value'),
            'decision':content[42].get('value'),
            'req_ship_to_address_country':content[43].get('value'),
            'req_item_0_tax_amount':content[98].get('value'),
            'req_ship_to_phone':content[45].get('value'),
            'req_customer_ip_address':content[46].get('value'),
            'message':content[99].get('value'),
            'signed_field_names':content[47].get('value'),
            'req_transaction_uuid':content[100].get('value'),
            'payer_authentication_eci':content[49].get('value'),
            'req_transaction_type':content[51].get('value'),
            'req_item_1_quantity':content[103].get('value'),
            'payer_authentication_xid':content[52].get('value'),
            'req_access_key':content[104].get('value'),
            'decision_early_reason_code':content[108].get('value'),
            'req_item_0_name':content[54].get('value'),
            'req_reference_number':content[55].get('value'),
            'payer_authentication_validate_result':content[106].get('value'),
            'req_bill_to_address_state':content[107].get('value'),
            'req_ship_to_address_line2':content[108].get('value'),
            'req_ship_to_address_line1':content[109].get('value'),
            'decision_early_rcode':content[110].get('value'),
            'req_line_item_count':content[56].get('value'),
            'req_item_1_tax_amount':content[111].get('value'),
            'payer_authentication_uci':content[57].get('value'),
        }
 
        url = content[19].get('value')
        res = self.session.post(url,data=payload,headers=headers)
        while str(res.status_code) != '200':
            print statusTime(self.index) + 'Entering Payment info failed...'
            res = self.session.post(url,data=payload,headers=headers,proxies=self.proxy)
            time.sleep(1)
        #print res.status_code
        print statusTime(self.index) + 'Checkout successful!'
 
    def run(self):
        while True:
            try:
                self.login()
                break
            except:
                print statusTime(self.index)+'Login failed...'
                time.sleep(1)
        # self.hypeAddToCart()
        # self.checkCart()
        while True:
            try:
                self.enterBillingShipping()
                break
            except:
                print statusTime(self.index)+'Entering Billing/Shipping info failed...'
                time.sleep(1)
        # self.enterPayment()
        while True:
            try:
                self.enterPayment()
                break
            except:
                print statusTime(self.index)+'Entering Payment info failed...'
                time.sleep(1)
        endTime = datetime.datetime.now()-self.startTime
        print statusTime(self.index)+'Total execution time: '+str(endTime)
 
 
# profile = str(raw_input('Enter profile for checkout: '))
# while profile != '\n':
#     bot = AdidasBot('BB3899','12',profile)
#     bot.run()
#     profile = str(raw_input('Enter profile for checkout: '))
# print getCardType(profiles['Cary']['creditCard_number'])
 
# bot = AdidasBot('cary.mcewan@gmail.com','Bbbarhsffy.1995','BB3899','12','bsk')
# bot2 = AdidasBot('BB3899','12','Cary')
# bot.start()
# bot2.start()
 
#############################################
##               INSTRUCTIONS              ##
#############################################
 
# 1. First make sure you have entered your accounts into your adidasProfiles.py file.
# 2. Add all of the profiles on line 16. ie profiles = {'Buyandsellkickz':adidasProfiles.buyandsellkickz, 'AidanSZN':adidasProfiles.aidanszn}
# 3. Also, make sure you have added all your proxies, with the format provided above.
# 3. Once you have loaded your profiles and proxies, running the script is really easy. Since we won't be adding to cart in this script,
    # it doesn't matter what you enter for the PID or the size. You can enter whatever you want.
# 4. To run, simply type the following in the file:
 
# bot = AdidasBot('email','password','BB3899','12','profileName')
# bot.start()
 
# Here's an example:
# bot = AdidasBot('buyandsellkickz@gmail.com','sneakers123','BB3899','12','Buyandsellkickz')
# bot.start()
 
# To run multiple accounts,simply create another bot with a different name. ie. bot2
# Here's an example of running two accounts:
 
# bot = AdidasBot('buyandsellkickz@gmail.com','sneakers123','BB3899','12','Buyandsellkickz')
# bot2 = AdidasBot('aidanSZN@gmail.com','sneakers123','BB3899','12','AidanSZN')
# bot.start()
# bot2.start()
 
# You can run as many accounts as you want like this. Just note that Entering Billing/Shipping info will show as failed
# until you have actually carted.