import openpyxl
import requests
import os
import json

def test_token():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 设置参数文件路径
    username = "陈展鸿"  # 可以修改为其他用户名
    token_dir = os.path.join(current_dir, 'token', username)
    gateway_params_file = os.path.join(token_dir, 'gateway_app_parameters.xlsx')
    
    print(f"正在检查用户: {username}")
    print(f"参数文件路径: {gateway_params_file}")
    
    # 读取参数文件
    try:
        gateway_app_params_wb = openpyxl.load_workbook(gateway_params_file)
        gateway_app_params_dict = {}
        for row in gateway_app_params_wb.active.iter_rows(min_row=2, values_only=True):
            parameter = row[0]
            value = row[1] if row[1] is not None else ''
            gateway_app_params_dict[parameter] = value
        
        print("\n参数文件内容:")
        for key, value in gateway_app_params_dict.items():
            print(f"{key}: {value}")
        
        # 获取accessToken
        access_token = gateway_app_params_dict.get('accessToken')
        if not access_token:
            print("\n错误: 参数文件中没有找到accessToken")
            return
        
        print(f"\n使用accessToken: {access_token}")
        
        # 设置请求头
        headers = {
            'Host': 'gateway.app.xdf.cn',
            'stafftoken': '98ba3907b83fd78eba5463580010e28c',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://deskwx.xdf.cn',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Language/zh ColorScheme/Light DistType/publish-website wxwork/4.1.36 (MicroMessenger/6.2) WeChat/2.0.4 wwmver/3.26.36.625 Safari/605.1.15',
            'accept-language': 'zh-CN,zh-Hans;q=0.9',
            'referer': 'https://deskwx.xdf.cn/',
        }
        
        # 设置请求参数
        params = {
            'appId': '3027D9E5-0C09-4AD3-86F0-6C678B7826A4',
            'appVersion': '',
            'accessToken': access_token,
            'userId': gateway_app_params_dict.get('userId', ''),
            'classStatus': '3',
            'schoolId': '3',
            'teacherCode': gateway_app_params_dict.get('teacherCode', ''),
            'teacherType': '1',
            'pageSize': '5',
            'pageNo': '1',
        }
        
        print("\n发送请求...")
        print(f"请求URL: https://gateway.app.xdf.cn/k12-assistant-api/api/v1.0/acl/wx/1/class/all/list")
        print(f"请求头: {json.dumps(headers, indent=2, ensure_ascii=False)}")
        print(f"请求参数: {json.dumps(params, indent=2, ensure_ascii=False)}")
        
        # 发送请求
        response = requests.get(
            'https://gateway.app.xdf.cn/k12-assistant-api/api/v1.0/acl/wx/1/class/all/list',
            headers=headers,
            params=params
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 解析响应
        try:
            data = response.json()
            if data.get('code') == 200:
                print("\n权限验证成功！")
                print(f"班级列表: {json.dumps(data.get('data', {}).get('classList', []), indent=2, ensure_ascii=False)}")
            else:
                print(f"\n权限验证失败！错误码: {data.get('code')}, 错误信息: {data.get('message')}")
        except Exception as e:
            print(f"\n解析响应失败: {str(e)}")
            
    except Exception as e:
        print(f"\n发生错误: {str(e)}")

if __name__ == "__main__":
    test_token() 