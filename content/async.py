import asyncio
import aiohttp

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)


async def get_content(pid, url):
    async with session.get(url) as response:
        content = await response.read()
        print(pid, content)

loop.create_task(get_content(1, 'http://asyncio.readthedocs.io/'))
loop.create_task(get_content(2, 'http://asyncio.readthedocs.io/'))
loop.create_task(get_content(3, 'http://asyncio.readthedocs.io/'))
loop.create_task(get_content(4, 'http://asyncio.readthedocs.io/'))
loop.create_task(get_content(5, 'http://asyncio.readthedocs.io/'))

# loop.run_until_complete(get_content('http://asyncio.readthedocs.io/'))
# loop.run_until_complete(get_content('http://asyncio.readthedocs.io/'))
# loop.run_until_complete(get_content('http://asyncio.readthedocs.io/'))
# loop.run_until_complete(get_content('http://asyncio.readthedocs.io/'))
# loop.run_until_complete(get_content('http://asyncio.readthedocs.io/'))
# loop.run_until_complete(get_content('http://asyncio.readthedocs.io/'))
# loop.run_until_complete(get_content('http://asyncio.readthedocs.io/'))
# loop.run_until_complete(get_content('http://asyncio.readthedocs.io/'))

# session.close()
loop.run_forever()
