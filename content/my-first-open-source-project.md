Title: My first Open Source Project
Date: 2017-07-23 20:10
Modified: 2017-07-23 20:10
Category: programming
Tags: python, open, source
Slug: my-first-open-source-project
Authors: Jahongir Rahmonov
Summary: My first open source project as a PyPI package

Lately, people [have](https://www.monster.com/career-advice/article/open-source-coding-can-give-your-career-an-edge)
[been](http://www.yegor256.com/2016/03/08/pimp-up-your-resume.html) saying that contributing to an open source project is very important for a 
programmer's career. I absolutely agree. That's why, I have been trying to contribute as much as I can in my free time by 
fixing a typo here, opening an issue there and solving some small issues. I still remember this feeling of joy when my first pull request
was merged to [the Falcon framework](https://falconframework.org/) :)

![first-pr](/static/images/post-images/first-osp/pr.jpg)

I also wanted to do something of my own. And today, I am excited to say that I published my first open source project in the form of a [PyPI package](https://pypi.python.org/pypi/agile-crm-python). YAY!

<div class="gallery large">
    <a href="/static/images/post-images/first-osp/pypi.png" rel="lightbox" title="My PyPi package">
        <img src="/static/images/post-images/first-osp/pypi.png" alt="My PyPi package">
        <span>My PyPi package</span>
    </a>
</div>

It is nothing big. Just a Python wrapper for [AgileCRM](https://www.agilecrm.com/) [REST API](https://github.com/agilecrm/rest-api).

However, there are a number of reasons why I made [this package](https://github.com/rahmonov/agile-crm-python)!

First of all, [their own package](https://github.com/agilecrm/python-api) was not comfortable to use. The following is how you update a tag field of a contact:

```python
update_tag_value = {
   "id": "5708993221623808",
   "tags": [
       "test1",
       "test2"
   ]
}

print agileCRM("contacts/edit/tags","PUT",update_tag_value,"application/json")
```
    
You have to input all these things manually such as `"application/json"` content-type or the method. You also have to know the URL of the endpoint.
Both of them could have easily been managed by the package itself.
   
The second reason is that this would decrease the readability of your code because the only method that is available is called `agileCRM()`. It 
is not really descriptive, is it? My colleagues would kill me for writing this kind of code. The solution is to wrap this by another method. Again, I think
that it the package should provide this.

The most important reason, however, is installation! In order to use this package, you have to find it in Github and download the code from there.
Very uncomfortable and raises the question of where you would put this code in your project.

Now, let's take a look at [my baby](https://github.com/rahmonov/agile-crm-python).

I will just give you some examples:

```python
agile_client.contact.fetch('5649050225344512')
agile_client.contact.delete('5649050225344512')
agile_client.contact.find(q='los', page_size=15)
agile_client.contact.get_notes(contact_id='5689413791121408')
agile_client.deal.fetch('5719238044024832')
client.contact.add_notes(subject='Second Note', description='DESCRIPTION', contact_id=contact_id)
```
    
I am definitely a little biased here but it is very easy to use because you just have to input your variables and forget about
method type, the endpoint url or the content-type. And look how readable it is. Just by reading, you know that you are fetching or updating a contact or you are
adding a note to a contact.

As for the installation, simple:

```commandline
pip install agile-crm-python
```
    
That's it!
    
Again, it is nothing big and probably won't be useful for a lot of people. However, I learned a lot in the process, from writing such a wrapper to making it available as a PyPI package.
    
If you also want to start or contribute to an open source project, I think the best advice would be taking a close look at the packages/libraries/frameworks that
you currently use. Maybe there are things that you think need some improvement. Even a small typo in the documentation. Or the name of the function. Anything!
Go ahead and fork the project, make improvements and send a pull request. You will see how exciting it is.

Okay, that's it from me today. If you liked what I did, please go to [my GitHub repo](https://github.com/rahmonov/agile-crm-python) and star the project. 
That would be awesome. Leave a comment if you think that something can be improved. That would be more than awesome. Thank you.

Fight on!


     
     
    
 