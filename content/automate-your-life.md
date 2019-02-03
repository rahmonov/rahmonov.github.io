Title: You are a programmer, automate your life already!
Date: 2019-02-03 20:10
Modified: 2019-02-03 20:10
Category: automation
Tags: programming
Slug: automate-your-life
Authors: Jahongir Rahmonov
Summary: Who likes doing mundane manual tasks over and over again every day? Automate them!

Hello, how are you? I have missed you. I haven't blogged for a long time now. But I have prepared something good for you to compensate.

Today, we will automate a boring task that I have been doing manually for a very long time now.

An inspiration for this blog post came from [Nina Zakharenko](https://twitter.com/nnja), Senior Cloud Developer Advocate at Microsoft, who recently tweeted the following:

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">My personal <a href="https://twitter.com/AppleSupport?ref_src=twsrc%5Etfw">@AppleSupport</a> laptop has been in and out of the shop most of Nov / Dec and part of January.<br><br>On the bright side... I made a handy script to set up a new computer &amp; configure from scratch since I&#39;ve had to do it over and over<br><br>Check it out here:<a href="https://t.co/qTgp7UOwYi">https://t.co/qTgp7UOwYi</a></p>&mdash; 𝙽𝚒𝚗𝚊 𝚉𝚊𝚔𝚑𝚊𝚛𝚎𝚗𝚔𝚘 💖🐍 (@nnja) <a href="https://twitter.com/nnja/status/1087464173016047616?ref_src=twsrc%5Etfw">January 21, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

I was like "Wow! People do that? I am a developer as well. I have got to automate something too". Then, I asked myself "what is something that I do every single day over and over again?".
The answer was pretty simple. When I come to work, I do these things every day with no exception:

1. Open PyCharm with our main project.
2. Start Docker
3. Open iTerm
4. Start Docker-Compose for our main project so that I have the project running on my browser.

So I decided to write a script that does these things for me automatically. Disclaimer: you don't have to know any of these things. You can use them as a general reference and customize it for your needs.
Also, I am on a macOS, so if you have a different OS, the script will probably need to be changed a little.

With everything out of the way, let's get this done.

Of course, the easiest way to automate such a thing is writing a shell script. So, create a file "shockingly" called `start_day.sh` and put a shebang line on the top:

```shell
#!/usr/bin/env bash
```

The first thing that we want to do is to start PyCharm with our project open. In order to start PyCharm from the command line, you need to enable the so called `Command-Line Launcher`:

1. Open Pycharm
2. Find tools in the menu bar
3. Click Create Command-line Launcher
4. Leave the default which is `/usr/local/bin/charm` and click `OK`.

Now you can open PyCharm with the help of the `charm` command. Try it in your terminal and see if it works. Now let's use this knowledge and write the first command in your `start_day.sh` script:

```shell
#!/usr/bin/env bash

charm /path/to/your/project/
```

Make sure to change the path correctly.

Let's run this script now. In order to do that, we need to make it executable. In your terminal, do the following:

```shell
chmod +x start_day.sh
```

Now that it is executable, we can run it like so:

```shell
./start_day.sh
```

It should open PyCharm with your project ready. Yay! First step is done! On to the next.

The next step is pretty easy. We need to start `Docker`. On macOS, you can easily open any application in terminal with the following command:

```shell
open -a ApplicationName
```

Let's include that in our script to have this:

```shell
#!/usr/bin/env bash

charm /path/to/your/project/
open -a Docker
```

Run the script again and you will see that after PyCharm opens, Docker starts as well. Cool!

The next step is the most interesting one. We need to go to our project folder and do `docker-compose up`. However, there is a catch.
Our script will execute very fast but `Docker` that we started above takes around 20 seconds to start. Thus, if we immediately do `docker-compose up`, it will fail saying that
`Docker` hasn't started yet. Here is the script, run it and see for yourself:

```shell
#!/usr/bin/env bash

charm /path/to/your/project/
open -a Docker
cd /path/to/your/project/
docker-compose up
```

We could tell it to `sleep()` for some hard-coded amount of time so that `Docker` has enough time to start:

```shell
#!/usr/bin/env bash

charm /path/to/your/project/
open -a Docker
cd /path/to/your/project/
sleep 25
docker-compose up
```

Obviously this is not a good solution and the sleep time will vary from machine to machine. Thus, we need to know when Docker fully starts and then run `docker-compose`.

Here is what we will do. We will run any `Docker` command and see if it ran successfully meaning that `Docker` has started. If it is not successful, it means that `Docker` hasn't started yet and thus
we will tell it to try again after 1 second. We will try this in a loop until it is successful. When it finally runs successfully, we can call our `docker-compose up` command.

Here is the part that waits for `Docker` to start:

```shell
while (! docker stats --no-stream);
    do echo 'Waiting for Docker to launch...';
    sleep 1;
done
```

In a while loop, it tries to get docker stats. It continues running as long as that command returns a falsy result. Only after it returns a truthy result, the while loop ends and the script can continue.

We have all the pieces of the puzzle now and we can put it together:

```shell
#!/usr/bin/env bash

charm /path/to/your/project/
open -a Docker
cd /path/to/your/project/

while (! docker stats --no-stream);
    do echo 'Waiting for Docker to launch...';
    sleep 1;
done

docker-compose up
```

That's it! Now try running it and you will see this "robot" will do everything for you.

## Conclusion

In this blog post, we wrote a small bash script to automate my start of the day. This is how I start my day at work now. I come to work, open iTerm, run this script and go have some coffee until everything is ready for me.
This is not a difficult script and task. However, it still feels good. I was inspired by Nina Zakharenko and now I hope that this will serve as an inspiration to somebody as well.
I am extremely interested in what you automated in your workflow. Let me know in the comments.

Fight on!
