'''
Created on Aug 27, 2017

@author: moose-home
'''

import requests
import bs4
import webbrowser
import threading
import RandomHeaders

# get this from storm proxies
proxies = {
    'http' : '37.48.118.90:13012',
    'https' : '37.48.118.90:13012',
}

ModelNumber = 'BB9043'
SizeList = [9, 13, 8, 10]
ThreadCount = 10

# Ex: size 7 is 590, size 8 is 610
# Ex link of AlphaBounce size 8 from my cart:
#    http://www.adidas.com/us/alphabounce-ams-shoes/BY4327.html?forceSelSize=BY4327_610
def URLGen(model, size, quantity):
    BaseShoeSize = 580    # Base Show Size code based on Size 6.5
    ShoeSize = float(size) - 6.5
    ShoeSize = ShoeSize * 20
    RawShoeSizeCode = ShoeSize + BaseShoeSize
    ShoeSizeCode = int(RawShoeSizeCode)
    URL = "https://www.adidas.com/us/" + str(model) + '.html?Quantity=' + str(quantity) + '&forceSelSize=' + str(model) + '_' + str(ShoeSizeCode)
 #   return "https://www.adidas.com/us/BB9043.html?forceSelSize=BB9043_600"
    return URL
             
def CheckStock(url):
    print('CheckStock')
    RawHTML = requests.get(url, headers=RandomHeaders.LoadHeader())  # , proxies=proxies)
    Page = bs4.BeautifulSoup(RawHTML.text, "lxml")
    RawAvailableSizes = Page.select('.size-dropdown-block')     # got this css tag by using selector gadget
    Sizes = str(RawAvailableSizes[0].getText()).replace("\t", "")
    Sizes = Sizes.replace("\n\n", " ")
    Sizes = Sizes.split()
    Sizes.remove('Select')
    Sizes.remove('size')
    return Sizes

def DoSomething(size):
    print('Buy size ' + size)
    
def SneakerBot(model, size=None):
    print('SneakerBot, model=' + model + ', size=' + str(size))
    while True:
        try:
            url = 'http://www.adidas.com/us/{}.html?'.format(model)
            Sizes = CheckStock(url)
            for s in Sizes:
                print(s)
            if size != None:
                if str(size) in Sizes:
                    DoSomething(size)
            else:
                for a in Sizes:
                    DoSomething(a)
        except:
            pass
                    
#
#
#
#===============================================================================
# model = raw_input('Model Number: ')     # this is a string so it needs raw_input
# size = input('Size: ')
# quantity = input('Quantity: ')
# 
# FindItem(model, size, quantity)
#===============================================================================

# create ThreadCount * sizeof(SizeList) threads.  ie 10 threads for each size in the SizeList
threads = [threading.Thread(name='ThreadNumber{}'.format(n), target=SneakerBot, args=(ModelNumber, size,)) for size in SizeList for n in range(ThreadCount)]
i=0
for t in threads: 
    print("Starting thread:" + str(i))
    i+=1
    t.start()
