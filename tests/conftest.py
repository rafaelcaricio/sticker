import os.path
import pytest

HERE = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR = os.path.join(HERE, 'fixtures')


@pytest.fixture()
def simple_api_get_spec():
    return os.path.join(FIXTURES_DIR, 'api_simple_get', 'api.yml')


@pytest.fixture(scope='class')
def simple_api_spec_attr(request):
    request.cls.simple_api_get_spec = simple_api_get_spec()
