# __init__.py

# version of ElectricKiwiApi for Python
__version__ = "0.10.0"

from electrickiwi_api.api import (
    ElectricKiwiEndpoint,
    ElectricKiwiApi
)

from electrickiwi_api.auth import (
    AbstractAuth
)

from electrickiwi_api.util import (
    NZ_TZ,
    interval_start
)

# for production
# Authorization URL 	https://welcome.electrickiwi.co.nz/oauth/authorize
# Token URL 	https://welcome.electrickiwi.co.nz/oauth/token
# API 	https://api.electrickiwi.co.nz
