Title: Introduction to Python Social Auth
Date: 2015-09-12 21:14
Modified: 2015-09-12 21:14
Category: python
Tags: python, authentication
Slug: introduction-to-python-social-auth
Authors: Jahongir Rahmonov
Summary: Python Social Auth aims to be an easy to setup social authentication and authorization mechanism for Python projects

Python Social Auth aims to be an easy to setup social authentication and authorization mechanism for 
Python projects supporting protocols like OAuth (1 and 2), OpenId and others.

Written by [omab](https://github.com/omab), this library helps a great deal in integrating social 
authentication to your web apps. Why am I writing this when there is a whole 
[documentation](http://psa.matiasaguirre.net/docs/index.html) on the subject? This post is by no means 
intended to replace the documentation. It is intended to serve as an introduction to the library itself 
and concepts used in it, such as pipeline, partial pipeline, extending and etc. understanding of which 
would have saved me a lot of time when I was learning the library.

I will not talk about small things like installation and configuration but rather try to give you a 
bigger picture on PSA.

Pipeline
---------

PSA uses a mechanism called Pipeline to do the autentication. Pipeline is like a stack of functions. 
These functions get executed one by one and return some result to the next function. 
The default pipeline looks like this:

```python
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    # 'social.pipeline.mail.mail_validation',
    # 'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
```

This is what happens when a user clicks a login button: `social_details` function gets executed first. 
It gets the information it can from, let's say, Facebook and returns it to the method `social_uid` in a 
simple format. `social_uid` method does the same thing: does something with the information it got from 
`social_details` and returns the result to `auth_allowed`. So on and so forth until the end of the 
pipeline when user gets returned to the url you specified. This is the authentication pipeline. 
There is also an disconnection pipeline, i.e. pipeline for when a user logs out. The same principles 
apply to that too. More info on pipeline can be found 
[here](http://psa.matiasaguirre.net/docs/pipeline.html).


Now, you can do whatever you like with this set of functions for the pipeline and customize it however 
you like. You can remove any of the methods, for example to create a pipeline that won't create users, 
just accepts already registered ones:

```python
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
```

Customize any of the methods:

```python
SOCIAL_AUTH_PIPELINE = (
    'path.to.custom.social_details',    # custom method
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
```

or just create a function and add it to the pipeline. Good example of extending a pipeline can be found 
[here](http://psa.matiasaguirre.net/docs/pipeline.html#extending-the-pipeline).

Partial Pipeline
----------------

It is also possible to cut the pipeline to ask the user for more information and resume the proccess 
later. For example, to ensure that the user provides his email, you can write the following partial 
pipeline:

```python
@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('require_email')
```

This method first checks whether email exists. If so, continues the pipeline. Otherwise, it will 
redirect to `require_email` view, which looks like this:

```python
def require_email(request):
    return render(request, 'path/to/template.html', args)
```

So, it will render the template with a form. Attention: this form must be submitted to 
`/complete/<backend>/` to continue the pipeline:

```html
<form action="/complete/instagram" method="post">
```

After a user submits the form, the pipeline comes to this part of the partial pipeline code:

```python
email = strategy.request_data().get('email')
if email:
    details['email'] = email  
```

and if user entered his email, the pipeline continues and you will have access to his email through 
`details['email']`.

Important use case
------------------

Provide login/registration with PSA for two types of users.

So we have two types of users, SimpleUser and Shop(SimpleUser) which extends from SimpleUser. 
To provide different registration proccess for them we can do the following:

1. Provide two different links and mark one of them with a get parameter(user_type):

        <a href="{% url 'social:begin' 'facebook' %}">Login as SimpleUser</a>
        <a href="{% url 'social:begin' 'facebook' %}?user_type=shop">Login as Shop</a>

2. In order to access this get parameter, we will have to do this in our settings file:
    
        FIELDS_STORED_IN_SESSION = ['user_type']
    
    This will ensure that the value of this paramter is saved in a session.

3. Then in `create_user` method of the pipeline, create different users depending on this parameter:

        :::python
        def create_user(strategy, backend, details, user=None, *args, **kwargs):
            user_type = strategy.session_get('type')
            if user_type == 'shop':
                  # create a shop
            else:
                  # create a simple user

    and don't forget to include it in the pipeline settings.

4. We are done! Hooorrayy  =)
  
Okay fellas, I hope you now have at least a little idea about how things work in PSA and can easily 
read the documentation. These were only the most important and basic parts. 
Checkout the documentation for the details. 

Fight on!