# coding:utf-8
import json

import requests


def mock_yxzuser(phone):
    uri = "https://test-internal.gezhijiankang.com/zeus/user/test/mock/phoneUser"
    body = {
        "createBy": "qa_mock_user",
        "phone": phone,
        "site": "TONG_MICS"
    }
    headers = {"content-type": "application/json;charset=UTF-8"}
    res = requests.post(uri, headers=headers, json=body, verify=False)
    print(json.loads(res.text)["data"]["userId"])
    return json.loads(res.text)["data"]["userId"]

def mocksession(userid, site=4):
    url = 'https://test-internal.gezhijiankang.com/zeus/user/test/session/add?site={}&userId={}'.format(site, userid)
    res = requests.get(url)
    print(json.loads(res.text)['data'])
    return json.loads(res.text)['data']


def write_yxz(fields, record_id):
    app_id, app_secret = 'cli_a4829baf2cbc500b', 'KA3JvaL059HjRChCM4q4ObduAyUjOm0e'
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    post_data = {"app_id": app_id,
                 "app_secret": app_secret}
    r = requests.post(url, data=post_data)
    token = r.json()["tenant_access_token"]
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    res = requests.put(
        'https://open.feishu.cn/open-apis/bitable/v1/apps/MBYtbtyqNaQG6ssLbHtcCM96npd/tables/tblIOU6HYIZ1WGIe/records/{}'.format(record_id),
        json={'fields': fields}, headers=headers)
    print(res.text)
    return res.text


if __name__ == '__main__':
    userid = mock_yxzuser(16600000005)
    se = mocksession(userid)
    write_yxz('session', se)
