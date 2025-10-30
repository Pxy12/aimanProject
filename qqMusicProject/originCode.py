import subprocess
from functools import partial
from pprint import pprint

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')  # 要置于开头，才能设置子进程编码一致
import json
import time
import base64
import requests
import execjs


class qq_music_api:
    def __init__(self):
        self.cookies = {
            'yyb_muid': '23D7AC87621D683F1A56BA01631E6991',
            'pgv_pvid': '4223998579',
            'RK': 'wml0GRiqvd',
            'ptcz': '405bb67b5bd517b8228c685b01ac9e95ae111dc336a1a868ad5e85f5330bda3b',
            'qq_domain_video_guid_verify': 'd345530fc1397af9',
            '_qimei_uuid42': '19a100e1b21100022790af772eeae84c617662e72d',
            '_qimei_i_3': '58fd5186c00b5189c19ff830588727e6a2eff0f21a080b8bbd8b200e2fc6716f693536943c89e28189aa',
            'fqm_pvqid': '018518a8-49e0-4a5e-8e7b-8367965b9239',
            'ts_refer': 'cn.bing.com/',
            'ts_uid': '3785047104',
            '_ga': 'GA1.1.1619560827.1761031519',
            '_ga_PF3XX5J8LE': 'GS2.1.s1761031519$o1$g0$t1761031520$j59$l0$h0',
            'ptui_loginuin': '3223607546',
            'psrf_qqunionid': '3986D8288F5ADDC7B1A780D5B7DDE09F',
            'qm_keyst': 'Q_H_L_63k3Naar6MKPuE4qM1Az3S1Oq4SJriQxcg7FP82bL5ennvV4klHZSTc6M8ElvQxf58MYQF3Ua3twU7QXN_8LCxjCSurNcdw',
            'wxopenid': '',
            'psrf_access_token_expiresAt': '1766853843',
            'wxrefresh_token': '',
            'music_ignore_pskey': '202306271436Hn@vBj',
            'qqmusic_key': 'Q_H_L_63k3Naar6MKPuE4qM1Az3S1Oq4SJriQxcg7FP82bL5ennvV4klHZSTc6M8ElvQxf58MYQF3Ua3twU7QXN_8LCxjCSurNcdw',
            'tmeLoginType': '2',
            'euin': 'oi-AoiCz7i4P7c**',
            'psrf_musickey_createtime': '1761669843',
            'psrf_qqopenid': 'B6DDF023DB5FAEC17BA21AF1BF9BFEB8',
            'wxunionid': '',
            'psrf_qqrefresh_token': '377590A6E99EEE6C6C7D1E75A4BAB76B',
            'psrf_qqaccess_token': 'B793DD578C18CA7714DD49977BA719C2',
            'uin': '3223607546',
            'fqm_sessionid': '55a0a776-d9ba-453b-a460-48cdf71ac836',
            'pgv_info': 'ssid=s6802235616',
            'ts_last': 'y.qq.com/n/ryqq/player',
        }

        self.headers = {
            'accept': 'application/octet-stream',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-type': 'text/plain',
            'origin': 'https://y.qq.com',
            'priority': 'u=1, i',
            'referer': 'https://y.qq.com/',
            'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
        }



    def run_node_script(self, data):
        """
        执行Node.js脚本获取签名和加密数据
        """
        try:
            result = subprocess.run(
                ['node', "main.js", json.dumps(data).replace(" ", "")],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
                timeout=30
            )
            return result.stdout
        except subprocess.TimeoutExpired:
            print("Node.js脚本执行超时！")
            return None
        except subprocess.CalledProcessError as e:
            print(f"Node.js脚本执行出错，返回码：{e.returncode}")
            print(f"错误信息：{e.stderr}")
            return None

    def decrypt_response(self, encrypted_data):
        """
        解密响应数据
        """
        listPath = "dataDecrypt.js"
        jscode = ''
        with open(listPath, 'r', encoding="utf-8") as f:
            jscode += f.read()
        js = execjs.compile(jscode)
        return js.call('songData', encrypted_data)

    # 解析响应数据函数
    def search_music(self,search_data):

        # 执行Node.js脚本获取签名和加密数据
        res = self.run_node_script(search_data)
        if res is None:
            return None

        sign = res.split('\n')[0]
        encrypt = res.split('\n')[1]

        # print("sign:", sign)
        # print("encrypt:", encrypt)

        # 获取当前时间戳
        current_time = str(int(time.time() * 1000))
        # print(current_time)

        # 构建请求参数
        params = {
            '_': current_time,
            'encoding': 'ag-1',
            'sign': sign,
        }

        # 发送请求
        response = requests.post(
            'https://u6.y.qq.com/cgi-bin/musics.fcg',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=encrypt
        )

        # 解密响应数据
        encrypted_response = base64.b64encode(response.content).decode()
        result = self.decrypt_response(encrypted_response)
        return result


# 使用示例
# if __name__ == "__main__":
#     data1 = {"comm": {"cv": 4747474, "ct": 24, "format": "json", "inCharset": "utf-8", "outCharset": "utf-8",
#                       "notice": 0,
#                       "platform": "yqq.json", "needNewCode": 1, "uin": 3223607546,
#                       "g_tk_new_20200303": 1188746000,
#                       "g_tk": 1188746000},
#              "req_1": {"method": "DoSearchForQQMusicDesktop", "module": "music.search.SearchCgiService",
#                        "param": {"remoteplace": "txt.yqq.top", "searchid": "61292176913318089",
#                                  "search_type": 0,
#                                  "query": '周杰伦', "page_num": 1, "num_per_page": 30}}}
#     qq_music = qq_music_api(data1)
#     # 搜索周杰伦的音乐，第2页，每页60条
#     search_result = qq_music.search_music()
#     pprint(search_result)

# 搜索其他歌手
# search_result = qq_music.search_music("林俊杰", 1, 20)
# print(search_result)
