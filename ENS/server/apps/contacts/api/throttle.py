from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle,
)


class GetThrottle(AnonRateThrottle,
                  UserRateThrottle):
    rate = '1/s'


class CreateThrottle(AnonRateThrottle,
                     UserRateThrottle):
    rate = '10/m'