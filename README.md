Django-Market
=============
Django Market is an application for basic management of categories and products.
I'm using the super nice django-mptt application for handling hierarchies and
another very good app called django-modeltranslation for localization.
Kudos to the authors of both apps.

Requirements
------------
- [django == 1.6.x](https://www.djangoproject.com/), cannot still confirm for 1.7.x compatibility.
- [django-mptt](https://github.com/django-mptt/django-mptt/)
- [django-modeltranslation == 0.7.x](https://github.com/deschler/django-modeltranslation/)
- [django-galleries](https://github.com/marcopompili/django-galleries/)

Features
--------
Key features of django-market are:
- The ability to use long hierarchical structures.
- Localized text for every field published in the template.
- URLs are localized as well, meaningful URLs in every language are automatically generated.
- Image galleries support.
- Manager for displaying categories and products on a slider/front-page/home.

Installation
------------
This application can be installed cloning this repository and using pip to install the application locally, like this:
```
pip install django-market
```

Configuration
-------------
Standard configuration for the settings.py file, add the needed applications in this order:
```python
INSTALLED_APPS = (
  [...]
  'modeltranslation',
  'sorl.thumbnails',
  'mptt',
  'django_galleries',
  'django_market',
  [...]
)
```

And then run syncdb to synchronize the database, like this:
```
manage.py syncdb
```

Multi-language will automatically be supported in a localized configuration, for example:
```python
LOCALE_PATHS = (
    django_path('locale/'),
)

gettext = lambda s: s

LANGUAGES = (
    ('it', gettext('Italiano')),
    ('en', gettext('English')),
    ('de', gettext('Deutsche')),
)

TIME_ZONE = 'Europe/Rome'

LANGUAGE_CODE = 'it'
```

This configuration will support Italian (default), English and German.
If localized support is not needed just don't add any localized configuration in settings.py.

It is good to know that localization will make your tables grow, for every language a new column will be added.
This is how django-modeltranslation works, i cannot change this behaviour.


Template
--------
The templates are based on [Bootstrap 3.2.0](http://getbootstrap.com/).
I'm using the grid system for displaying categories and products.

So remember to include bootstrap in your base template.