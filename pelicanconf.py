#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jahongir Rahmonov'
SITENAME = u'Jahongir Rahmonov'
SITEURL = 'http://rahmonov.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Tashkent'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None
# AUTHOR_FEED_ATOM = None
# AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['static']

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/{date:%b}/index.html'

THEME = 'themes/jahon'

PAGE_PATHS = ['pages']

LOAD_CONTENT_CACHE = False

DISQUS_SITENAME = u'rahmonov'
DISQUS_SECRET_KEY = u'o9soJ56YBumSIqWC1lq08OxotvKBivK8udpmDeMPkzeRd0H5WXS0hpvgkDXDKqZO'
DISQUS_PUBLIC_KEY = u'NKDqpbbBmL1Li8U6uhI001AgTTxtaMZX5FqccTvyLRpfkHUU3uLeYpqeYpof3uUW'

FEED_ALL_ATOM = 'feeds/atom.xml'
FEED_ALL_RSS = 'feeds/rss.xml'
FEED_DOMAIN = SITEURL
