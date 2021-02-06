import requests
import datetime
import json

from utilities import create_HMAC
from const import shared_key, secret_Key, nep_organization, nep_enterprise_unit

date = datetime.datetime.now(datetime.timezone.utc)

url = "https://gateway-staging.ncrcloud.com/order/3/orders/1"
content_type = "application/json"


body = {
	"expireAt" : "2021-05-08T14:26:48Z",
	"comments" : "test"
    }

headers = {
    'content-type' : content_type,
    'Authorization' : create_HMAC(shared_key,
                                 secret_Key,
                                 date,
                                 "POST",
                                 url,
                                 content_type = content_type,
                                 nepOrganization = nep_organization),
    
    'nep-organization' : nep_organization,
    'nep-enterprise-unit' : nep_enterprise_unit,
    'date' : bytes(date.replace(microsecond=0).strftime("%a, %d %b %Y %H:%M:%S %Z"), 'utf-8')
    }

request = requests.post(url, data=json.dumps(body), headers = headers)

print(request.json())
