#! /usr/bin/python

'''
How I've been using:
- Manual search in Yelp for the area, filtering & skimming for key parameters.
- Type the restaurant names into the searches list & update city
- Run the program to extract search data
- Do diligence from the resulting sheet

It would be nice to get rid of those manual steps. Could certainly do this -
there is a fragment loop to go through all the hits that are returned from a
general search in a certain geo area. Haven't implemented yet as there is still
that need to filter with human insight.


Documentation on this:
The Business API
    https://www.yelp.com/developers/documentation/v2/business

The Search API
    https://www.yelp.com/developers/documentation/v2/search_api

API Keys:
    https://www.yelp.com/developers/manage_api_keys

Python Samples on GitHub:
    https://github.com/Yelp/yelp-python

'''
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import string
import json
import io

searches = ['Bar Bay Grill', 'Naschmarkt', 'South Winchester BBQ',
            'Orchard City Kitchen', 'Kaizen Japanese Bar', 'The Table',
            'Pacific Catch', 'Black Sheep Brasserie', 'Fogo de Chao Brazilian',
            'Siena Bistro', 'Willard Hicks', 'Dry Creek Grill', 'LB Steak']
city = '95128'

'''
            ['1760',
            'Gamine',
            'Stones Throw',
            'Nopa',
            'Academy Bar Kitchen',
            'The brick yard restaurant and bar',
            'Causwells',
            'bitters bock and rye',
            'absinthe-brasserie-and-bar',
            'Lord Stanley']
'''

outfile = open('yelpOut.csv', 'wb')
outfile.write('search term, name, url, phone, address, neighborhood, rating')
outfile.write('\n')

with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

'''
# Used this before hiding the API keys in separate JSON
auth = Oauth1Authenticator(
    consumer_key='',
    consumer_secret='',
    token='',
    token_secret=''
)

client = Client(auth)
'''

for searchName in searches:
    params = {
        'term': searchName,
        # 'lang': 'en'
    }

    # results = {
    term = params['term']
    name = ''
    phone = ''
    url = ''
    rating = ''
    address = ''
    neighborhood = ''
    try:
        res = client.search(city, **params)
        topHit = res.businesses[0]
        biz = topHit
        # res = client.get_business('Bobo-san-francisco', **params)
        # for biz in res.businesses:

        phone = str(biz.phone)
        phone = phone[:3] + '.' + phone[3:6] + '.' + phone[6:]
        url = biz.url
        url = string.split(url, '?')[0]
        rating = biz.rating
        for i, line in enumerate(biz.location.display_address):
            if i == 1: pass
            elif i == 1: address += line[:-1] + ' '
            else: address += line + ' '
        neighborhood = biz.location.neighborhoods[0]
        name = biz.name

    except: pass
    result = [term, name, url, phone, address, neighborhood, rating]
    for field in result:
        if type(field) == unicode:
            field = field.encode('utf8')
        field = string.replace(str(field), ',', '')
        outfile.write(field + ',')
    outfile.write('\n')

