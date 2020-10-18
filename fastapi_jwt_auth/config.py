from datetime import timedelta
from typing import Optional, Union, Sequence, List
from types import GeneratorType
from pydantic import (
    BaseModel,
    root_validator,
    validator,
    StrictBool,
    StrictInt,
    StrictStr
)

class LoadConfig(BaseModel):
    authjwt_secret_key: Optional[StrictStr] = None
    authjwt_public_key: Optional[StrictStr] = None
    authjwt_private_key: Optional[StrictStr] = None
    authjwt_algorithm: Optional[StrictStr] = "HS256"
    authjwt_decode_algorithms: Optional[List[StrictStr]] = None
    authjwt_decode_leeway: Optional[Union[StrictInt,timedelta]] = 0
    authjwt_encode_issuer: Optional[StrictStr] = None
    authjwt_decode_issuer: Optional[StrictStr] = None
    authjwt_decode_audience: Optional[Union[StrictStr,Sequence[StrictStr]]] = None
    authjwt_blacklist_enabled: Optional[StrictStr] = None
    authjwt_blacklist_token_checks: Optional[Sequence[StrictStr]] = {'access','refresh'}
    authjwt_header_name: Optional[StrictStr] = "Authorization"
    authjwt_header_type: Optional[StrictStr] = "Bearer"
    authjwt_access_token_expires: Optional[Union[StrictBool,StrictInt,timedelta]] = timedelta(minutes=15)
    authjwt_refresh_token_expires: Optional[Union[StrictBool,StrictInt,timedelta]] = timedelta(days=30)

    @root_validator(pre=True)
    def validate_blacklist_enabled(cls, values):
        _secret_key = values.get("authjwt_secret_key")
        _public_key = values.get("authjwt_public_key")
        _private_key = values.get("authjwt_private_key")
        _algorithm = values.get("authjwt_algorithm")
        _decode_algorithms = values.get("authjwt_decode_algorithms")
        _decode_leeway = values.get("authjwt_decode_leeway")
        _encode_issuer = values.get("authjwt_encode_issuer")
        _decode_issuer = values.get("authjwt_decode_issuer")
        _decode_audience = values.get("authjwt_decode_audience")
        _blacklist_enabled = values.get("authjwt_blacklist_enabled")
        _blacklist_token_checks = values.get("authjwt_blacklist_token_checks")
        _header_name = values.get("authjwt_header_name")
        _header_type = values.get("authjwt_header_type")
        _access_token_expires = values.get("authjwt_access_token_expires")
        _refresh_token_expires = values.get("authjwt_refresh_token_expires")

        if _secret_key and not isinstance(_secret_key, str):
            raise TypeError("The 'AUTHJWT_SECRET_KEY' must be a string")

        if _public_key and not isinstance(_public_key, str):
            raise TypeError("The 'AUTHJWT_PUBLIC_KEY' must be a string")

        if _private_key and not isinstance(_private_key, str):
            raise TypeError("The 'AUTHJWT_PRIVATE_KEY' must be a string")

        if _algorithm and not isinstance(_algorithm, str):
            raise TypeError("The 'AUTHJWT_ALGORITHM' must be a string")

        if _decode_algorithms and not isinstance(_decode_algorithms, list):
            raise TypeError("The 'AUTHJWT_DECODE_ALGORITHMS' must be a list")

        if _decode_leeway and not isinstance(_decode_leeway, (timedelta, int)):
            raise TypeError("The 'AUTHJWT_DECODE_LEEWAY' must be a timedelta or integer")

        if _encode_issuer and not isinstance(_encode_issuer, str):
            raise TypeError("The 'AUTHJWT_ENCODE_ISSUER' must be a string")

        if _decode_issuer and not isinstance(_decode_issuer, str):
            raise TypeError("The 'AUTHJWT_DECODE_ISSUER' must be a string")

        if (
            _decode_audience and
            not isinstance(_decode_audience, (str, list, tuple, set, frozenset, GeneratorType))
        ):
            raise TypeError("The 'AUTHJWT_DECODE_AUDIENCE' must be a string or sequence")

        if _blacklist_enabled and _blacklist_enabled not in ['true','false']:
            raise TypeError("The 'AUTHJWT_BLACKLIST_ENABLED' must be between 'true' or 'false'")

        if (
            _blacklist_token_checks and
            not isinstance(_blacklist_token_checks, (list, tuple, set, frozenset, GeneratorType))
        ):
            raise TypeError("The 'AUTHJWT_BLACKLIST_TOKEN_CHECKS' must be a sequence")

        if _header_name and not isinstance(_header_name, str):
            raise TypeError("The 'AUTHJWT_HEADER_NAME' must be a string")

        if _header_type and not isinstance(_header_type, str):
            raise TypeError("The 'AUTHJWT_HEADER_TYPE' must be a string")

        if _access_token_expires and not isinstance(_access_token_expires, (timedelta,int,bool)):
            raise TypeError("The 'AUTHJWT_ACCESS_TOKEN_EXPIRES' must be between timedelta, int, bool")

        if _access_token_expires and _access_token_expires is True:
            raise TypeError("The 'AUTHJWT_ACCESS_TOKEN_EXPIRES' only accept value False")

        if _refresh_token_expires and not isinstance(_refresh_token_expires, (timedelta,int,bool)):
            raise TypeError("The 'AUTHJWT_REFRESH_TOKEN_EXPIRES' must be between timedelta, int, bool")

        if _refresh_token_expires and _refresh_token_expires is True:
            raise TypeError("The 'AUTHJWT_REFRESH_TOKEN_EXPIRES' only accept value False")

        return values

    @validator('authjwt_blacklist_token_checks', each_item=True)
    def validate_blacklist_token_checks(cls, v):
        if v not in ['access','refresh']:
            raise ValueError("The 'AUTHJWT_BLACKLIST_TOKEN_CHECKS' must be between 'access' or 'refresh'")

        return v

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True
