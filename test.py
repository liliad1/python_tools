import hashlib
import json
import re
import time
import urllib
from urllib.parse import unquote

import requests

APPKEY = '12574478'
DATA = '{"source": "darenhome", "type": "h5", "userId": "667241583", "page": 1, "tab": "10004"}'
URL = 'https://h5api.m.taobao.com/h5/mtop.taobao.maserati.darenhome.feed/1.0/'
params = {'jsv': '2.5.6', 'appKey': APPKEY, 't': int(time.time() * 1000),
          'sign': 'FAKE_SIGN_WITH_ANYTHING', 'api': 'mtop.taobao.maserati.darenhome.feed', 'v': '1.0',
          'preventFallback': True,
          'type': 'jsonp', 'dataType': 'jsonp', 'callback': 'mtopjsonp', 'a': '上海', 'b': '悠悠',
          'data': DATA}
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 ' + \
                  '(KHTML, like Gecko) Version/9.0 Mobile/13G35 Safari/601.1'
}
images = []
try:
    DATA1 = {"contentId": "", "source": "darenhome", "type": "h5",
             "params": "{\"sourcePageName\":\"darenhome\"}", "business_spm": "", "track_params": ""}
    URL1 = 'https://h5api.m.taobao.com/h5/mtop.taobao.beehive.detail.contentservicenewv2/1.0/'
    params1 = {'jsv': '2.5.1', 'appKey': APPKEY, 't': int(time.time() * 1000),
               'sign': 'FAKE_SIGN_WITH_ANYTHING', 'api': 'mtop.taobao.beehive.detail.contentservicenewv2', 'v': '1.0',
               'AntiCreep': True, 'AntiFlood': True, 'timeout': 5000,
               'type': 'jsonp', 'dataType': 'jsonp', 'callback': 'mtopjsonp1', 'a': '上海', 'b': '悠悠',
               'data': DATA1}
    # get token in first request
    r1 = requests.get(URL, params=params, headers=headers)
    token_with_time = r1.cookies.get('_m_h5_tk')
    token = token_with_time.split('_')[0]
    enc_token = r1.cookies.get('_m_h5_tk_enc')
    # get results in second request
    t2 = str(int(time.time() * 1000))
    c = '&'.join([token, t2, APPKEY, DATA])
    m = hashlib.md5()
    m.update(c.encode('utf-8'))
    params.update({'t': t2, 'sign': m.hexdigest()})
    cookies = {'_m_h5_tk': token_with_time, '_m_h5_tk_enc': enc_token}
    r2 = requests.get(URL, params=params, headers=headers, cookies=cookies)
    items = json.loads(r2.text[11:len(r2.text) - 1]).get('data').get('result').get('data').get('feeds')
    # print(json.loads(r2.text[11:len(r2.text) - 1]).get('data').get('result').get('data').get('feeds')[0].get('items'))
    for item in items:
        print(item.get('cover'))
        print(item.get('summary'))
        print(item.get('url'))
        r3 = requests.get(item.get('url'))
        print(r3.text)
        r4 = requests.get(URL1, params=params1, headers=headers, cookies=cookies)
    # print(r2.request.url)
    # json_text = re.match(r'(.*\()(.*)(\))', r2.text).group(2)
    # images = dict(json.loads(json_text))['data']['images']
except Exception as e:
    print(e)
