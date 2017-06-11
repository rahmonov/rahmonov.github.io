Title: TestCase vs TransactionTestCase in Django
Date: 2017-06-11 20:10
Modified: 2017-06-11 20:10
Category: programming
Tags: python, django, unittesting, testing
Slug: testcase-vs-transactiontestcase-in-django
Authors: Jahongir Rahmonov
Summary: The difference between TestCase and TransactionTestCase in Django

Based on my observation, a lot of developers don't seem to understand the difference between `TestCase` and `TransactionTestCase`
in Django and how to use them. In this post, I will try to put the puzzle pieces together and make things clear.

TestCase class
---------------

Here is what [the documentation](https://docs.djangoproject.com/en/1.11/topics/testing/tools/#django.test.TestCase) has to say
about the `TestCase` class:


> Wraps the tests within two nested atomic() blocks: one for the whole class and one for each test.

Now imagine that you have a method that must be executed inside a transaction or else it raises an error. You could write a test similar to this:

    class SomeTestCase(TestCase):
    
        def test_your_method_raises_error_without_atomic_block(self):
            with self.assertRaises(SomeError):
                your_method()
    
In this test, `your_method()` is called without any transaction and the test is asserting that it raises `SomeError` because of that.

However, this test will unexpectedly fail! The reason is, you guessed it, TestCase wraps the tests with `atomic()` blocks 
ALL THE TIME. Thus, `your_method()` will not raise an error, which is why this test will fail.

TransactionTestCase to the rescue
----------------------------------

This is where `TransactionTestCase` should be used. It does not wrap the tests with `atomic()` block and thus you can test your special 
methods that require a transaction without any problem. The above test will pass with `TransactionTestCase` now:

    class SomeTestCase(TransactionTestCase):
    
        def test_your_method_raises_error_without_atomic_block(self):
            with self.assertRaises(SomeError):
                your_method()
                

Real Life example
-----------------

Let's see a real example now. A queryset method called [select_for_update()](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#django.db.models.query.QuerySet.select_for_update) 
is one of those methods that require to be inside a transaction. If you call it without any transaction, it raises an error.

Let's say you have a model called `Item` and you are calling `select_for_update()`:

    Item.objects.select_for_update()
    
It will immediately raise the following error:

    TransactionManagementError: select_for_update cannot be used outside of a transaction.
    
Now, let's try to write tests for it with both `TestCase` and `TransactionTestCase`:

    class ItemTestCase(TestCase):
        def setUp(self):
            self.item = Item.objects.create(name='hat')

        def test_select_for_update_raises_an_error_without_transaction(self):
            with self.assertRaises(TransactionManagementError):
                items = Items.objects.select_for_update().filter()
                print(items)  # needed to actually execute the query because they are lazy
                
Try to run the test and you will get the following:

    AssertionError: TransactionManagementError not raised
    
The reason? `TestCase` wraps the tests with `atomic()` blocks ALL THE TIME. Good. Glad you remember this. 

Now, let's make this test pass with `TransactionTestCase`:

    
    class ItemTestCase(TransactionTestCase):
        def setUp(self):
            self.item = Item.objects.create(name='hat')

        def test_select_for_update_raises_an_error_without_transaction(self):
            with self.assertRaises(TransactionManagementError):
                items = Items.objects.select_for_update().filter()
                print(items)  # needed to actually execute the query because they are lazy

and voila! The test passes! Great!

I hope it will clear things out for some people. Let me know in the comments if something is still not clear.

Fight on!




    
                