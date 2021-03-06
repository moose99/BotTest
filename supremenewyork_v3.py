#from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
import requests
import timeit
import datetime
import time
import sys
import re
#from getconf import *

# TO DO: scrape for early links

# Constants
base_url = 'http://www.supremenewyork.com'

# Inputs
keywords_category = ['shirts']  # Demo stuff, feel free to change
keywords_model = ['mini', 'shadow', 'plaid', 'shirt']
keywords_style = ['blue']

size = 'medium'

use_early_link = True

early_link = 'http://www.supremenewyork.com/shop/jackets/kv6iqm8zl/w71g3imfh'
# early_link = 'http://www.supremenewyork.com/shop/jackets/nzpacvjtk' #sold out
# early_link = 'http://www.supremenewyork.com/shop/shirts/r1k32vjf4/sblz8csj2' # mult sizes
# early_link = 'http://www.supremenewyork.com/shop/accessories/kcgevis8r/xiot9byq4' #one size

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


# Functions
def product_page(url):
	print('Finding matching products...')
	session = requests.Session()
	session.headers.update({
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
		              'Chrome/52.0.2743.116 Safari/537.36',
		'X-XHR-Referer': 'http://www.supremenewyork.com/shop/all',
		'Referer': 'http://www.supremenewyork.com/shop/all/bags',
		'Accept': 'text/html, application/xhtml+xml, application/xml',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
		'DNT': '1'
	})

	response = session.get(base_url + url)
	soup = bs(response.text, 'html.parser')

	h1 = soup.find('h1', {'itemprop': 'name'})

	p = soup.find('p', {'itemprop': 'model'})

	match = []

	if h1 is not None and p is not None:
		model = h1.string
		style = p.string

		for keyword in keywords_model:
			if keyword.title() in model:
				match.append(1)
			else:
				match.append(0)

		# add to cart
		if 0 not in match:
			match = []
			for keyword in keywords_style:
				if keyword.title() in style:
					match.append(1)
				else:
					match.append(0)
			if 0 not in match:
				print('FOUND: ' + model + ' at ' + base_url + url)
				add_to_cart(soup, base_url+url)
			else:
				sys.exit('Sorry, couldnt find {} in {}'.format(model, style))


def add_to_cart(soup, url):
	product_name = soup.find('h1',{'itemprop': 'name'}).string
	print('Adding {} to cart...'.format(product_name))
	session = requests.Session()
	session.headers.update({
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
		              'Chrome/52.0.2743.116 Safari/537.36',
		'X-XHR-Referer': 'http://www.supremenewyork.com/shop/all',
		'Referer': 'http://www.supremenewyork.com/shop/all/',
		'Accept': 'text/html, application/xhtml+xml, application/xml',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
		'DNT': '1'
	})
	form = soup.find('form', {'action': re.compile('(?<=/shop/)(.*)(?=/add)')})
	csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

	# find size
	sold_out = soup.find('fieldset', {'id': 'add-remove-buttons'}).find('b')
	if sold_out is not None:
		sys.exit('Sorry, product is sold out!')
	else:
		if size.upper() == 'OS':
			size_value = form.find('input', {'name': 'size'})['value']
		else:
			try:
				size_value = soup.find('option', string=size.title())['value']
			except:
				sys.exit('Sorry, {} is sold out!'.format(size))
	
	if form is not None:
		payload = {
			'utf8': 'âœ“',
			'st': form.find('input', {'name': 'st'})['value'],
			'size': size_value,
			'commit': 'add to cart'
		}
		headers = {
			'Accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
			'Origin': 'http://www.supremenewyork.com',
			'X-Requested-With': 'XMLHttpRequest',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Referer': url,
			'X-XHR-Referer': None,
			'X-CSRF-Token': csrf_token,
			'Accept-Encoding': 'gzip, deflate'
		}

		print('st:' + payload['st'])
		print('size:' + payload['size'])
		
		session.post(base_url + form['action'], data=payload, headers=headers)
		print('Added to cart!')
		checkout(session)
	else:
		sys.exit('Sorry, product is sold out!')


def format_phone(n):
	return '({}) {}-{}'.format(n[:3], n[3:6], n[6:])


def format_card(n):
	return '{} {} {} {}'.format(n[:4], n[4:8], n[8:12], n[12:])


def checkout(session):
	print('Filling out checkout info...')
	response = session.get('https://www.supremenewyork.com/checkout')
	soup = bs(response.text, 'html.parser')
	form = soup.find('form', {'action': '/checkout'})

	csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
	headers = {
		'Accept': 'text/html, */*; q=0.01',
		'X-CSRF-Token': csrf_token,
		'X-Requested-With': 'XMLHttpRequest',
		'Referer': 'https://www.supremenewyork.com/checkout',
		'Accept-Encoding': 'gzip, deflate, sdch, br'
	}

	country_abbrv = shipping_country_abbrv
	if country_abbrv == 'US':
		country_abbrv = 'USA'

	payload = {
		'utf8': 'âœ“',
		'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
		'order[billing_name]': first_name + ' ' + last_name,
		'order[email]': email,
		'order[tel]': format_phone(phone_number),
		'order[billing_address]': shipping_address_1,
		'order[billing_address_2]': shipping_apt_suite,
		'order[billing_zip]': shipping_zip,
		'order[billing_city]': shipping_city,
		'order[billing_state]': shipping_state,
		'order[billing_country]': country_abbrv,
		'same_as_billing_address': '1',
		'store_credit_id': '',
		'credit_card[type]': card_type,
		'credit_card[cnb]': format_card(card_number),
		'credit_card[month]': card_exp_month,
		'credit_card[year]': card_exp_year,
		'credit_card[vval]': card_cvv,
		'order[terms]': '1',
		'hpcvv': '',
		'cnt': '2'
	}
	response = session.get('https://www.supremenewyork.com/checkout.js', data=payload, headers=headers)
	payload = {
		'utf8': 'âœ“',
		'authenticity_token': form.find('input', {'name': 'authenticity_token'})['value'],
		'order[billing_name]': first_name + ' ' + last_name,
		'order[email]': email,
		'order[tel]': format_phone(phone_number),
		'order[billing_address]': shipping_address_1,
		'order[billing_address_2]': shipping_apt_suite,
		'order[billing_zip]': shipping_zip,
		'order[billing_city]': shipping_city,
		'order[billing_state]': shipping_state_abbrv,
		'order[billing_country]': country_abbrv,
		'same_as_billing_address': '1',
		'store_credit_id': '',
		'credit_card[type]': card_type,
		'credit_card[cnb]': format_card(card_number),
		'credit_card[month]': card_exp_month,
		'credit_card[year]': card_exp_year,
		'credit_card[vval]': card_cvv,
		'order[terms]': '1',
		'hpcvv': ''
	}
	headers = {
		'Origin': 'https://www.supremenewyork.com',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Referer': 'https://www.supremenewyork.com/checkout',
		'Accept-Encoding': 'gzip, deflate, br'
	}

	response = session.post('https://www.supremenewyork.com/checkout', data=payload, headers=headers)
	
	#print(response.text)
	
	if 'Your order has been submitted' in response.text:
		print('Checkout was successful!')
		sys.exit(0)
	else:
		soup = bs(response.text, 'html.parser')
		print(soup.find('p').text)
		sys.exit(0)


def on_time():
	# Main
	print(datetime.datetime.now())
	start = timeit.default_timer()

	session1 = requests.Session()
	session1.headers.update({
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
		              'Chrome/52.0.2743.116 Safari/537.36',
		'Upgrade-Insecure-Requests': '1',
		'DNT': '1',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'en-US,en;q=0.8,da;q=0.6'
	})

	if use_early_link:
		try:
			response1 = session1.get(early_link)
			soup = bs(response1.text, 'html.parser')
		except:
			sys.exit('Unable to connect to site...')
		add_to_cart(soup, early_link)
	else:
		try:
			url = base_url + '/shop/all/' + keywords_category[0] + '/'
			response1 = session1.get(url)
		except:
			sys.exit('Unable to connect to site...')
		soup1 = bs(response1.text, 'html.parser')
		links1 = soup1.find_all('a', href=True)
		links_by_keyword1 = []
		for link in links1:
			for keyword in keywords_category:
				product_link = link['href']
				if keyword in product_link and 'all' not in product_link:
					if product_link not in links_by_keyword1:
						links_by_keyword1.append(link['href'])
		pool1 = ThreadPool(len(links_by_keyword1))
		result1 = pool1.map(product_page, links_by_keyword1)  # runtime

#sched = BlockingScheduler(timezone='America/New_York')
#sched.add_job(on_time, run_date='2016-09-01 10:59:59')
#sched.start()

on_time();

#
# checkout payload
#
####################################################
#===============================================================================
# REQUEST URL: https://www.supremenewyork.com/checkout.json 
# POST
# /////////////////
# PAYLOAD
# utf8	✓
# authenticity_token	mCbltO+dcmg5wGluqqHPR7AD0wZK22…kR4/ptDG//zwRH/kQTvv4M7sYlw==
# order[billing_name]	email+email
# order[email]	email@gmail.com
# order[tel]	123-456-7890
# order[billing_address]	123+main+street
# order[billing_address_2]	
# order[billing_zip]	12345
# order[billing_city]	Schenectady
# order[billing_state]	NY
# order[billing_country]	USA
# asec	Rmasn
# same_as_billing_address	1
# store_credit_id	
# credit_card[nlb]	4859+1093+9478+1135
# credit_card[month]	08
# credit_card[year]	2021
# credit_card[rvv]	982
# order[terms]	[…]
# 0	0
# 1	1
# g-recaptcha-response	03AHhf_50qryjIZWVaNkqZKDIfqChn…tBm7u3H8oVI6jgXLM4IjFyPN4tFTn
# credit_card[vval]
#===============================================================================
