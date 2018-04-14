Title: Customize django admin templates
Date: 2015-10-18 21:14
Modified: 2015-10-18 21:14
Category: python
Tags: python, django, admin
Slug: customize-django-admin-templates
Authors: Jahongir Rahmonov
Summary: How to customize django admin templates

Quite often, we need to customize the django admin template: to add additional functionality or just 
change its look and feel.

Recently, I had the task of adding an ajax request on admin page load(specifically, change_form.html) 
and adding two buttons, one of which would bring a modal up and the other would delete the selected items
which, in their turn, were brought by that ajax request.

Here is what I did and went through:

Template
--------

First, I created a `change_form.html` file in `/templates/admin/` folder. As I wanted this file to extend, 
not replace, the default `change_form.html`, I wrote this at the beginning of the file:

    :::python
    {% extends 'admin/change_form.html' %}
    
This, naturally, led to `maximum recursin depth exceeded` error as it was trying to `extend` itself.

Then, I read somewhere that I could put this file in `/templates/admin/app_name` folder, so that it will 
change the templates of only this app. Voila! Recursion problem solved.

Then, I added all those buttons and modals I wanted to(more on this later). Everything was working fine 
until I found out that the buttons I added appear on the admin pages of all the models in the app. But 
I wanted them to appear only on the admin pages of, let's say, `product` model.

Turned out, the same works here. I just needed to put the file inside `/templates/admin/app_name/model_name`.
In my case, it the file was  `/templates/admin/enterprise/product`.

Styles, Scripts and Buttons
---------------------------

Where do I put them? Taking a look at `admin/base.html` did the trick. It has special blocks for extra styles and
scripts. So I put my css and javascript files in the following way:

    :::python
    {% block extrastyle %}
        {{ block.super }}
        
        <link rel="stylesheet" href="{% static 'css/enterprise/main.css'%}">
    {% endblock %}
    
    {% block extrahead %}
        {{ block.super }}
        
        <script type="text/javascript" src="{% static 'js/enterprise/modal.js'%}"></script>
    {% endblock %}
    
As for buttons, I thought a good place would be above the default buttons. So, I thought out the block of those buttons 
and put mine right above them:

    :::python
    {% block submit_buttons_bottom %}
        <div class="submit-row">
            <button class="btn btn-danger">Custom Button</button>
        </div>
    
        {{ block.super }}
    {% endblock %}
    
As I was using [django-admin-bootstrapped](https://github.com/django-admin-bootstrapped/django-admin-bootstrapped),
`submit-row` gave the `div` nice and natural look.

Additional
----------

In the ajax request, I had to send the `id` of the product being changed. So I thought I could get it with `{{ product.id }}`
but I was wrong. Then, I learned that I could get it like so:

    :::python
    {{ original.id }}
    
So, the model instance being dealt with can be accessed with the word `original`. How original, isn't it?

Wrap up
-------

Either I am bad at reading the documentation or it could be improved a little further. Probably first option. 

I hope it will help somebody save some time in the future.

Fight on!


   
