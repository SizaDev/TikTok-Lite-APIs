from urllib.parse import urlencode, unquote_plus
from hashlib import md5
#from alat_tiktok.ladon import Ladon
#from alat_tiktok.argus import Argus
import json
import random
import requests
import time 

class XGorgon:
    def __init__(self, url, data, cookie, ts):
        self._url   = url
        self.data   = data
        self.cookie = cookie
        self.ts = ts

    def calc_gorg(self):
     gorgon = ''

     if isinstance(self._url, str):
        url_md5 = md5(self._url.encode('utf-8')).hexdigest()
        gorgon += url_md5
     else:
        gorgon += '00000000000000000000000000000000'

     if self.data and isinstance(self.data, str):
        data_md5 = md5(self.data.encode('utf-8')).hexdigest()
        gorgon += data_md5
     else:
        gorgon += '00000000000000000000000000000000'

     if self.cookie and isinstance(self.cookie, str):
        cookie_md5 = md5(self.cookie.encode('utf-8')).hexdigest()
        gorgon += cookie_md5
     else:
        gorgon += '00000000000000000000000000000000'

     gorgon += '00000000000000000000000000000000'

     return self.calc_xg(gorgon)
    def calc_xg(self, data):
        len = 0x14
        key = [0xDF, 0x77, 0xB9, 0x40, 0xb9, 0x9b, 0x84, 0x83, 0xd1, 0xb9, 0xcb, 0xd1, 0xf7, 0xc2, 0xb9, 0x85, 0xc3, 0xd0, 0xfb, 0xc3]
        param_list = []
        for i in range(0, 12, 4):
            temp = data[8 * i: 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2:(j + 1) * 2], 16)
                param_list.append(H)
        param_list.extend([0x0, 0x6, 0xB, 0x1C])
        H = int(hex(self.ts), 16)
        param_list.append((H & 0xFF000000) >> 24)
        param_list.append((H & 0x00FF0000) >> 16)
        param_list.append((H & 0x0000FF00) >> 8)
        param_list.append((H & 0x000000FF) >> 0)
        eor_result_list = []
        for A, B in zip(param_list, key):
            eor_result_list.append(A ^ B)
        for i in range(len):
            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len]
            E = C ^ D
            F = self.RBIT(E)
            H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
            eor_result_list[i] = H
        result = ''
        for param in eor_result_list:
            result += self.hex_string(param)
        xgorgon = '0408b0d30000' + result
        return xgorgon
        
    def RBIT(self, num):
        result = ''
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8:
            tmp_string = '0' + tmp_string
        for i in range(0, 8):
            result = result + tmp_string[7 - i]
        return int(result, 2)
    
    def hex_string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = '0' + tmp_string
        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num)
        return int(tmp_string[1:] + tmp_string[:1], 16)
def encrypt_xor(string):
        return "".join([hex(ord(c) ^ 5)[2:] for c in string])
class TiktokLite:
    def __init__(self, tt_token=None, cookies=None):
        self.url = 'https://api22-normal-c-alisg.tiktokv.com'
        self.aweme = f"{self.url}/aweme/v1"
        self.lite = f"{self.url}/lite/v2"
        self.tt_token = tt_token
        self.cookies = cookies

    @staticmethod
    def encrypt_xor(string):
        return "".join([hex(ord(c) ^ 5)[2:] for c in string])

    def headers(self, params, data=None):
        openuiid, rticket, unix, device_id, platform, license_id, x_sdk_version, aid = ''.join(random.choices('0123456789abcdef', k=16)), int(time.time() * 1000), int(time.time()), '7323326935881844230', 0, 2142840551, '2.3.2.i18n', '1340'
        params_full = {
            "origin_type":"web", "request_source":"0",
            "manifest_version_code":"320815", "_rticket": rticket,
            "app_language":"en", "app_type":"normal",
            "iid":"7323771908776167173", "channel":"beta",
            "device_type":"M2007J20CG", "language":"en",
            "host_abi":"arm64-v8a", "locale":"en",
            "resolution":"1080*2309", "openudid": openuiid,
            "update_version_code":"320815", "ac2":"wifi5g",
            "cdid":"4a3f51f8-9925-4532-8086-2342edf0428c", "sys_region":"US",
            "os_api":"33", "timezone_name":"America/New_York", "dpi":"400", "ac":"wifi",
            "device_id": device_id, "os_version":"13",
            "timezone_offset":"-18000", "version_code":"320815",
            "app_name":"musically_go", "ab_version":"32.8.15", "version_name":"32.8.15", "device_brand":"POCO",
            "op_region":"US", "ssmix":"a", "device_platform":"android", "build_number":"32.8.15", "region":"US", "aid": aid,
            "ts": unix, "okhttp_version":"4.1.103.28-ul", "use_store_region_cookie":"1"
        }
        if params:
            params_full = f'{params}&{urlencode(params_full)}'
        x_ss_stub = md5(urlencode(data).encode()).hexdigest().upper() if data else data
        heads = {
            'x-tt-req-timeout': '90000',
            'accept-encoding': 'gzip',
            'sdk-version': '2',
            'passport-sdk-version': '30990',
            'x-tt-ultra-lite': '1',
            'x-vc-bdturing-sdk-version': x_sdk_version,
            'x-tt-store-region': 'id',
            'x-tt-store-region-src': 'uid',
            'user-agent': 'com.zhiliaoapp.musically.go/320815 (Linux; U; Android 13; en_US; M2007J20CG; Build/TQ3A.230805.001;tt-ok/3.12.13.2-alpha.68-quictest)',
#            'x-ladon': Ladon.encrypt(unix, license_id, aid),
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-khronos': str(unix),
#            'x-argus': Argus.get_sign(params_full, data=x_ss_stub, timestamp=unix,platform        = platform,    aid             = aid,license_id      = license_id,sec_device_id   = device_id,sdk_version     = x_sdk_version),
            'x-gorgon': XGorgon(url = params_full, data = x_ss_stub, cookie = self.cookies, ts=unix).calc_gorg()
        }
        if data:
            heads['x-ss-stub'] = x_ss_stub
        if self.tt_token:
            heads['cookie'] = self.cookies
            heads['x-tt-token'] = self.tt_token
        return {'params': params_full, 'head': heads}
    
    # aweme
    def detail(self, aweme_id='7320948264453295366', endpoint='aweme/detail/'):
        tools = self.headers(f'aweme_id={aweme_id}')
        response = requests.get(f"{self.aweme}/{endpoint}?{tools['params']}", headers=tools['head'])
        return response.text
     #   return json.dumps(response.json(), indent=5)
    
    def music(self, aweme_id='7322598975814798086', endpoint='music/detail/'):
        tools = self.headers(f'music_id={aweme_id}')
        print(tools['head'])
        response = requests.get(f"{self.aweme}/{endpoint}?{tools['params']}", headers=tools['head'])
        #return json.dumps(response.json(), indent=5)
        return response.status_code, response.text, response.headers

    def translate(self, f, t, text, endpoint='contents/translation/'):
        data = {'src_lang': f, 'trg_lang': t, 'translation_info': json.dumps([{'src_content': text}])}
        tools = self.headers('scene=2', data=data)
        response = requests.post(f"{self.aweme}/{endpoint}?{tools['params']}", headers=tools['head'], data=data)
        # ' '.join([x['translated_content'] for x in response.json()['translated_content_list']])
        return json.dumps(response.json(), indent=5)
    
    def sorten(self, target, vm=False):
        if vm:
            data = {'share_url': target, 'platform_id': 'copy', 'scene': '2'}
            tools = self.headers('request_tag_from=5', data)
            response = requests.post(f"https://api22-normal-c-alisg.tiktokv.com/tiktok/share/link/shorten/v1/?{tools['params']}", headers=tools['head'], data=data)
        else:
            tools = self.headers(f'target={target}&belong=trill')
            response = requests.get(f"https://api22-normal-c-alisg.tiktokv.com/shorten/?{tools['params']}", headers=tools['head'])
        return json.dumps(response.json(), indent=5)
    
    # lite
    def comment(self, aweme_id, text, endpoint='comment/publication/'):
        data = {'aweme_id': aweme_id, 'text': unquote_plus(text), 'text_extra': []}
        tools = self.headers('', data=data)
        response = requests.post(f"{self.lite}/{endpoint}?{tools['params']}", headers=tools['head'], data=data)
        # return json.dumps(response.json(), indent=5)
        return response.headers, response.text

    # login 
    def login(self, endpoint='passport/user/login/', email=encrypt_xor('ckdj9o4rad@txcct.com'),password=encrypt_xor('UXlEUKJrHBK1!')):
        data = {'password': password, 'account_sdk_source': 'app', 'email': email, 'mix_mode': '1'}
        tools = self.headers('', data=data)
        response = requests.post(f"{self.url}/{endpoint}?{tools['params']}", headers=tools['head'], data=data)
        return json.dumps(response.json(), indent=5)

    # create account
    def register(self, email='666461646b62646b34456468646b6a716064682b666a68', password='64716469643437362f26', endpoint='passport/email/register/v2/'):
        data = {
            "birthday":"1979-12-14",
            "rules_version":"v2",
            "password": password,
            "fixed_mix_mode":"1",
            "account_sdk_source":"app",
            "mix_mode":"1",
            "email": email
        }
        tools = self.headers('',data=data)
        response = requests.post(f"{self.url}/{endpoint}?{tools['params']}", headers=tools['head'], data=data)
        return response.text

if __name__ == '__main__':
    tt_token = '037c56df62e308b682a0595cd1ea545fa60494db048f49ccd6f609d0a40a0a7d6d133c41162aa2bba3af91d4943f3283ee78b11eabbe3ba16743819244b2634d5a5be902ae6d1ec719b8354e95b0b9783cd39ad106319b97ea2be2130751ef8ac611e-CkBkMTZlODA2ZmE5ZDVhODM3YWNjN2ZlNzdiZmJkODY5YWE1MmJmZTIwOGRhOGY3NzhiZWQxNzU2YjI0ZTVmYjMy-2.0.0'
    cookies= ''

    tiktok = TiktokLite()
#    detail = tiktok.detail('7376786318874938630')
#    music = tiktok.music()
#    sorten = tiktok.sorten('https://www.tiktok.com/@kumbangkelana051/video/7322701558695709960', vm=True)
#     translate = tiktok.translate('id', 'en', 'kmu jahat')
#    comment = tiktok.comment(text='kasihan banget', aweme_id='7322701558695709960') 
    login = tiktok.login()
#    register = tiktok.register()
    print(login)