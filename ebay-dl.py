import argparse
import requests
from bs4 import BeautifulSoup
import json

def parse_itemssold(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_shippingcost(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_shippingcost('+$65.90 shipping')
    6590
    >>> parse_shippingcost('Free shipping')
    0
    >>> parse_shippingcost('+$24.41 shipping')
    2441
    '''
    numbers = '0'
    for char in text:
        if char in '1234567890':
            numbers += char
    return int(numbers)

def parse_price(text):
    '''
    Takes as input a string and returns the number of items sold, as specified in the string.

    >>> parse_price('$74.99')
    7499
    >>> parse_price('$22.00 to $130.00')
    2200
    '''
    numbers = ''
    stop_index = None
    for i in range(len(text)-1):
        if text[i]=='t':
            x=i+1
            if text[x]=='o':
                stop_index = x
    if stop_index is not None:
        text = text[:stop_index-1]
    for char in text:
        if char in '1234567890':
            numbers += char
    return int(numbers)

# this if statement says only run the code below when the python file is run normally (not in the doctests)

if __name__ == '__main__':

    # get command line arguments
    parser = argparse.ArgumentParser(description='Donwload info from EBay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    args = parser.parse_args()
    print("args.search_term=", args.search_term)

    items = []

    # loop over the ebay webpages
    for page_number in range(1,int(args.num_pages)+1):
        # build the url
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw='
        url += args.search_term
        url += '&_sacat=0&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        print('url=',url)

        # download the html
        r = requests.get(url)
        status=r.status_code
        print('status=',status)
        html=r.text
        #print('html=',html[:50])
        
        # process the html
        soup = BeautifulSoup(html, 'html.parser')

        # loop over the items in the page
        tags_items = soup.select('.s-item')
        for tag_item in tags_items:
            print('tag_item=', tag_item)

            name = None
            tags_name = tag_item.select('.s-item__title')
            for tag in tags_name:
                name = tag.text

            price = None
            tags_price = tag_item.select('.s-item__price')
            for tag in tags_price:
                price = parse_price(tag.text)

            status = None
            tags_status = tag_item.select('.SECONDARY_INFO')
            for tag in tags_status:
                status = tag.text

            shipping = None
            tags_shipping = tag_item.select('.s-item__logisticsCost')
            for tag in tags_shipping:
                shipping = parse_shippingcost(tag.text)
            
            '''shipping = None
            tags_shipping = tag_item.select('.s-item__logisticsCost')
            for tag in tags_shipping:
                shipping = tag.text'''
            
            freereturns = False
            tags_freereturns = tag_item.select('.s-item__free-returns')
            for tag in tags_freereturns:
                freereturns=True

            items_sold = None
            tags_itemssold = tag_item.select('.s-item__hotness')
            for tag in tags_itemssold:
                items_sold = parse_itemssold(tag.text)

            item = {
                'name': name,
                'price': price,
                'status': status,
                'shipping': shipping,
                'free_returns': freereturns,
                'items_sold': items_sold,
            }
            items.append(item)

        print('len(tag_items)=', len(tags_items))

        for item in items:
            print('item=', item)

    print('len(items)=', len(items))

    # write the json to a file
    filename = args.search_term+'.json'
    with open (filename, 'w', encoding='ascii') as f:
        f.write(json.dumps(items))