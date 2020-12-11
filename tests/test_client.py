from pygiftbit.giftbit import Client
from pygiftbit.errors import APIError, KeyLengthError, RegionError, AuthError
import pytest


def test_auth_error():
    with pytest.raises(AuthError):
        Client(api_key='a' * 258)


def test_key_length_assertion():
    with pytest.raises(KeyLengthError):
        Client(api_key='bad_key')


def test_auth_success():
    client = Client()
    assert "Authenticated as" in client.__str__()


def test_region_error():
    with pytest.raises(RegionError):
        Client().get_brand_codes(region=256)


def test_brands_returned():
    brands = Client().get_brand_codes(region=1, search='golf')
    assert len(brands) == 1
    assert brands[0] == 'venuegolfca'


def test_api_error_raise():
    client = Client()
    client.headers['SIMULATE-RATELIMIT'] = 'true'
    with pytest.raises(APIError) as err:
        client.list_regions()
    assert 'ERROR_TOO_MANY_REQUESTS' in err.value.message
