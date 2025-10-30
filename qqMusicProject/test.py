import requests

cookies = {
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

headers = {
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
    # 'cookie': 'yyb_muid=23D7AC87621D683F1A56BA01631E6991; pgv_pvid=4223998579; RK=wml0GRiqvd; ptcz=405bb67b5bd517b8228c685b01ac9e95ae111dc336a1a868ad5e85f5330bda3b; qq_domain_video_guid_verify=d345530fc1397af9; _qimei_uuid42=19a100e1b21100022790af772eeae84c617662e72d; _qimei_i_3=58fd5186c00b5189c19ff830588727e6a2eff0f21a080b8bbd8b200e2fc6716f693536943c89e28189aa; fqm_pvqid=018518a8-49e0-4a5e-8e7b-8367965b9239; ts_refer=cn.bing.com/; ts_uid=3785047104; _ga=GA1.1.1619560827.1761031519; _ga_PF3XX5J8LE=GS2.1.s1761031519$o1$g0$t1761031520$j59$l0$h0; ptui_loginuin=3223607546; psrf_qqunionid=3986D8288F5ADDC7B1A780D5B7DDE09F; qm_keyst=Q_H_L_63k3Naar6MKPuE4qM1Az3S1Oq4SJriQxcg7FP82bL5ennvV4klHZSTc6M8ElvQxf58MYQF3Ua3twU7QXN_8LCxjCSurNcdw; wxopenid=; psrf_access_token_expiresAt=1766853843; wxrefresh_token=; music_ignore_pskey=202306271436Hn@vBj; qqmusic_key=Q_H_L_63k3Naar6MKPuE4qM1Az3S1Oq4SJriQxcg7FP82bL5ennvV4klHZSTc6M8ElvQxf58MYQF3Ua3twU7QXN_8LCxjCSurNcdw; tmeLoginType=2; euin=oi-AoiCz7i4P7c**; psrf_musickey_createtime=1761669843; psrf_qqopenid=B6DDF023DB5FAEC17BA21AF1BF9BFEB8; wxunionid=; psrf_qqrefresh_token=377590A6E99EEE6C6C7D1E75A4BAB76B; psrf_qqaccess_token=B793DD578C18CA7714DD49977BA719C2; uin=3223607546; fqm_sessionid=55a0a776-d9ba-453b-a460-48cdf71ac836; pgv_info=ssid=s6802235616; ts_last=y.qq.com/n/ryqq/player',
}

params = {
    '_': '1761726889562',
    'encoding': 'ag-1',
    'sign': 'zzc9bd96eau0dsghmk0yuyci5wlk0qe5ge62caa5bd',
}

data = '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'

response = requests.post('https://u6.y.qq.com/cgi-bin/musics.fcg', params=params, cookies=cookies, headers=headers, data=data).text
print(response)