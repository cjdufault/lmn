import requests
from .models import Artist, Venue, Show
from django.http import HttpResponse, HttpResponseServerError
import os
import logging
from urllib import parse
from django.db import IntegrityError

key = os.environ.get('TICKETMASTER_KEY')
baseUrl = 'https://app.ticketmaster.com/discovery/v2/'

unavailable_message = 'There was a problem. Try again later.'


def get_events():
    """ This function calls the ticketmaster api and returns event data for area 336
    :return: The Ticketmaster API response as a `JSON`
    """
    # 336 is Minneapolis/ St Paul
    designted_market_area = '336'
    # https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#supported-dma
    query = {'classificationName': 'music', 'dmaId': designted_market_area}
    url = '{}events.json?{}&apikey={}'.format(baseUrl, parse.urlencode(query), key)
    response = requests.get(url.strip())
    response.raise_for_status()
    return response.json()


def get_artist(request):
    """ This function is called by the /artist endpoint and populates the db with artist information"""
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
    """ This function is called by the /venue endpoint and populates the db with venue information"""
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
                Venue(name=venue_name, city=venue_city, state=venue_state).save()
            except IntegrityError as e:
                logging.error(f'Error: {e}')

        return HttpResponse('ok')

    except Exception as e:
        logging.error(f'Error: {e}')
        return HttpResponseServerError(unavailable_message)


def get_show(request):
    """ This function is called by the /show endpoint and populates the db with show information"""
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
