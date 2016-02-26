Installation
============

Introduction
------------

The postcodepy_proxy package offers a simple API for Django to the Postcode.nl API REST service.
To use the Django postcodepy_proxy you will need an *access_key* and *access_secret*. For details
check api.postcode.nl_.

.. _api.postcode.nl: https://api.postcode.nl

.. note:: 

   This package is ONLY useful to be used with the postcode REST-service of api.postcode.nl_.


Application
-----------

The simple combination of ``postcode/housenumber`` allows the retrieval of a rich set of address information. You can use this for instance in websites for orderhandling or registration purposes. Using AJAX 
a registration form can be autocompleted for several parts. For details take a look at the :ref:`example-label`.



Download & Install
------------------

From pypi
```````````

Install the package with pip:

.. code-block:: shell

    $ pip install django-postcodepy-proxy



From Github
```````````

.. code-block:: shell

    $ git clone https://github.com/hootnot/django-postcodepy-proxy.git
    $ cd django-postcodepy-proxy
    $ python setup.py install
