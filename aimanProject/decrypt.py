import json
import subprocess
import requests
import os
import sys

# 设置编码环境变量
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# 执行JavaScript代码调用dataFilter函数解密数据
def decrypt_data_with_js(encrypted_data):
    print(f"\n=== 开始解密数据 ===")
    
    # 构建JavaScript代码
    js_code = f'''
    // 设置UTF-8编码
    process.stdout.setEncoding('utf8');
    
    // 引入文件系统模块
    const fs = require('fs');
    
    try {{
        // 加载dataDecrypt.js文件
        const dataDecryptCode = fs.readFileSync('dataDecrypt.js', 'utf8');
        
        // 注入必要的全局对象
        global.window = {{}};
        global.document = {{}};
        global.navigator = {{ userAgent: 'node.js' }};
        global.location = {{ href: '' }};
        
        // 执行dataDecrypt.js代码
        eval(dataDecryptCode);
        
        // 检查dataFilter函数是否存在
        if (typeof dataFilter !== 'function') {{
            console.error('ERROR: dataFilter函数不存在');
            process.exit(1);
        }}
        
        // 调用dataFilter函数解密数据
        const encryptedData = {json.dumps(encrypted_data, ensure_ascii=False)};
        const decryptedData = dataFilter(encryptedData);
        
        // 输出解密结果标记
        console.log(`DECRYPT_RESULT:${{JSON.stringify(decryptedData)}}`);
    }} catch (error) {{
        console.error(`ERROR: ${{error.message}}`);
        process.exit(1);
    }}
    '''
    
    try:
        # 执行JavaScript代码
        result = subprocess.run(
            ['node', '-e', js_code],
            capture_output=True,
            encoding='utf-8',
            timeout=60
        )
        
        print(f"命令返回码: {result.returncode}")
        
        # 处理输出
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'DECRYPT_RESULT:' in line:
                    decrypt_result = line.split('DECRYPT_RESULT:')[1]
                    print(f"解密成功，返回结果")
                    return json.loads(decrypt_result)
        
        # 处理错误
        if result.stderr:
            print(f"JavaScript错误: {result.stderr}")
        
        return None
    except Exception as e:
        print(f"执行JavaScript代码时出错: {type(e).__name__}: {e}")
        return None

# 直接执行JavaScript代码获取签名
def get_sign_directly(url_info, data_info, other_info):
    print(f"\n=== 开始获取sign ===")
    print(f"URL信息: {json.dumps(url_info, ensure_ascii=False)}")
    print(f"数据信息: {json.dumps(data_info, ensure_ascii=False)}")
    
    # 构建JavaScript代码
    js_code = f'''
    // 设置UTF-8编码
    process.stdout.setEncoding('utf8');
    
    // 引入文件系统模块
    const fs = require('fs');
    
    try {{
        // 加载signDecrypt.js文件
        const signDecryptCode = fs.readFileSync('signDecrypt.js', 'utf8');
        
        // 注入必要的全局对象
        global.window = {{}};
        global.document = {{}};
        global.navigator = {{ userAgent: 'node.js' }};
        global.location = {{ href: '' }};
        
        // 执行signDecrypt.js代码
        eval(signDecryptCode);
        
        // 准备参数
        const urlInfo = {json.dumps(url_info, ensure_ascii=False)};
        const dataInfo = {json.dumps(data_info, ensure_ascii=False)};
        const otherInfo = {json.dumps(other_info, ensure_ascii=False)};
        
        // 检查Ny函数是否存在
        if (typeof global.Ny !== 'function') {{
            console.error('ERROR: Ny函数不存在');
            process.exit(1);
        }}
        
        // 调用Ny函数获取签名
        const sign = global.Ny(urlInfo, dataInfo, otherInfo);
        
        // 输出签名结果标记
        console.log(`SIGN_RESULT:${{sign}}`);
    }} catch (error) {{
        console.error(`ERROR: ${{error.message}}`);
        process.exit(1);
    }}
    '''
    
    try:
        # 执行JavaScript代码
        result = subprocess.run(
            ['node', '-e', js_code],
            capture_output=True,
            encoding='utf-8',
            timeout=60
        )
        
        print(f"命令返回码: {result.returncode}")
        
        # 处理输出
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'SIGN_RESULT:' in line:
                    sign = line.split('SIGN_RESULT:')[1]
                    print(f"获取的sign: {sign}")
                    return sign
        
        # 处理错误
        if result.stderr:
            print(f"JavaScript错误: {result.stderr}")
        
        return None
    except Exception as e:
        print(f"执行JavaScript代码时出错: {type(e).__name__}: {e}")
        return None

# 频道配置 - 只需修改这里的word变量即可获取不同频道的数据
# 支持的值：'movielist', 'varietylist', 等
word = '爱情'

print(f"🔍 获取{word}频道数据...")

# 准备签名参数
url_info = {'url': 'mobile/entertainment/objectFansRank', 'method': 'GET'}
data_info = {'channel': word}
other_info = {}

# 直接调用JavaScript获取签名
sign = get_sign_directly(url_info, data_info, other_info)

# 准备请求参数和头信息
cookies = {
    'mobile_iindex_uuid': '86c80c37-26fc-5e43-a4f1-af5cd8d51bfa',
    'Hm_lvt_2873e2b0bdd5404c734992cd3ae7253f': '1760943399,1761024829,1761043958',
    'HMACCOUNT': 'AAD517BE97368D67',
    'Hm_lpvt_2873e2b0bdd5404c734992cd3ae7253f': '1761111391',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://www.chinaindex.net/ranklist/680',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'UUID': '86c80c37-26fc-5e43-a4f1-af5cd8d51bfa',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    'funcID': 'undefined',
    'incognitoMode': '0',
    'sec-ch-ua': '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': 'mobile_iindex_uuid=86c80c37-26fc-5e43-a4f1-af5cd8d51bfa; Hm_lvt_2873e2b0bdd5404c734992cd3ae7253f=1760943399,1761024829,1761043958; HMACCOUNT=AAD517BE97368D67; Hm_lpvt_2873e2b0bdd5404c734992cd3ae7253f=1761111391',
}

# 如果成功获取到签名，发送请求
if sign:
    params = {
        'channel': word,
        'sign': sign,
    }
    
    print("\n=== 发送请求 ===")
    print(f"请求URL:https://www.chinaindex.net/iIndexMobileServer/mobile/comm/getSearchResult")
    print(f"请求参数: {params}")
    
    response = requests.get(
        'https://www.chinaindex.net/iIndexMobileServer/mobile/comm/getSearchResult',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    
    print("\n=== 请求结果 ===")
    print(f"状态码: {response.status_code}")
    # 直接打印响应的JSON数据
    print("响应数据:")
    response_data = response.json()
    print(f"原始响应: {json.dumps(response_data, ensure_ascii=False)}")
    
    # 检查是否需要解密
    if response_data.get('isEncrypt') == 1 and response_data.get('data'):
        print("检测到加密数据，开始解密...")
        # 准备解密参数
        decrypt_params = {
            'data': response_data.get('data'),
            'isEncrypt': response_data.get('isEncrypt'),
            'result': response_data.get('result'),
            'fetchTime': response_data.get('fetchTime', 0),
            'loginStatus': response_data.get('loginStatus', 0),
            'totalNo': response_data.get('totalNo', 0),
            'residueNum': response_data.get('residueNum', 0),
            'updatedNum': response_data.get('updatedNum', 0),
            'pageNum': response_data.get('pageNum', 0),
            'pageLimit': response_data.get('pageLimit', 0),
            'lastFetchTime': response_data.get('lastFetchTime', 0)
        }
        
        # 调用dataFilter函数解密数据
        decrypted_result = decrypt_data_with_js(decrypt_params)
        
        if decrypted_result:
            print("\n=== 解密结果 ===")
            print(json.dumps(decrypted_result, ensure_ascii=False, indent=2))
            # 保存解密结果到文件
            output_file = f"decrypted_result_{word}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(decrypted_result, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 解密结果已保存到: {output_file}")
        else:
            print("\n❌ 解密失败")
    else:
        print("数据未加密或不需要解密")
else:
    print("\n❌ 无法获取有效的sign，跳过请求步骤")
    print("请检查JavaScript解密文件和函数名是否正确")
    # 如果无法获取签名，使用固定签名进行请求
    print("\n使用备用固定签名进行请求...")
    params = {
        'channel': word,
        'sign': '6fb5ce5dd1fb90ed46df7b71cef028e3',
    }
    response = requests.get(
        'https://www.chinaindex.net/iIndexMobileServer/mobile/comm/getSearchResult',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(f"状态码: {response.status_code}")
    print("响应数据:")
    response_data = response.json()
    print(f"原始响应: {json.dumps(response_data, ensure_ascii=False)}")
    
    # 检查是否需要解密
    if response_data.get('isEncrypt') == 1 and response_data.get('data'):
        print("检测到加密数据，开始解密...")
        # 准备解密参数
        decrypt_params = {
            'data': response_data.get('data'),
            'isEncrypt': response_data.get('isEncrypt'),
            'result': response_data.get('result'),
            'fetchTime': response_data.get('fetchTime', 0),
            'loginStatus': response_data.get('loginStatus', 0),
            'totalNo': response_data.get('totalNo', 0),
            'residueNum': response_data.get('residueNum', 0),
            'updatedNum': response_data.get('updatedNum', 0),
            'pageNum': response_data.get('pageNum', 0),
            'pageLimit': response_data.get('pageLimit', 0),
            'lastFetchTime': response_data.get('lastFetchTime', 0)
        }
        
        # 调用dataFilter函数解密数据
        decrypted_result = decrypt_data_with_js(decrypt_params)
        
        if decrypted_result:
            print("\n=== 解密结果 ===")
            print(json.dumps(decrypted_result, ensure_ascii=False, indent=2))
            # 保存解密结果到文件
            output_file = f"decrypted_result_{word}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(decrypted_result, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 解密结果已保存到: {output_file}")
        else:
            print("\n❌ 解密失败")
    else:
        print("数据未加密或不需要解密")