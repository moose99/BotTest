'''
Created on Aug 27, 2017

@author: moose-home
'''

import requests
import bs4
import webbrowser
import threading
import json

#headers1 = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

# https://www.adidas.com/api/products/BY9587/availability?sitePath=us

session = None
cookies = None
base_url = 'https://www.adidas.com'
product_url = base_url + '/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'
headers1 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/52.0.2743.116 Safari/537.36',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Upgrade-Insecure-Requests': '1',
    'Referer': product_url,     # yes misspelled on purpose
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

#
# USER INFO
#
billing_address_1 = 'John Doe'
billing_address_2 = '123 Main St'
billing_apt_suite = ''
billing_city =      'schenectady'
billing_country = 'United States of America'
billing_country_abbrv = 'USA'
billing_state = 'schenectady'
billing_state_abbrv = 'NY'
billing_zip = '12345'
card_cvv = '982'
card_exp_month = '08'
card_exp_year = '21'
card_number = '1111222233334444'
card_type = 'Visa'
email = 'foo@gmail.com'
first_name = 'John'
last_name = 'Doe'
name_on_card = 'John Doe'
phone_number = '1234568910'
shipping_address_1 = 'John Doe'
shipping_address_2 = '123 Main St'
shipping_apt_suite = ''
shipping_city = 'schenectady'
shipping_country = 'United States of America'
shipping_country_abbrv = 'USA'
shipping_state = 'New York'
shipping_state_abbrv = 'NY'
shipping_zip = '12345'
             
# returns a list of available sizes
# {'sku': 'BY9587_530', 'availability': 0, 'availability_status': 'NOT_AVAILABLE', 'size': '4'}
# {'sku': 'BY9587_570', 'availability': 15, 'availability_status': 'IN_STOCK', 'size': '6'}             
def GetSizeList(response):
    # convert response to json
    print("GetSizeList")
    jsonData = json.loads(response.text)
    print(jsonData)
    
    if (jsonData['availability_status'] != 'IN_STOCK'):
        print("NOT IN STOCK")
        return [];
    
    sizeList = jsonData['variation_list']
    return sizeList
        
# returns sku (BY9587_570) or None
def FindItem(model, size, quantity):
    print('FindItem')
    url = "https://www.adidas.com/api/products/" + str(model) + "/availability?sitePath=us"
    print(url)
    response = requests.get(url, headers=headers1)
    sizeList = GetSizeList(response)
    if (sizeList == []):
        print("OUT OF STOCK")
        return None
    
    sku = None
    for entry in sizeList:
        if (entry['size'] == str(size) and int(entry['availability']) >= quantity and entry['availability_status']=='IN_STOCK' ):
            sku = entry['sku']
            break
    return sku

#
# https://www.adidas.com/api/cart_items?sitePath=us
#===============================================================================
# JSON payload
# product_id    BY9587
# quantity    1
# product_variation_sku    BY9587_640
# size    9.5
# recipe    null
# invalidFields    []
# isValidating    false
# clientCaptchaResponse
#===============================================================================
def AddToCart(model, size, sku):
    global session
    global cookies

    print('AddToCart')
    payload = {
    'product_id' : model,
    'quantity' : str(quantity),
    'product_variation_sku' : sku,
    'size' : str(size),
    'recipe' : 'null',
    'invalidFields' : '[]',
    'isValidating' : 'false',
    'clientCaptchaResponse' : ''
    }
    print (payload)
    endpoint = 'https://www.adidas.com/api/cart_items?sitePath=us'
    session = requests.Session()    # START SESSION
    res    = session.get(endpoint, headers=headers1)
    # did this for first to get the cookies from the page, stored them with next line:
    cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))

    res = session.post(endpoint, json=payload, headers=headers1, timeout=15, cookies=cookies)
    print ('post result: ' + str(res.status_code))
#           print ('text: ' + res.text)
    if (res.status_code==200):
        res = session.get(endpoint, headers=headers1, cookies=cookies)
        print ('get result: ' + str(res.status_code))
        #           print ('text: ' + res.text)
        if (res.status_code==200):
            return True
        
    return False

def CheckOut():
    print('Checking out...')
    global session
    global cookies
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'Referer': product_url,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    
    endpoint = base_url + '/us/delivery-start';    # redirects to https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COShipping-Show
    
    # start at general delivery url, then bget redirected url
    response = session.get(endpoint, headers=headers1, cookies=cookies)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    endpoint = soup.find('div', {'class': 'cart_wrapper rbk_shadow_angle rbk_wrapper_checkout summary_wrapper'})['data-url']
    print("endpoint:" + endpoint)
    
    # now get securekey    
    response = session.get(endpoint, headers=headers1, cookies=cookies)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')   
    #delivery_key = soup.find('input', {'name': 'dwfrm_delivery_securekey'})['value']
    delivery_key = soup.find('input', {'name': 'dwfrm_shipping_securekey'})['value']
    print('securekey:' + delivery_key)
    
    # delivery details
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Origin': 'http://www.adidas.com',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.adidas.com/us/delivery-start'
    }
    payload = {
        'dwfrm_cart_selectShippingMethod': 'ShippingMethodID',
        'dwfrm_cart_shippingMethodID_0': 'Standard',
        'dwfrm_delivery_billingOriginalAddress': 'false',
        'dwfrm_delivery_billingSuggestedAddress': 'false',
        'dwfrm_delivery_billing_billingAddress_addressFields_address1': billing_address_1,
        'dwfrm_delivery_billing_billingAddress_addressFields_address2': billing_address_2,
        'dwfrm_delivery_billing_billingAddress_addressFields_city': billing_city,
        'dwfrm_delivery_billing_billingAddress_addressFields_country': billing_country_abbrv,
        'dwfrm_delivery_billing_billingAddress_addressFields_countyProvince': billing_state_abbrv,
        'dwfrm_delivery_billing_billingAddress_addressFields_firstName': first_name,
        'dwfrm_delivery_billing_billingAddress_addressFields_lastName': last_name,
        'dwfrm_delivery_billing_billingAddress_addressFields_phone': phone_number,
        'dwfrm_delivery_billing_billingAddress_addressFields_zip': billing_zip,
        'dwfrm_delivery_billing_billingAddress_isedited': 'false',
        'dwfrm_delivery_savedelivery': 'Review and Pay',
        'dwfrm_delivery_securekey': delivery_key,
        'dwfrm_delivery_shippingOriginalAddress': 'false',
        'dwfrm_delivery_shippingSuggestedAddress': 'false',
        'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address1': shipping_address_1,
        'dwfrm_delivery_singleshipping_shippingAddress_addressFields_address2': shipping_address_2,
        'dwfrm_delivery_singleshipping_shippingAddress_addressFields_city': shipping_city,
        'dwfrm_delivery_singleshipping_shippingAddress_addressFields_countyProvince': shipping_state_abbrv,
        'dwfrm_delivery_singleshipping_shippingAddress_addressFields_firstName': first_name,
        'dwfrm_delivery_singleshipping_shippingAddress_addressFields_lastName': last_name,
        'dwfrm_delivery_singleshipping_shippingAddress_addressFields_phone': phone_number,
        'dwfrm_delivery_singleshipping_shippingAddress_addressFields_zip': shipping_zip,
        'dwfrm_delivery_singleshipping_shippingAddress_ageConfirmation': 'true',
        'dwfrm_delivery_singleshipping_shippingAddress_agreeForSubscription': 'false',
        'dwfrm_delivery_singleshipping_shippingAddress_email_emailAddress': email,
        'dwfrm_delivery_singleshipping_shippingAddress_isedited': 'false',
        'format': 'ajax',
        'referer': 'Cart-Show',
        'shipping-group-0': 'Standard',
        'shippingMethodType_0': 'inline',
        'signup_source': 'shipping',
        'state': shipping_state + ','
    }

    response = session.post(endpoint, data=payload, headers=headers1, cookies=cookies)
    print ('delivery info result: ' + str(response.status_code))

    # review & pay
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://www.adidas.com',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start'
    }
    payload = {
        'dwfrm_payment_creditCard_cvn': card_cvv,
        'dwfrm_payment_creditCard_month': card_exp_month,
        'dwfrm_payment_creditCard_number': card_number,
        'dwfrm_payment_creditCard_owner': '{} {}'.format(first_name, last_name),
        'dwfrm_payment_creditCard_type': '001',  # visa
        'dwfrm_payment_creditCard_year': card_exp_year,
        'dwfrm_payment_securekey': delivery_key,
        'dwfrm_payment_signcreditcardfields': 'sign'
    }

    url = soup.find('form', {'id': 'dwfrm_delivery'})['action']
    print('CC url:' + url);
    response = session.post(url, data=payload, headers=headers1, cookies=cookies)
    print ('CC info result: ' + str(response.status_code))

    if response.status_code == 200:
        print('Check your email for confirmation!')
        return True
    
    return False
    
#===============================================================================
# MAIN ENTRY POINT
#===============================================================================

model = input('Enter Model Number (BY9587):')     # this is a string so it needs raw_input
if (model==''):
    model='BY9587'
    
size = input('Enter Size (8):')
if (size==''):
    size=8
    
quantity = input('Enter Quantity (1):')
if (quantity==''):
    quantity=1
    
sku = FindItem(model, size, quantity)
if (sku != None):
    buy = input('Item found.  Purchase (Y/N)? ')
    if (buy.upper() == 'Y'):
        if (AddToCart(model, size, sku) == True):
            if (CheckOut() == True):
                print('CheckOut succeeded')
            else:
                print('CheckOut failed')        

print("DONE")


            
#===============================================================================
# https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start/C51340681    
# 
# dwfrm_payment_creditCard_type:001
# dwfrm_payment_creditCard_owner:Mike Thomas
# dwfrm_payment_creditCard_month:08
# dwfrm_payment_creditCard_year:2021
# selectedPaymentMethodID:CREDIT_CARD
# dwfrm_payment_securekey:1623082865
# dwfrm_payment_signcreditcardfields:sign
#===============================================================================
            
#===============================================================================
# https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COShipping-Submit    
# this is the request payload...        
# dwfrm_shipping_securekey    1932263553
# dwfrm_shipping_selectedDeliveryMethodID_d0vdgxgzaqoz    shiptoaddress
# dwfrm_shipping_selectedShippingType_d0lahecgkyry    shiptoaddress
# dwfrm_shipping_shiptoaddress_shippingAddress_firstName_d0aemuvngbki    Mike
# dwfrm_shipping_shiptoaddress_shippingAddress_lastName_d0kpfcpczehz    Thomas
# dwfrm_shipping_shiptoaddress_shippingAddress_address1_d0bqgormpand    2100+Fiefdom+Rd
# dwfrm_shipping_shiptoaddress_shippingAddress_address2_d0mbyfpyhxyo    
# dwfrm_shipping_shiptoaddress_shippingAddress_city_d0kebwdfuern    Baltimore
# dwfrm_shipping_shiptoaddress_shippingAddress_countyProvince_d0ihaiggtlmh    MD
# dwfrm_shipping_shiptoaddress_shippingAddress_postalCode_d0whbsiltzok    21093
# dwfrm_shipping_shiptoaddress_shippingAddress_country_d0ryyutsvmbo    US
# dwfrm_shipping_shiptoaddress_shippingAddress_phone_d0iivcvypmmp    1123454891
# dwfrm_shipping_email_emailAddress_d0fxekyzcach    shazam@gmail.com
# dwfrm_shipping_shiptoaddress_shippingAddress_useAsBillingAddress_d0qrhwlzxuoa    true
# dwfrm_shipping_shiptoaddress_shippingAddress_ageConfirmation_d0kitbuwqtwq    true
# dwfrm_shipping_shiptoaddress_shippingDetails_selectedShippingOption_d0dmfxtintrn    eyJtZSI6IjAifQ==
# dwfrm_shipping_shiptoaddress_shippingDetails_selectedShippingSubOption_d0spessojmmn    
# shippingMethodType_0    inline
# dwfrm_cart_selectShippingMethod    ShippingMethodID
# dwfrm_cart_shippingMethodID_0    2ndDay
# referer    Cart-Show
# shipping-option-me    0
# dwfrm_shipping_submitshiptoaddress    Review+and+Pay
# dwfrm_shipping_shiptostore_search_country_d0lhhlbnkjdt    US
# dwfrm_shipping_shiptostore_search_maxdistance_d0zzkgnvltwq    50
# dwfrm_shipping_shiptostore_search_latitude_d0rzwfbtxkwq    
# dwfrm_shipping_shiptostore_search_longitude_d0pzqnnpthoo    
# dwfrm_shipping_shiptostore_search_country_d0rnqgxkstlv    US
# dwfrm_shipping_shiptostore_search_maxdistance_d0gvwmfjyebt    50
# dwfrm_shipping_shiptostore_search_latitude_d0tetpazcsmh    
# dwfrm_shipping_shiptostore_search_longitude_d0clklfsvojy    
# dwfrm_shipping_shiptostore_shippingDetails_selectedShippingMethod_d0ccfzjslnbl    
# dwfrm_shipping_shiptostore_shippingDetails_storeId_d0uktqdgxfwg    
# dwfrm_shipping_shiptopudo_shippingDetails_selectedShippingMethod_d0negeyxblhs    
# dwfrm_shipping_shiptopudo_shippingDetails_pudoId_d0bnqzbiyvhn
#===============================================================================
            

