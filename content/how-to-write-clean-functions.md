Title: How to write clean functions
Date: 2016-06-15 20:10
Modified: 2016-06-15 20:10
Category: programming
Tags: clean, code, functions, robert, martin
Slug: how-to-write-clean-functions
Authors: Jahongir Rahmonov
Summary: Key takeaways from the chapter Functions of the book Clean Code by Robert C. Martin 

The following is heavily influenced (99%) by one of the must-read books for any developer: [Clean Code: A Handbook of Agile Software Craftsmanship](https://www.amazon.com/gp/product/0132350882/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0132350882&linkCode=as2&tag=rahmonov-20&linkId=8f50e156683243a557687dbe7c8fda9e)

<a target="_blank" href="https://www.amazon.com/gp/product/0132350882/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0132350882&linkCode=as2&tag=rahmonov-20&linkId=8f50e156683243a557687dbe7c8fda9e"><img border="0" src="//ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=US&ASIN=0132350882&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_SL250_&tag=rahmonov-20" ></a><img src="//ir-na.amazon-adsystem.com/e/ir?t=rahmonov-20&l=am2&o=1&a=0132350882" width="1" height="1" border="0" alt="Clean Code" style="border:none !important; margin:0px !important;" />

Clean Code
----------

    Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live.
    Code for readability.
    
Damn right!!! Uncle Bob Martin even mentions of a once-successful company that went bankrupt 
because of unmaintainable codebase. Clean code is that serious.

Now that we know the importance of clean code, let's take a look at how to write clean functions first.

Clean Functions
---------------

Functions are key players in any program and it is very important to write them well.

Let's take a look at the following code:

    :::java
    public static String testableHtml(PageData pageData, boolean includeSuiteSetup) throws Exception {
        WikiPage wikiPage = pageData.getWikiPage();
        StringBuffer buffer = new StringBuffer();
        if (pageData.hasAttribute("Test")) {
            if (includeSuiteSetup) {
                WikiPage suiteSetup =
                        PageCrawlerImpl.getInheritedPage(
                                SuiteResponder.SUITE_SETUP_NAME, wikiPage
                        );
                if (suiteSetup != null) {
                    WikiPagePath pagePath =
                            suiteSetup.getPageCrawler().getFullPath(suiteSetup);
                    String pagePathName = PathParser.render(pagePath);
                    buffer.append("!include -setup .")
                            .append(pagePathName)
                            .append("\n");
                }
            }
            WikiPage setup =
                    PageCrawlerImpl.getInheritedPage("SetUp", wikiPage);
            if (setup != null) {
                WikiPagePath setupPath =
                        wikiPage.getPageCrawler().getFullPath(setup);
                String setupPathName = PathParser.render(setupPath);
                buffer.append("!include -setup .")
                        .append(setupPathName)
                        .append("\n");
            }
        }
        buffer.append(pageData.getContent());
        if (pageData.hasAttribute("Test")) {
            WikiPage teardown =
                    PageCrawlerImpl.getInheritedPage("TearDown", wikiPage);
            if (teardown != null) {
                WikiPagePath tearDownPath =
                        wikiPage.getPageCrawler().getFullPath(teardown);
                String tearDownPathName = PathParser.render(tearDownPath);
                buffer.append("\n")
                        .append("!include -teardown .")
                        .append(tearDownPathName)
                        .append("\n");
            }
            if (includeSuiteSetup) {
                WikiPage suiteTeardown =
                        PageCrawlerImpl.getInheritedPage(
                                SuiteResponder.SUITE_TEARDOWN_NAME,
                                wikiPage
                        );
                if (suiteTeardown != null) {
                    WikiPagePath pagePath =
                            suiteTeardown.getPageCrawler().getFullPath(suiteTeardown);
                    String pagePathName = PathParser.render(pagePath);
                    buffer.append("!include -teardown .")
                            .append(pagePathName)
                            .append("\n");
                }
            }
        }
        pageData.setContent(buffer.toString());
        return pageData.getHtml();
    }
    
Obviously, this is not a well-written function. But what problems does it have?!

    - Too much going on, i.e. too big
    - Many different levels of abstraction
    - Nested if statements controlled by flags
    
With little method extraction, renaming and restructuring, we can come to the better version:

    :::java
    public static String renderPageWithSetupsAndTeardowns(PageData pageData, boolean isSuite) throws Exception {
        boolean isTestPage = pageData.hasAttribute("Test");
        if (isTestPage) {
            WikiPage testPage = pageData.getWikiPage();
            StringBuffer newPageContent = new StringBuffer();
            includeSetupPages(testPage, newPageContent, isSuite);
            newPageContent.append(pageData.getContent());
            includeTeardownPages(testPage, newPageContent, isSuite);
            pageData.setContent(newPageContent.toString());
        }
        return pageData.getHtml();
    }
    
Now, it is much better! But the main question remains: What attributes should we give our functions that 
will a casual reader to intuit what it does easily?
    
Small
-----

Functions should be small! They should even be smaller than that! Actually, the code above is too large and
it should be shortened to this:

    :::java
    public static String renderPageWithSetupsAndTeardowns(PageData pageData, boolean isSuite) throws Exception {
        if (isTestPage(pageData))
            includeSetupAndTeardownPages(pageData, isSuite);
        return pageData.getHtml();
    }
    
How long? Uncle Bob says that they should hardly be 20 lines long.

Do One Thing
------------

Functions should do one thing. They should do it well. They should do it only.

The function `testableHtml()` is doing too many things:

    - Creating buffers
    - Fetching pages
    - Searching for inherited pages
    - Rendering paths
    - Generating HTML
    
On the other hand, the function `renderPageWithSetupsAndTeardowns()` is doing only one thing: Including setups and teardowns into test pages!

However, it can be hard to know what that one thing is. Hence, the next rule.

One level of abstraction per function
-------------------------------------

Let's see the following example to understand what one level of abstraction means.
Imagine we need to write a function that builds a house. That is, our function should answer the question of
"What needs to be done to build a house?". The answer would roughly be: find location, design, get permits, break ground and etc...
In code, it would look something like this: 

    :::python
    def buildHouse():
        find_location()
        design()
        fix_documents()
        break_ground()
        build_walls_and_roof()
        etc...()
        
This function does have only one level of abstraction. Everything inside the function is a part of the answer to the question of "how to build a house?".
To compare, take a look at the following:

    :::python
    def buildHouse():
        select_desirable_place()
        select_property()
        survey_property()
        consider_access_issues()
        
        consult_architect()
        design_utilities()
        design_efficiently()
        
        etc...()
        
Do you see it? The first 4 functions is not a part of the answer to the question: "What to do to build a house?", but rather "What to do to find a location to build a house?".
Do you see it now? They are 2 levels deep, not one! In real code, it would look much worse.

Use descriptive names
---------------------

The title says it all. Examples: is_testable(), includePages().
You know you are working on clean code when each function turns out to be pretty much what you expected.
 
In choosing a name, we should:
    - not be afraid to make a long name
    - not be afraid to spend time choosing a name
    - even try several different names and read the code with each in place
    - be consistent in our names

Follow these pieces of advice and your functions become much cleaner and more maintainable.

Fight on!
