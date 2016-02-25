"""Postcodepy API ProxyView classes."""

from django.views.generic import View

from django.conf import settings
from postcodepy import postcodepy

USER_SETTINGS = getattr(settings, "POSTCODEPY", None)


class PostcodepyProxyView(View):
    """PostcodeProxyView."""

    def get(self, request, *args, **kwargs):
        """get."""
        access_key = USER_SETTINGS['AUTH']['API_ACCESS_KEY']
        access_secret = USER_SETTINGS['AUTH']['API_ACCESS_SECRET']
        api = postcodepy.API(environment='live',
                             access_key=access_key,
                             access_secret=access_secret)

        pcat = (kwargs['postcode'], kwargs['houseNumber'])
        if 'houseNumberAddition' in kwargs:
            pcat = pcat + (kwargs['houseNumberAddition'],)

        retValue = api.get_postcodedata(*pcat)
        return retValue


class SignalProxyView(View):
    """SignalProxyView."""

    def get(self, request, sar, *args, **kwargs):
        """get."""
        access_key = USER_SETTINGS['AUTH']['API_ACCESS_KEY']
        access_secret = USER_SETTINGS['AUTH']['API_ACCESS_SECRET']
        api = postcodepy.API(environment='live',
                             access_key=access_key,
                             access_secret=access_secret)
        retValue = api.get_signalcheck(sar)
        return retValue
