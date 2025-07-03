
import httpx
from datetime import datetime
"""
快手电商开放平台
https://open.kwaixiaodian.com/zone/new/docs/api
"""

def get_access_token_by_code(app_id, app_secret, code, grant_type="code"):
    """
    首次授权通过回调地址中的code获取access_token
    """
    url = "https://openapi.kwaixiaodian.com/oauth2/access_token"
    params = {
        "app_id": app_id,
        "app_secret": app_secret,
        "code": code,
        "grant_type": grant_type
    }
    response = httpx.get(url, params=params)
    return response.json()

def refresh_access_token(app_id, app_secret, refresh_token, grant_type="refresh_token"):
    url = "https://openapi.kwaixiaodian.com/oauth2/refresh_token"
    data = {
        "app_id": app_id,
        "app_secret": app_secret,
        "refresh_token": refresh_token,
        "grant_type": grant_type
    }
    response = httpx.post(url, data=data)
    return response.json()

def generate_timestamp(start_date: str, end_date) -> int:
    """
    生成时间戳
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 返回时间戳
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return int(start.timestamp()), int(end.timestamp()) + 86399

if __name__ == "__main__":
    pass
