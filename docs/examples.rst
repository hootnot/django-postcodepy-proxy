.. _example-label:

Example
-------


Lets create a simple Django appplication that accepts parameters via the URL and present the
postcode.nl REST API response in HTML output.

Setup the Django environment
============================

Create a virtual environment and install the packages we need:

.. code-block:: shell

     $ cd <somedir>
     $ virtualenv pcp
     $ cd pcp
     $ . ./bin/activate
     $ pip install django
     $ pip install django-postcodepy-proxy

     $ django-admin startproject pcp
     $ cd pcp
     $ django-admin startapp pcproxy
     $ cd pcproxy

Add views
=========================

Edit the file: pcproxy/views.py and add the HTML and JSON views.

.. code-block:: python

    from django.shortcuts import render
    from django.http import HttpResponse
    import json
    
    from postcodepy_proxy.views import PostcodepyProxyView
    from postcodepy.postcodepy import PostcodeError
    
    
    class PCDemoHTMLView(PostcodepyProxyView):
        template_name = "postcodeproxy.html"
    
        def get(self, request, *args, **kwargs):
            rv = None
            try:
                rv = super(PCDemoHTMLView, self).get(request, *args, **kwargs)
            except PostcodeError as e:
                # Pass the exceptioninformation as response data
                rv = e.response_data

        return render(request, self.template_name, rv)
    
    
    class PCDemoJSONView(PostcodepyProxyView):
        def get(self, request, *args, **kwargs):
            rv = None
            try:
                rv = super(PCDemoJSONView, self).get(request, *args, **kwargs)
            except PostcodeError as e:
                # Pass the exceptioninformation as response data
                rv = e.response_data
    
            return HttpResponse(json.dumps(rv, sort_keys=True, indent=2),
                                content_type="application/json")


Add a HTML template
===================

Create a file: templates/postcodeproxy.html

.. code-block:: html

      <h1>Postcodeproxy</h1>
        {{ postcode }}
        {{ huisnummer }}
        {{ city }}
        {{ street }}
        {{ postcode }}
        {{ houseNumber }}
        {{ latitude }}
        {{ longitude }}


      {% if exception %}
        <H1>OOPS:<H1>
        <H3>exception: {{exception}}<H3>
        <H3>exceptionId: {{exceptionId}}<H3>
      {% endif %}


Add request routes
==================

Create the ``pcproxy/urls.py`` file and add url's to route the requests.

.. code-block:: python

      from django.conf.urls import url
      from django.contrib import admin

      from pcproxy import views

      urlpatterns = [
          url(r'^postcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/$', views.PCDemoHTMLView.as_view() ),
          url(r'^postcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/(?P<houseNumberAddition>[\dA-Za-z]+)/$', views.PCDemoHTMLView.as_view() ),
      
          url(r'^jsonpostcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/$', views.PCDemoJSONView.as_view() ),
          url(r'^jsonpostcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/(?P<houseNumberAddition>[\dA-Za-z]+)/$', views.PCDemoJSONView.as_view() ),
      ]


Alter project settings
======================

Edit the ``pcp/settings.py`` and add the apps

.. code-block:: python

      INSTALLED_APPS = (
        ...
        'postcodepy_proxy',
        'pcproxy',
      )

and the authentication information required by *postcodepy_proxy*

.. code-block:: python

      POSTCODEPY = {
        "AUTH" : {
          "API_ACCESS_KEY" : "<your_access_key>",
          "API_ACCESS_SECRET" : "<your_access_secret>",
        },
      }


Add the app urls to the project urls
````````````````````````````````````

Edit the project ``pcp/urls.py`` file and add the reference the ``pcproxy/urls.py`` file:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'^pcp/', include('pcproxy.urls')),
    ]


Up and running ...
``````````````````

.. code-block:: shell

    $ python manage.py runserver

From your webbrowser hit: ``http://127.0.0.1:8000/pcp/jsonpostcode/7514BP/129/`` and you should get the response:

.. code-block:: json

    {
      "addressType": "building", 
      "bagAddressableObjectId": "0153010000345343", 
      "bagNumberDesignationId": "0153200000345342", 
      "city": "Enschede", 
      "houseNumber": 129, 
      "houseNumberAddition": "", 
      "houseNumberAdditions": [
        "", 
        "A"
      ], 
      "latitude": 52.22770127, 
      "longitude": 6.89701549, 
      "municipality": "Enschede", 
      "postcode": "7514BP", 
      "province": "Overijssel", 
      "purposes": [
        "assembly"
      ], 
      "rdX": 258149, 
      "rdY": 472143, 
      "street": "Lasondersingel", 
      "surfaceArea": 6700
    }

As you can see in the response, this postcode/number combination also comes with a houseNumberAddition ``A``. When we hit: ``http://127.0.0.1:8000/pcp/jsonpostcode/7514BP/129/A/`` you should get the response:

.. code-block:: json

    {
      "addressType": "building", 
      "bagAddressableObjectId": "0153010000329929", 
      "bagNumberDesignationId": "0153200000329928", 
      "city": "Enschede", 
      "houseNumber": 129, 
      "houseNumberAddition": "A", 
      "houseNumberAdditions": [
        "", 
        "A"
      ], 
      "latitude": 52.22770127, 
      "longitude": 6.89701549, 
      "municipality": "Enschede", 
      "postcode": "7514BP", 
      "province": "Overijssel", 
      "purposes": [
        "residency"
      ], 
      "rdX": 258149, 
      "rdY": 472143, 
      "street": "Lasondersingel", 
      "surfaceArea": 119
    }


... or with an exception, hit: ``http://127.0.0.1:8000/pcp/jsonpostcode/7514BP/129/B`` and you should get the response:

.. code-block:: json

    {
      "exception": "Invalid housenumber addition: 'None'", 
      "exceptionId": "ERRHouseNumberAdditionInvalid", 
      "validHouseNumberAdditions": [
        "", 
        "A"
      ]
    }
