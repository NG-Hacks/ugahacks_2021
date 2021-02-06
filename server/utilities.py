# this is meant to be copied and used in your project to authenticate to the NCR Business Services Platform
#
# Disclaimer: This is not proper python format, but it has been reduced for ease of integration for those not
# familiar with the BSP or python
#
# createHMAC
#
# Arguments:
# shared_key - user's shared key
# secret_key - user's secret key
# date - date value in ISO-8601 format (literally: datetime.datetime.now(datetime.timezone.utc))
# http_method - GET, POST, PUT, PATCH, etc.
# requestURL - full url of the request
# content_type - content-type header from request (optional, unless required by API documentation)
# contentMD5 - contentMD5 header from request (optional, unless required by API documentation)
# nepApplicationKey - nepApplicationKey header from request (optional, unless required by API documentation)
# nepCorrelationID - nepCorrelationID header from request (optional, unless required by API documentation)
# nepOrganization - nepOrganization header from request (optional, unless required by API documentation)
# nepServiceVersion - nepServiceVersion header from request (optional, unless required by API documentation)
#
# returns the value for the Authorization header on a BSP API request

import base64
import hashlib
import hmac
import urllib


def create_HMAC(shared_key,
                secret_key,
                date_header,
                http_method,
                requestURL,
                content_type=None,
                contentMD5=None,
                nepApplicationKey=None,
                nepCorrelationID=None,
                nepOrganization=None,
                nepServiceVersion=None):
    toSign = http_method + "\n" + urllib.parse.urlsplit(requestURL).path
    if content_type is not None:
        toSign += "\n" + content_type

    if contentMD5 is not None:
        toSign += "\n" + contentMD5

    if nepApplicationKey is not None:
        toSign += "\n" + nepApplicationKey

    if nepCorrelationID is not None:
        toSign += "\n" + nepCorrelationID

    if nepOrganization is not None:
        toSign += "\n" + nepOrganization

    if nepServiceVersion is not None:
        toSign += "\n" + nepServiceVersion

    key = bytes(secret_key + date_header.replace(microsecond=0)
                .strftime("%Y-%m-%dT%H:%M:%S.000Z"), 'utf-8')

    message = bytes(toSign, 'utf-8')

    digest = hmac.new(key, msg=bytes(message),
                      digestmod=hashlib.sha512).digest()

    signature = base64.b64encode(digest)

    return "AccessKey {}:{}".format(shared_key, signature.decode('ascii'))
