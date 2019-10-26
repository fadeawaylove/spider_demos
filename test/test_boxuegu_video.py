import requests
import urllib.parse
import time
from Crypto.Cipher import AES


class BoXueGuSpider(object):
    base_url = "https://cd15-ccd1-2.play.bokecc.com/flvs/78665FEF083498AB/2019-02-14"

    m3u8_url = "https://cd15-ccd1-2.play.bokecc.com/flvs/78665FEF083498AB/2019-02-14/030F2A399BAAA55C9C33DC5901307461-20.m3u8"
    m3u8_params = {
        't': '1572071585',
        'key': '51DDA99488B2EB16ACF707B43E4A5B0A',
        'tpl': '10',
        'tpt': '112'
    }
    m3u8_headers = {
        "Origin": "https://xuexi.boxuegu.com",
        "Referer": "https://xuexi.boxuegu.com/video.html?courseId=1139&moduleId=101885&type=PATH&phaseId=755",
        "Sec-Fetch-Mode": "cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    }

    def __init__(self):
        pass

    def run(self):
        self.decode_ts_file()

    def parse_m3u8(self):
        """解析m3ub文件得到ts文件的url地址"""
        resp = requests.get("https://cd15-ccd1-2.play.bokecc.com/flvs/78665FEF083498AB/2019-02-14/030F2A399BAAA55C9C33DC5901307461-20.m3u8?t=1572084661&key=A0D7442ECC6F853094F8A0EEC9A23401&tpl=10&tpt=112", headers=self.m3u8_headers)
        resp_data = resp.text
        lines = resp_data.splitlines()
        for line in lines:
            if not line.startswith("#"):
                path = line
                ts_url = self.base_url + "/" + path
                yield ts_url

    def decode_ts_file(self):
        # key = " ):   _ 0 Z3wb".encode("utf8")
        key = b'\x00\x0c):\x98\xa9\xa6_\x9f0\xdfZ\x023wb'
        for i, ts_url in enumerate(self.parse_m3u8()):
            print("begin: {}".format(ts_url))
            resp = requests.get(ts_url, headers=self.m3u8_headers)
            with open("{}.ts".format(i), "ab") as f:
                f.write(self.aes_decode(resp.content, key))
            time.sleep(5)

    def aes_decode(self, data, key):
        """AES解密
        :param key:  密钥（16.32）一般16的倍数
        :param data:  要解密的数据
        :return:  处理好的数据
        """
        cryptor = AES.new(key, AES.MODE_CBC, key)
        plain_text = cryptor.decrypt(data)
        return plain_text.rstrip(b'\0')  # .decode("utf-8")


if __name__ == "__main__":
    b = BoXueGuSpider()
    b.run()
