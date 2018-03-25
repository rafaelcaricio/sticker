from sticker import SanicAPI


async def test_simple(simple_api_get_spec):
    api = SanicAPI(simple_api_get_spec)
    app = api.get_app(__name__)
    api_client = app.test_client

    request, response = api_client.get('/')
    assert response.status == 200
    assert (await response.content.read()) == 'Hello!'
