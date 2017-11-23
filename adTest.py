'''
Created on Nov 23, 2017

@author: moose-home
'''

import requests
import bs4
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/52.0.2743.116 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',

    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def PrintDict(d):
    if (d != None):
        for i in d:
            print(str(i) + ' : ' + str(d[i]))
        
def CheckResponse(response, label):
    print(label)
    
    print('STATUS CODE:' + str(response.status_code))
#    print('cookies after:' + str(requests.utils.dict_from_cookiejar(session.cookies)))
    
    # Consider any status other than 2xx an error
    if not response.status_code // 100 == 2:
        print("ERROR: Unexpected response {}".format(response))
        print("REASON:" + response.reason)
    
    print('REQUEST headers:')
    PrintDict(response.request.headers)
    
    print('RESPONSE headers:')
    PrintDict(response.headers)
    
#    print('response cookies:' + str(response.cookies))
    print('HISTORY:' + str(response.history))
    
    try:
        PrintDict(response.json())
    except json.decoder.JSONDecodeError:
        print("No JSON response")
    
#
# MAIN
# product: https://www.adidas.com/us/nmd_r1-primeknit-shoes/BZ0223.html?pr=home_rr&slot=1
#

session = requests.Session()    # START SESSION

#
# Get
#
endpoint = 'https://www.adidas.com/api/cart_items?sitePath=us'
response = session.get(endpoint, headers=headers)
CheckResponse(response, '\nADDTOCART - GET')

#
# Post
#
payload = {
    'product_id' : 'BZ0223',
    'quantity' : '2',
    'product_variation_sku' : 'BZ0223_630',
    'size' : '9',
#    'recipe' : 'null',
    'invalidFields' : '[]',
    'isValidating' : 'false',
#    'clientCaptchaResponse' : ''
}
#print('content-length:' + payload.length)
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control' : 'no-cache',
    'Connection' : 'keep-alive',
#    'Content-Length' : '165',        # set by requests module
    'content-type': 'application/json',
    # 'Cookie' : ' '                  # set by requests module
    'Host' : 'www.adidas.com',
    'origin' : 'https://www.adidas.com',
    'Pragma' : 'no-cache',
    'Referer' : 'https://www.adidas.com/us/nmd_r1-primeknit-shoes/BZ0223.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/52.0.2743.116 Safari/537.36',
#    'DNT': '1',
#    'Upgrade-Insecure-Requests': '1',
}

params = {
    'sitePath' : 'us',
}

response = session.post(url=endpoint, params=params, json=payload, headers=headers)
CheckResponse(response, "\nADDTOCART - POST")

print('\nDONE')