from __future__ import print_function

import json

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext

# cache related
from django.core.cache import cache
from django.views.decorators.cache import cache_page




def get_navbar_as_string(request):

    return render_to_string('navbar_details.html'\
                            , {}\
                            , context_instance=RequestContext(request))


@cache_page(60 * 15)    # 15 minutes (900 seconds)
def view_nav_only(request):
    """
    Return the navbar HTML
    """
    return HttpResponse(get_navbar_as_string(request))


#@cache_page(60 * 15)    # 15 minutes (900 seconds)
CACHE_TIMEOUT = 60 * 15   # 15 minutes (900 seconds)
# 
def view_nav_only_as_json(request):
    """
    Return the navbar HTML as JSON
    """
    CACHE_KEY_FOR_NAVBAR = 'NAVBAR_JSON_DATA_RENDERED'
    
    # Is the navbar cached?
    navbar_data_json = cache.get(CACHE_KEY_FOR_NAVBAR)
    
    # No, create navbar
    #
    if navbar_data_json is None:
        
        # Render navbar as string
        #
        menu_string = get_navbar_as_string(request)

        # Add navbar to dict
        #
        navbar_data = { 'navbar_html' : menu_string }

        # Convert dict to JSON string
        #
        try:
            navbar_data_json = json.dumps(navbar_data)
        except:
            raise ValueError("Failed to convert navbar to JSON")
        
        # Save navbar JSON in cache
        #
        cache.set(CACHE_KEY_FOR_NAVBAR, navbar_data_json, CACHE_TIMEOUT)


    # Is this a JSON response?
    #
    if 'callback' in request.REQUEST:
        data = '%s(%s);' % (request.REQUEST['callback'], navbar_data_json)
        return HttpResponse(data, "text/javascript")

    return HttpResponse(navbar_data_json, mimetype="application/json")
