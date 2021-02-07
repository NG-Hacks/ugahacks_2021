
import requests
import datetime

from const import shared_key, secret_Key, nep_organization, nep_enterprise_unit
from utilities import create_HMAC

content_type = 'application/json'
method = 'POST'
order_service = 'https://gateway-staging.ncrcloud.com/order/3/orders/1'

url = f'{order_service}/find'
url_p = f'{order_service}/find?pageSize=1000'

date = datetime.datetime.now(datetime.timezone.utc)
auth = create_HMAC(shared_key,
                   secret_Key,
                   date,
                   method,
                   url,
                   content_type=content_type,
                   nepOrganization=nep_organization)

headers = {
    'content-type': content_type,
    'Authorization': auth,
    'nep-organization': nep_organization,
    'nep-enterprise-unit': nep_enterprise_unit,
    'date': bytes(date.replace(microsecond=0).strftime('%a, %d %b %Y %H:%M:%S %Z'), 'utf-8')
}

# this works
resp = requests.post(url, data="{}", headers=headers)

print(resp.status_code)
print(resp.json())

resp = requests.post(url_p, data="{}", headers=headers)

print(resp.status_code)
print(resp.json())

resp = requests.post(url, data="{}", headers=headers,
                     params={"pageSize": "1000"})

print(resp.status_code)
print(resp.json())
