'''
Created on Nov 14, 2017

@author: moose-home

Based on tutorial: https://www.youtube.com/watch?v=rkt8o1Ze3To
'''
import requests
from bs4 import BeautifulSoup as bs
import random
import threading

#
# GET AVAILABLE SIZES
#
def get_sizes_in_stock(session):
    endpoint = "http://www.jimmyjazz.com/mens/footwear/nike-sportswear-foamposite-pro-prm/624041-006?color=Black"
    response = session.get(endpoint)
    
    soup = bs(response.text,"html.parser")
    
    div = soup.find("div",{"class":"box_wrapper"})
    all_sizes = div.find_all("a")
    
    sizes_in_stock = []
    for size in all_sizes:
        if "piunavailable" not in size["class"]:
            size_id = size["id"]
            sizes_in_stock.append(size_id.split("_")[1])
            
    return sizes_in_stock

#
# ADD TO CART a random size
#
def add_to_cart(session):
    sizes_in_stock = get_sizes_in_stock(session)
    if (sizes_in_stock == []):
        print("Out of stock")
        return False;
    size_chosen = random.choice(sizes_in_stock)
    
    endpoint = "http://www.jimmyjazz.com/cart-request/cart/add/%s/1"%(size_chosen)
    response = session.get(endpoint)
    
    ok = '"success":1' in response.text
    if (ok == False):
        print (response.text)
    else:
        print("Added to cart:" + endpoint)
    return ok;

#
# CHECKOUT
#
def checkout(session):
    endpoint0 = "https://www.jimmyjazz.com/cart/checkout"
    response0 = session.get(endpoint0)
    
    # get the form_build_id token
    soup = bs(response0.text,"html.parser")
    inputs = soup.find_all("input",{"name":"form_build_id"})
    form_build_id = inputs[1]["value"]
    
    # post the CHECKOUT form
    endpoint1 = "https://www.jimmyjazz.com/cart/checkout"
    payload1 = {
        "billing_email":"email@gmail.com",
        "billing_email_confirm":"email@gmail.com",
        "billing_phone":"1234567890",
        "email_opt_in":"1",
        "shipping_first_name":"Noah",
        "shipping_last_name":"Fighter",
        "shipping_address1":"123 Street Street",
        "shipping_address2":"",
        "shipping_city":"Brooklyn",
        "shipping_state":"NY",
        "shipping_zip":"11238",
        "shipping_method":"0",
        "signature_required":"1",
        "billing_same_as_shipping":"1",
        "billing_first_name":"",
        "billing_last_name":"",
        "billing_country":"US",
        "billing_address1":"",
        "billing_address2":"",
        "billing_city":"",
        "billing_state":"",
        "billing_zip":"",
        "cc_type":"Visa",
        "cc_number":"1111 2222 3333 4444",
        "cc_exp_month":"08",
        "cc_exp_year":"21",
        "cc_cvv":"982",
        "gc_num":"",
        "form_build_id":form_build_id,
        "form_id":"cart_checkout_form"
    }
    response1 = session.post(endpoint1, data=payload1)
    
    # get the form_build_id token again and POST cart confirm
    soup = bs(response1.text,"html.parser")
    inputs = soup.find_all("input",{"name":"form_build_id"})
    form_build_id = inputs[1]["value"]
    
    endpoint2 = "https://www.jimmyjazz.com/cart/confirm"
    payload2 = {
        "form_build_id":form_build_id,
        "form_id":"cart_confirm_form"
    }
    response2 = session.post(endpoint2, data=payload2)
    
    ok = '"success":1' in response2.text
    if (ok == False):
        soup = bs(response2.text, 'html.parser')
        try:
            error = soup.find('div', {'class': 'messages error'}).text
            print(error)
        except:
            return ok
    return ok

def run():
    session = requests.session()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'};
    session.headers.update(headers);
    
    if (add_to_cart(session) == True):
        if (checkout(session) == True):
            print("Checkout success")
        else:
            print("Checkout failed")
    else:
        print("Add to cart failed")
    
#
# MAIN
#

#
# kick off 5 threads of the 'run function'
# probably need proxies here, so that too many actions at once from the same place don't cause a block
#
numThreads=2
threads=[]
for i in range(numThreads):
    t = threading.Thread(target=run)
    threads.append(t)
    t.start()
    
