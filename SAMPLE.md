Sample backend-app
=====================

     $ cd <somedir>
     $ virtualenv pcp
     $ cd pcp
     $ . ./bin/activate
     $ pip install django
     $ pip install django-postcodepy-proxy

     $ django-admin startproject pcp
     $ cd pcp
     $ django startapp pcproxy
     $ cd pcproxy

Add views to the views.py
--------------------------

Edit the file: views.py and add the HTML and JSON views

     from django.shortcuts import render
     from django.http import HttpResponse
     import json

     from postcodepy_proxy.views import PostcodepyProxyView
     from postcodepy.postcodepy import PostcodeError

     class PCDemoHTMLView( PostcodepyProxyView ):
       template_name = "postcodeproxy.html"

       def get(self, request, *args, **kwargs):
         rv = super(PCDemoHTMLView, self).get(request, *args, **kwargs)
         return render(request, self.template_name, rv)


     class PCDemoJSONView( PostcodepyProxyView ):
       def get(self, request, *args, **kwargs):
         rv = None
         try:
           rv = super(PCDemoJSONView, self).get(request, *args, **kwargs)
         except PostcodeError, e:
           # Pass the exceptioninformation as response data
           rv = e.response_data

         return HttpResponse( json.dumps(rv), content_type="application/json")


Add a HTML template
----------------------

Create a file: templates/postcodeproxy.html

      <h1>Postcodeproxy</h1>
      {{ postcode }}
      {{ huisnummer }}
      {{ city }}
      {{ street }}
      {{ postcode }}
      {{ houseNumber }}
      {{ latitude }}
      {{ longitude }}

Routes for the requests
-----------------------

Create the file: urls.py

      from django.conf.urls import patterns, include, url
      from django.contrib import admin

      from pcproxy import views

      urlpatterns = patterns('',
          url(r'^postcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/$', views.PCDemoHTMLView.as_view() ),
          url(r'^postcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/(?P<houseNumberAddition>[A-Za-z]+)/$', views.PCDemoHTMLView.as_view() ),
      
          url(r'^jsonpostcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/$', views.PCDemoJSONView.as_view() ),
          url(r'^jsonpostcode/(?P<postcode>[\d]{4}[a-zA-Z]{2})/(?P<houseNumber>[\d]+)/(?P<houseNumberAddition>[A-Za-z]+)/$', views.PCDemoJSONView.as_view() ),
)


Alter project settings
-------------------------

Edit the pcp/settings.py and add the apps

      INSTALLED_APPS = (
        ...
        'postcodepy_proxy',
        'pcproxy',
      )

and the authentication information required by *postcodepy_proxy*

      POSTCODEPY = {
        "AUTH" : {
          "API_ACCESS_KEY" : "<your_access_key>",
          "API_ACCESS_SECRET" : "<your_access_secret>",
        },
      }

Add the app urls to the project urls
------------------------------------

    url(r'^pcp/', include('pcproxy.urls')),

Up and running ...
-------------------

    python manage.py runserver
