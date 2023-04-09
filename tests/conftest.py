import pytest


from manager import webdriver_manager


@pytest.fixture(scope='session', autouse=True)
def setup_driver(request):
    return webdriver_manager.get_driver()
