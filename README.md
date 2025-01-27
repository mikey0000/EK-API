# Electric Kiwi Python API

[![SemVer 0.8.5][img_version]][url_version]
[![PyPI Releases][img_pypi]][url_pypi]
[![Supported Python Versions][img_pyversions]][url_pyversions]

[img_version]: https://img.shields.io/static/v1.svg?label=SemVer&message=0.8.5&color=blue
[url_version]: https://pypi.org/project/electrickiwi-api/

[img_pypi]: https://img.shields.io/badge/PyPI-wheels-green.svg
[url_pypi]: https://pypi.org/project/electrickiwi-api/#files

[img_pyversions]: https://img.shields.io/pypi/pyversions/electrickiwi-api.svg
[url_pyversions]: https://pypi.python.org/pypi/electrickiwi-api

## What it does
Provide a simple API interface to the Electric Kiwi API and includes all endpoints available on the juice hacker site

## What it does not
session management / token management, there are enough libraries and frameworks that
already do this very well, no point reinventing the wheel

Authentication has been left to you. 

If you are planning on joining Electric Kiwi use my link to score a $50 credit
[sign up link](https://www.electrickiwi.co.nz/RAFaMwYjGd)

## Authentication

To make any requests to the token url you are required to have basic auth using the client id and secret
same as the python api example.


## How to use it

implement AbstractAuth (see test_instance.py in tests)

once implemented you can pass it to `ElectricKiwiApi`
e.g

```python
api = ElectricKiwiApi(ApiAuthImpl(session))
await api.get_active_session()
await api.set_active_session()
```

You will need to call api.set_active_session() 
to set the customer number and connection id for you to run additional API calls
as it sets them on the class so your not passing them continuously.
