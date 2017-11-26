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
# -------------- Get, ADD TO CART ---------------------
#
endpoint = 'https://www.adidas.com/api/cart_items?sitePath=us'
response = session.get(endpoint, headers=headers)
CheckResponse(response, '\nADDTOCART - GET')

#
# Post ADD TO CART
#
payload = {
    'product_id' : 'BZ0223',
    'quantity' : '2',
    'product_variation_sku' : 'BZ0223_630', # NOTE - GET THIS SKU USING CODE FROM ad1.py (GetSizeList / FindItem)
    'size' : '9',
#    'recipe' : 'null',        # don't set null fields
    'invalidFields' : '[]',
    'isValidating' : 'false',
#    'clientCaptchaResponse' : ''
}

headers['content-type'] = 'application/json'

response = session.post(endpoint, json=payload, headers=headers)
CheckResponse(response, "\nADDTOCART - POST")

#
# ------------------- CHECKOUT ---------------------
#

#
# GET DATA URL
#
endpoint = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show'
response = session.get(endpoint, headers=headers)
CheckResponse(response, '\nCHECKOUT - CART-SHOW')
soup = bs4.BeautifulSoup(response.text, 'html.parser')        
dataURL = soup.find('div', {'class': 'cart_wrapper rbk_shadow_angle rbk_wrapper_checkout summary_wrapper'})['data-url']
print("data-url:" + dataURL)

#
# POST to DATA URL
#
headers['Referer'] = dataURL
headers['Content-Type'] = 'application/x-www-form-urlencoded'  # NOT JSON, use data param not json
payload = {
    'dwfrm_cart_checkoutCart' : 'Checkout'
    }
response = session.post(dataURL, headers=headers, data=payload)
CheckResponse(response, '\nCHECKOUT - POST DATA_URL')

#
# CHECKOUT, GET, SHIPPING_SHOW
#    
endpoint = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COShipping-Show'
response = session.get(endpoint, headers=headers)
CheckResponse(response, '\nCHECKOUT - SHIPPING-SHOW')
soup = bs4.BeautifulSoup(response.text, 'html.parser')        
secureKey = soup.find('input', {'name': 'dwfrm_shipping_securekey'})['value']
print('Securekey:' + secureKey)

######################################################################################
# FROM HERE DOWN PROBABLY IS NOT CORRECT
######################################################################################

#
# CHECKOUT - POST PAYMENT to DATA URL
#
headers['Referer'] = 'https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COSummary-Start'
payload = {
'dwfrm_payment_creditCard_type' :    '001',
'dwfrm_payment_creditCard_owner' :   'Mike+Thomas',
'dwfrm_payment_creditCard_month' :    '08',
'dwfrm_payment_creditCard_year' :    '2021',
'selectedPaymentMethodID' :    'CREDIT_CARD',
'dwfrm_payment_securekey' : secureKey,
'dwfrm_payment_signcreditcardfields' :   'sign',
'format' :    'ajax'
}
response = session.post(dataURL, headers=headers, data=payload)
CheckResponse(response, '\nCHECKOUT - POST PAYMENT INFO DATA_URL')

#
#CHECKOUT - POST, SHIPPING INFO
# 
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
    'dwfrm_delivery_securekey': secureKey,
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
response = session.post(dataURL, headers=headers, data=payload)
CheckResponse(response, '\nCHECKOUT - POST SHIPPING INFO, DATA_URL')

#
# CHECKOUT
#
payload = {
    'dwfrm_payment_creditCard_cvn': card_cvv,
    'dwfrm_payment_creditCard_month': card_exp_month,
    'dwfrm_payment_creditCard_number': card_number,
    'dwfrm_payment_creditCard_owner': '{} {}'.format(first_name, last_name),
    'dwfrm_payment_creditCard_type': '001',  # visa
    'dwfrm_payment_creditCard_year': card_exp_year,
    'dwfrm_payment_securekey': secureKey,
    'dwfrm_payment_signcreditcardfields': 'sign'
}

#url = soup.find('form', {'id': 'dwfrm_delivery'})['action']
url='https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/COShipping-Show'
response = session.post(url, data=payload, headers=headers)
CheckResponse(response, '\nCHECKOUT - POST CC INFO')


print('\nDONE')