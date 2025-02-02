# __init__.py

# version of ElectricKiwiApi for Python
__version__ = "0.9.11"

from electrickiwi_api.api import (
    ElectricKiwiEndpoint,
    ElectricKiwiApi
)

from electrickiwi_api.auth import (
    AbstractAuth
)

# for production
# Authorization URL 	https://welcome.electrickiwi.co.nz/oauth/authorize
# Token URL 	https://welcome.electrickiwi.co.nz/oauth/token
# API 	https://api.electrickiwi.co.nz
