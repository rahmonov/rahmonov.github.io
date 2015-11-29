Title: "Relation 'auth_user' does not exist" bug in Django 1.8
Date: 2015-10-01 21:14
Modified: 2015-10-01 21:14
Category: programming
Tags: python, django, bug
Slug: django-1.8-bug
Authors: Jahongir Rahmonov
Summary: Bug in Django 1.8 when used with PostgreSQL

I recently started a fresh project in Django 1.8 with PostgreSQL. I set everything up and was ready to do
my migrations. To my surprise, I got this error: `ProgrammingError: relation "auth_user" does not exist`.

I had absolutely no fancy stuff that could cause some problem.

I looked around and found out that I was not the only one. Even some [issues](https://github.com/evonove/django-oauth-toolkit/issues/204)
were opened on this question.

In short, here is how I solved it:

First option is to migrate the model which others depend on, i.e. `auth_user` and then the rest:

    :::python
    python manage.py migrate auth
    python manage.py migrate
     
Second option is downgrade the Django to 1.7 version and everything should work fine.

I hope this tip will prevent at least somebody from wasting a lot of time like I did.

Fight on!


