import aiohttp


async def fetch(session, url):
    """
    Use session object to perform 'get' request on url
    """
    async with session.get(url) as result:
        return await result.json()


async def handle_request(params):
    url = "https://api.github.com/repos/channelcat/sanic"

    async with aiohttp.ClientSession() as session:
        result = await fetch(session, url)

    return {'content': result}


if __name__ == '__main__':
    from sticker import SanicAPI
    api = SanicAPI('async_api.yml')
    app = api.get_app(__name__)
    app.run(host="0.0.0.0", port=8000, workers=2)
