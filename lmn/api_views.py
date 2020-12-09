import requests
from .models import Artist, Venue, Show
from django.http import HttpResponse, HttpResponseServerError
import os
import logging
from urllib import parse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

key = os.environ.get('TICKETMASTER_KEY')
baseUrl = 'https://app.ticketmaster.com/discovery/v2/'

unavailable_message = 'There was a problem. Try again later.'

def get_events():
    designted_market_area = '336' # https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#supported-dma
    query = {'classificationName': 'music', 'dmaId': designted_market_area}
    # Help of parsing url from https://www.youtube.com/watch?v=LosIGgon_KM
    url = '{}events.json?{}&apikey={}'.format(baseUrl, parse.urlencode(query), key)
    response = requests.get(url.strip())
    response.raise_for_status()
    return response.json()

def get_artist(request):
    try:
        data = get_events()
        events = data['_embedded']['events']

        for event in events:
            # attractions are artists
            attractions = event['_embedded']['attractions']
            for attraction in attractions:
                try:
                    Artist(name=attraction['name']).save()
                except IntegrityError as e:
                    logging.error(f'Error: {e}')

        return HttpResponse('ok')

    except Exception as e:
        logging.error(f'Error: {e}')
        return HttpResponseServerError(unavailable_message)


def get_venue(request):

    try:
        query = {'classificationName': 'music', 'stateCode': 'MN'}
        url = '{}venues.json?{}&apikey={}'.format(baseUrl, parse.urlencode(query), key)
        response = requests.get(url.strip())
        response.raise_for_status()
        data = response.json()
        results = data['_embedded']['venues']
        
        for result in results:
            try:
                venue_name = result['name']
                venue_city = result['city']['name']
                venue_state = result['state']['name']
                address = None
                if result.get('address'):
                    address = result.get('address').get('line1')
                
                thumbnail = '/static/images/default-image.png'
                if result.get('images'):
                    for image in result.get('images'):
                        if image['ratio'] == '3_1':
                            thumbnail =  image['url']
                Venue(
                uuid=result.get('id'),
                address=address,
                name=venue_name,
                city=venue_city,
                state=venue_state,
                thumbnail=thumbnail).save()
            except IntegrityError as e:
                logging.error(f'Error: {e}')

            except Exception as e:
                logging.error(f'Error: {e}')

        return HttpResponse('ok')

    except Exception as e:
        logging.error(f'Error: {e}')
        return HttpResponseServerError(unavailable_message)



def get_show(request):

    try:
        data = get_events()
        events = data['_embedded']['events']

        for event in events:
            try:
                # todo: there is a many to many relationship that needs to be fixed.
                # a show can have many artists and an artist cna have many shows.
                artist_name = event['_embedded']['attractions'][0]['name']
                venue_name = event['_embedded']['venues'][0]['name']
                show_date_time = event['dates']['start']['dateTime']
                artists = Show(show_date=show_date_time, artist=Artist.objects.get(name=artist_name), venue=Venue.objects.get(name=venue_name))
                artists.save()
            except IntegrityError as e:
                logging.error(f'Error: {e}')
        return HttpResponse('ok')

    except Exception as e:
        logging.error(f'Error: {e}')
        return HttpResponseServerError(unavailable_message)


