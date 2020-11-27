import requests
from .models import Artist, Venue, Show
from django.http import HttpResponse, HttpResponseServerError
import os
import logging
from urllib import parse
from django.core.exceptions import ObjectDoesNotExist


key = os.environ.get('TICKETMASTER_KEY')
baseUrl = 'https://app.ticketmaster.com/discovery/v2/'
not_authorized_message = 'You were not able to be authorized. Check your ticketmaster key is being properly set'
unavailable_message = 'There was a problem. Try again later.'

def get_artist(request):
    
    artist_list = []

    try:
        query = {'classificationName': 'music', 'dmaId': '336'}
        # Help of parsing url from https://www.youtube.com/watch?v=LosIGgon_KM
        url = '{}events.json?{}&apikey={}'.format(baseUrl, parse.urlencode(query), key)
        response = requests.get(url.strip())
        response.raise_for_status()
        data = response.json()
        results = data['_embedded']['events']

        for result in results:
            artist_name = result['_embedded']['attractions'][0]['name']

            if artist_name not in artist_list:
                artist_list.append(artist_name)
                Artist(name=artist_name).save()

        return HttpResponse('ok')

    except requests.HTTPError as e:
        logging.error(f'Error: {e}')
        if e.response.status_code == 401:
            return HttpResponseServerError(not_authorized_message)

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
            venue_name = result['name']
            venue_city = result['city']['name']
            venue_state = result['state']['name']

            Venue(name=venue_name, city=venue_city, state=venue_state).save()

        return HttpResponse('ok')

    except requests.HTTPError as e:
        logging.error(f'Error: {e}')
        if e.response.status_code == 401:
            return HttpResponseServerError(not_authorized_message)

    except Exception as e:
        logging.error(f'Error: {e}')
        return HttpResponseServerError(unavailable_message)



def get_show(request):

    try:
        query = {'classificationName': 'music', 'dmaId': '336'}
        url = '{}events.json?{}&apikey={}'.format(baseUrl, parse.urlencode(query), key)
        response = requests.get(url.strip())
        response.raise_for_status()
        data = response.json()
        results = data['_embedded']['events']
        
        for result in results:
            artist_name = result['_embedded']['attractions'][0]['name']
            venue_name = result['_embedded']['venues'][0]['name']
            show_date_time = result['dates']['start']['dateTime']

            artists = Show(show_date=show_date_time, artist=Artist.objects.get(name=artist_name), venue=Venue.objects.get(name=venue_name))

            artists.save()

        return HttpResponse('ok')

    except requests.HTTPError as e:
        logging.error(f'Error: {e}')
        if e.response.status_code == 401:
            return HttpResponseServerError(not_authorized_message)
            
    except Exception as e:
        logging.error(f'Error: {e}')
        return HttpResponseServerError(unavailable_message)


