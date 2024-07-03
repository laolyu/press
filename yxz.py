# -*- coding: utf-8 -*-
import os
import queue, uuid
# import cn2an
from random import choice
from locust import events, FastHttpUser, TaskSet, SequentialTaskSet, task, between, tag
import json, requests

# proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
requests.packages.urllib3.disable_warnings()


# def number_to_chinese(number):
#     return cn2an.transform(number, "an2cn")


def mock_yxzuser(phone):
    uri = "https://test-internal.gezhijiankang.com/zeus/user/test/mock/phoneUser"
    body = {
        "createBy": "qa_mock_user",
        "phone": phone,
        "site": "TONG_MICS"
    }
    headers = {"content-type": "application/json;charset=UTF-8"}
    res = requests.post(uri, headers=headers, json=body, verify=False)
    return json.loads(res.text)["data"]["userId"]


def mocksession(userid, site=14):
    url = 'https://test-internal.gezhijiankang.com/zeus/user/test/session/add?site={}&userId={}'.format(site, userid)
    res = requests.get(url)
    print(json.loads(res.text)['data'])
    return json.loads(res.text)['data']


def read_yxz():
    app_id, app_secret = 'cli_a4829baf2cbc500b', 'KA3JvaL059HjRChCM4q4ObduAyUjOm0e'
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    post_data = {"app_id": app_id,
                 "app_secret": app_secret}
    r = requests.post(url, data=post_data, verify=False)
    token = r.json()["tenant_access_token"]
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    res = requests.get(
        'https://open.feishu.cn/open-apis/bitable/v1/apps/MBYtbtyqNaQG6ssLbHtcCM96npd/tables/tblIOU6HYIZ1WGIe/records',
        headers=headers, verify=False)
    yxz_baseinfo_list = json.loads(res.text)['data']['items']
    return yxz_baseinfo_list


def write_yxz(fields, record_id):
    app_id, app_secret = 'cli_a4829baf2cbc500b', 'KA3JvaL059HjRChCM4q4ObduAyUjOm0e'
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    post_data = {"app_id": app_id, "app_secret": app_secret}
    r = requests.post(url, data=post_data)
    token = r.json()["tenant_access_token"]
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    res = requests.put(
        'https://open.feishu.cn/open-apis/bitable/v1/apps/MBYtbtyqNaQG6ssLbHtcCM96npd/tables/tblIOU6HYIZ1WGIe/records/{}'.format(
            record_id),
        json={'fields': fields}, headers=headers)
    print(res.text)
    return res.text


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print('===测试结束了提示===')


class YHomePage(TaskSet):
    host = 'https://test.viatris.cc/'
    weight = 5
    headers = {}
    session = ''

    def on_start(self):
        # print('DoctorHomePage start')
        curdata = self.user.user_data_queue.get()
        self.session = curdata[0]
        self.medcineid = curdata[1]
        self.templateid = curdata[2]
        self.phone = curdata[3]
        self.userid = curdata[4]
        self.headers = {'content-type': 'application/json', 'Authorization': self.session}
        # print(self.headers)

    def on_stop(self):
        self.user.user_data_queue.put(self.session)
        # print('DoctorHomePage end')

    @tag('1,获取当前登录用户信息')
    @task
    def userInfo_test(self):
        with self.client.get(self.host + 'gateway/yxz-service/auth/userInfo', headers=self.headers,
                             verify=False) as response:
            # print(response.content)  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))

    @tag('新建发起人')
    @task
    def user_create(self):
        data = {"phone": f'{self.phone}'}
        # print(data, self.headers,self.session)
        with self.client.post(self.host + 'gateway/yxz-admin/user/create', json=data, headers=self.headers,
                              verify=False) as response:
            print(response.content.decode('utf-8'))
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag('药品评价方案')
    @task
    def newu_test(self):
        # data = {"phone": f'{self.phone}'}
        # print(data, self.headers,self.session)
        with self.client.get(self.host + 'gateway/yxz-admin/evaluation/list?p=1&pageSize=20', headers=self.headers,
                             verify=False) as response:
            # print(response.content.decode('utf-8'))
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag('联系人库')
    @task
    def relatedUser_list(self):
        with self.client.get(self.host + 'gateway/yxz-service/relatedUser/list?p=1&pageSize=50', headers=self.headers,
                             verify=False) as response:
            # print(response.content)  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))

    @tag('药品库A')
    @task
    def medicine_list(self):
        with self.client.get(self.host + 'gateway/yxz-service/medicine/list?p=1&pageSize=50', headers=self.headers,
                             verify=False) as response:
            # print(response.content)  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))
            m = response.content['data']['records'][0][id]
            print(m)

    @tag('我创建的评分方案列表')
    @task
    def evaluation_list(self):
        with self.client.get(self.host + 'gateway/yxz-service/evaluation/list?p=1&pageSize=50', headers=self.headers,
                             verify=False) as response:
            # print(response.content.decode('utf-8'))  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))

    @tag('我参与的评分方案列表')
    @task
    def participating_test(self):
        with self.client.get(self.host + 'gateway/yxz-service/evaluation/participatingList?p=1&pageSize=50',
                             headers=self.headers, verify=False) as response:
            # print(response.content.decode('utf-8'))  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))

    @tag('新建模板方案')
    @task
    def managementDetail_test(self):

        data = {"name": f"方案名称{self.phone}", "medicineIdList": [str(self.medcineid)]}
        # print(data)
        with self.client.post(self.host + 'gateway/yxz-service/evaluation/create', json=data, headers=self.headers,
                              verify=False) as response:
            # print(response.content)
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag('提交评分方案')
    @task
    def fan_test(self):
        data = {
            "id": f"{int(self.templateid) - 1}",
            "categoryList": [
                {
                    "id": 0,
                    "templateId": "70",
                    "name": "安全性",
                    "maxScore": 25,
                    "createTime": 1695291937000,
                    "updateTime": 1695291937000,
                    "questionList": [
                        {
                            "id": 0,
                            "templateId": "70",
                            "categoryId": "167",
                            "name": "不良反应分级",
                            "type": 1,
                            "maxScore": 6,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "812",
                                    "templateId": "70",
                                    "questionId": "291",
                                    "label": "症状轻微，无需治疗",
                                    "score": 6,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "813",
                                    "templateId": "70",
                                    "questionId": "291",
                                    "label": "症状较轻，需要干预",
                                    "score": 4,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "814",
                                    "templateId": "70",
                                    "questionId": "291",
                                    "label": "症状明显，需要干预",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "815",
                                    "templateId": "70",
                                    "questionId": "291",
                                    "label": "症状严重，可能危及生命",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 1,
                            "templateId": "70",
                            "categoryId": "167",
                            "name": "药物警戒",
                            "type": 3,
                            "maxScore": 5,
                            "minScore": 0,
                            "remark": "满分5分，每条药物警戒公告减1分，最多减5分（得分越高，说明安全性越好）",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 2,
                            "templateId": "70",
                            "categoryId": "167",
                            "name": "特殊人群（非限制性使用，满分；限制性使用，赋分减半；禁用，0分）",
                            "type": 2,
                            "maxScore": 8,
                            "minScore": 2,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "817",
                                    "templateId": "70",
                                    "questionId": "293",
                                    "label": "儿童可用",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "818",
                                    "templateId": "70",
                                    "questionId": "293",
                                    "label": "老人可用",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "819",
                                    "templateId": "70",
                                    "questionId": "293",
                                    "label": "孕妇可用",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "820",
                                    "templateId": "70",
                                    "questionId": "293",
                                    "label": "哺乳期妇女可用",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "821",
                                    "templateId": "70",
                                    "questionId": "293",
                                    "label": "肝功能异常可用",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "822",
                                    "templateId": "70",
                                    "questionId": "293",
                                    "label": "肾功能异常可用",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "823",
                                    "templateId": "70",
                                    "questionId": "293",
                                    "label": "无其他人群禁忌",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 3,
                            "templateId": "70",
                            "categoryId": "167",
                            "name": "药物相互作用",
                            "type": 1,
                            "maxScore": 3,
                            "minScore": 1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "824",
                                    "templateId": "70",
                                    "questionId": "294",
                                    "label": "一般无需调整用药剂量",
                                    "score": 3,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "825",
                                    "templateId": "70",
                                    "questionId": "294",
                                    "label": "需要调整剂量",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "826",
                                    "templateId": "70",
                                    "questionId": "294",
                                    "label": "禁止在同一时段使用",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 4,
                            "templateId": "70",
                            "categoryId": "167",
                            "name": "其他",
                            "type": 2,
                            "maxScore": 3,
                            "minScore": 1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "827",
                                    "templateId": "70",
                                    "questionId": "295",
                                    "label": "不良反应均为可逆性",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "828",
                                    "templateId": "70",
                                    "questionId": "295",
                                    "label": "无致畸、致癌",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "829",
                                    "templateId": "70",
                                    "questionId": "295",
                                    "label": "无特别用药警示",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        }
                    ]
                },
                {
                    "id": 1,
                    "templateId": "70",
                    "name": "有效性",
                    "maxScore": 25,
                    "createTime": 1695291937000,
                    "updateTime": 1695291937000,
                    "questionList": [
                        {
                            "id": 0,
                            "templateId": "70",
                            "categoryId": "168",
                            "name": "指南推荐等级",
                            "type": 3,
                            "maxScore": 10,
                            "minScore": 0,
                            "remark": "诊疗规范推荐(国家卫生行政部门) 10分｜\n指南Ｉ级推荐(Ａ级证据9分,Ｂ级证据8分,Ｃ级证据7分,其他6分)｜\n指南ＩＩ级及以下推荐(Ａ级证据5分,Ｂ级证据4分,Ｃ级证据3分,其他2分)｜\n以上均无推荐 1分｜\n专家共识推荐 0分",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 1,
                            "templateId": "70",
                            "categoryId": "168",
                            "name": "说明书适应症",
                            "type": 2,
                            "maxScore": 5,
                            "minScore": 1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "835",
                                    "templateId": "70",
                                    "questionId": "297",
                                    "label": "原发性高胆固醇血症",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "836",
                                    "templateId": "70",
                                    "questionId": "297",
                                    "label": "纯合子家族性高胆固醇血症",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "837",
                                    "templateId": "70",
                                    "questionId": "297",
                                    "label": "冠心病合并高胆固醇血症",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "838",
                                    "templateId": "70",
                                    "questionId": "297",
                                    "label": "冠心病等危症合并高胆固醇血症或混合型血脂异常",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "839",
                                    "templateId": "70",
                                    "questionId": "297",
                                    "label": "纯合子谷甾醇血症",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 2,
                            "templateId": "70",
                            "categoryId": "168",
                            "name": "循证医学证据",
                            "type": 1,
                            "maxScore": 6,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "840",
                                    "templateId": "70",
                                    "questionId": "298",
                                    "label": "有高质量循证证据",
                                    "score": 6,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "841",
                                    "templateId": "70",
                                    "questionId": "298",
                                    "label": "有中等质量循证证据",
                                    "score": 4,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "842",
                                    "templateId": "70",
                                    "questionId": "298",
                                    "label": "有低质量循证证据",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "843",
                                    "templateId": "70",
                                    "questionId": "298",
                                    "label": "无循证证据",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 3,
                            "templateId": "70",
                            "categoryId": "168",
                            "name": "调脂强度",
                            "type": 3,
                            "maxScore": 4,
                            "minScore": 0,
                            "remark": "属于指南推荐高强度治疗药物",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [],
                            "report": None,
                            "reportRemarkList": None
                        }
                    ]
                },
                {
                    "id": 2,
                    "templateId": "70",
                    "name": "经济性",
                    "maxScore": 10,
                    "createTime": 1695291937000,
                    "updateTime": 1695291937000,
                    "questionList": [
                        {
                            "id": 0,
                            "templateId": "70",
                            "categoryId": "169",
                            "name": "药品日均治疗费用（百分位数）P值=所评药品数量",
                            "type": 1,
                            "maxScore": 5,
                            "minScore": 1,
                            "remark": "诊疗规范推荐(国家卫生行政部门) 10分｜",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "845",
                                    "templateId": "70",
                                    "questionId": "300",
                                    "label": "最低P20%",
                                    "score": 5,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "846",
                                    "templateId": "70",
                                    "questionId": "300",
                                    "label": "P20%~40%区间",
                                    "score": 4,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "847",
                                    "templateId": "70",
                                    "questionId": "300",
                                    "label": "P40%~60%区间",
                                    "score": 3,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "848",
                                    "templateId": "70",
                                    "questionId": "300",
                                    "label": "P60%~80%区间",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "849",
                                    "templateId": "70",
                                    "questionId": "300",
                                    "label": "P80%~100%区间",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 1,
                            "templateId": "70",
                            "categoryId": "169",
                            "name": "国家医保",
                            "type": 1,
                            "maxScore": 5,
                            "minScore": 1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "850",
                                    "templateId": "70",
                                    "questionId": "301",
                                    "label": "国家医保甲类,且没有支付限制条件",
                                    "score": 5,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "851",
                                    "templateId": "70",
                                    "questionId": "301",
                                    "label": "国家医保甲类,有支付限制条件",
                                    "score": 4,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "852",
                                    "templateId": "70",
                                    "questionId": "301",
                                    "label": "国家医保乙类/ 国家谈判药品,且没有支付限制条件",
                                    "score": 3,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "853",
                                    "templateId": "70",
                                    "questionId": "301",
                                    "label": "国家医保乙类/ 国家谈判药品,有支付限制条件",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "854",
                                    "templateId": "70",
                                    "questionId": "301",
                                    "label": "不在国家医保目录",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        }
                    ]
                },
                {
                    "id": 3,
                    "templateId": "70",
                    "name": "药品技术特点适宜性",
                    "maxScore": 8,
                    "createTime": 1695291937000,
                    "updateTime": 1695291937000,
                    "questionList": [
                        {
                            "id": 0,
                            "templateId": "70",
                            "categoryId": "170",
                            "name": "药品说明书",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "855",
                                    "templateId": "70",
                                    "questionId": "302",
                                    "label": "说明书格式正确内容全面，上市后主动对说明书进行修改",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "856",
                                    "templateId": "70",
                                    "questionId": "302",
                                    "label": "说明书格式正确内容较全面，上市后长时间未进行说明书更新",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "857",
                                    "templateId": "70",
                                    "questionId": "302",
                                    "label": "说明书格式不正确内容不全面，上市后长时间未进行说明书更新",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 1,
                            "templateId": "70",
                            "categoryId": "170",
                            "name": "药品有效期",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "858",
                                    "templateId": "70",
                                    "questionId": "303",
                                    "label": ">36个月",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "859",
                                    "templateId": "70",
                                    "questionId": "303",
                                    "label": "24~36个月",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "860",
                                    "templateId": "70",
                                    "questionId": "303",
                                    "label": "<24个月",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 2,
                            "templateId": "70",
                            "categoryId": "170",
                            "name": "储存条件",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "861",
                                    "templateId": "70",
                                    "questionId": "304",
                                    "label": "常温贮藏",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "862",
                                    "templateId": "70",
                                    "questionId": "304",
                                    "label": "常温贮藏,避光或遮光",
                                    "score": 1.5,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "863",
                                    "templateId": "70",
                                    "questionId": "304",
                                    "label": "阴凉贮藏",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "864",
                                    "templateId": "70",
                                    "questionId": "304",
                                    "label": "阴凉贮藏,避光或遮光",
                                    "score": 0.5,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "865",
                                    "templateId": "70",
                                    "questionId": "304",
                                    "label": "冷藏/ 冷冻贮藏",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 3,
                            "templateId": "70",
                            "categoryId": "170",
                            "name": "药品成分及辅料是否明确",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "866",
                                    "templateId": "70",
                                    "questionId": "305",
                                    "label": "主要成分及辅料明确",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "867",
                                    "templateId": "70",
                                    "questionId": "305",
                                    "label": "主要成分及辅料不完全明确",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        }
                    ]
                },
                {
                    "id": 4,
                    "templateId": "70",
                    "name": "药品使用适宜性",
                    "maxScore": 12,
                    "createTime": 1695291937000,
                    "updateTime": 1695291937000,
                    "questionList": [
                        {
                            "id": 0,
                            "templateId": "70",
                            "categoryId": "171",
                            "name": "用药依从性",
                            "type": 2,
                            "maxScore": 6,
                            "minScore": 1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "868",
                                    "templateId": "70",
                                    "questionId": "306",
                                    "label": "给药剂型适宜",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "869",
                                    "templateId": "70",
                                    "questionId": "306",
                                    "label": "给药剂量便于掌握",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "870",
                                    "templateId": "70",
                                    "questionId": "306",
                                    "label": "使用方便",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "871",
                                    "templateId": "70",
                                    "questionId": "306",
                                    "label": "给药频次适宜",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "872",
                                    "templateId": "70",
                                    "questionId": "306",
                                    "label": "服药不受饮食限制",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "873",
                                    "templateId": "70",
                                    "questionId": "306",
                                    "label": "服药不受时间限制",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 1,
                            "templateId": "70",
                            "categoryId": "171",
                            "name": "药理作用",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "874",
                                    "templateId": "70",
                                    "questionId": "307",
                                    "label": "临床疗效确切，作用机制明确",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "875",
                                    "templateId": "70",
                                    "questionId": "307",
                                    "label": "临床疗效确切，作用机制尚不十分明确",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "876",
                                    "templateId": "70",
                                    "questionId": "307",
                                    "label": "临床疗效一般，作用机制不明确",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 2,
                            "templateId": "70",
                            "categoryId": "171",
                            "name": "体内过程",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "877",
                                    "templateId": "70",
                                    "questionId": "308",
                                    "label": "体内过程明确，药动学参数完整",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "878",
                                    "templateId": "70",
                                    "questionId": "308",
                                    "label": "体内过程基本明确，药动学参数不完整",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "879",
                                    "templateId": "70",
                                    "questionId": "308",
                                    "label": "体内过程尚不明确，无药动学相关研究",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 3,
                            "templateId": "70",
                            "categoryId": "171",
                            "name": "一致性评价",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "880",
                                    "templateId": "70",
                                    "questionId": "309",
                                    "label": "原研药品/参比药品",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "881",
                                    "templateId": "70",
                                    "questionId": "309",
                                    "label": "通过一致性评价的仿制药品",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "882",
                                    "templateId": "70",
                                    "questionId": "309",
                                    "label": "非原研且未通过一致性评价的仿制药品",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        }
                    ]
                },
                {
                    "id": 5,
                    "templateId": "70",
                    "name": "可及性",
                    "maxScore": 15,
                    "createTime": 1695291937000,
                    "updateTime": 1695291937000,
                    "questionList": [
                        {
                            "id": 0,
                            "templateId": "70",
                            "categoryId": "172",
                            "name": "可获得性",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "883",
                                    "templateId": "70",
                                    "questionId": "310",
                                    "label": "已在本医疗卫生机构配备，供货稳定",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "884",
                                    "templateId": "70",
                                    "questionId": "310",
                                    "label": "已在本医疗卫生机构配备，供货不稳定",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "885",
                                    "templateId": "70",
                                    "questionId": "310",
                                    "label": "未在本医疗卫生机构配备",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 1,
                            "templateId": "70",
                            "categoryId": "172",
                            "name": "可负担性",
                            "type": 1,
                            "maxScore": 5,
                            "minScore": -1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "886",
                                    "templateId": "70",
                                    "questionId": "311",
                                    "label": "年费用/年收入＜1%",
                                    "score": 5,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "887",
                                    "templateId": "70",
                                    "questionId": "311",
                                    "label": "年费用/年收入1~5%",
                                    "score": 4,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "888",
                                    "templateId": "70",
                                    "questionId": "311",
                                    "label": "年费用/年收入6~10%",
                                    "score": 3,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "889",
                                    "templateId": "70",
                                    "questionId": "311",
                                    "label": "年费用/年收入11~20%",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "890",
                                    "templateId": "70",
                                    "questionId": "311",
                                    "label": "年费用/年收入>20%",
                                    "score": -1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 2,
                            "templateId": "70",
                            "categoryId": "172",
                            "name": "基本药物目录",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "891",
                                    "templateId": "70",
                                    "questionId": "312",
                                    "label": "在《国家基本药物目录》,没有△要求",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "892",
                                    "templateId": "70",
                                    "questionId": "312",
                                    "label": "在《国家基本药物目录》,有△要求",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "893",
                                    "templateId": "70",
                                    "questionId": "312",
                                    "label": "不在《国家基本药物目录》",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 3,
                            "templateId": "70",
                            "categoryId": "172",
                            "name": "带量采购情况",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "894",
                                    "templateId": "70",
                                    "questionId": "313",
                                    "label": "进入国家带量采购",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "895",
                                    "templateId": "70",
                                    "questionId": "313",
                                    "label": "进入省级带量采购",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "896",
                                    "templateId": "70",
                                    "questionId": "313",
                                    "label": "未进入带量采购",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 4,
                            "templateId": "70",
                            "categoryId": "172",
                            "name": "全球使用情况",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "897",
                                    "templateId": "70",
                                    "questionId": "314",
                                    "label": "美国、欧洲、日本均已上市 ",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "898",
                                    "templateId": "70",
                                    "questionId": "314",
                                    "label": "美国或欧洲或日本上市",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "899",
                                    "templateId": "70",
                                    "questionId": "314",
                                    "label": "美国、欧洲、日本均未上市",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 5,
                            "templateId": "70",
                            "categoryId": "172",
                            "name": "生产企业状况",
                            "type": 1,
                            "maxScore": 2,
                            "minScore": 0,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "900",
                                    "templateId": "70",
                                    "questionId": "315",
                                    "label": "生产企业为世界销量前50制药企业（美国制药经理人）",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "901",
                                    "templateId": "70",
                                    "questionId": "315",
                                    "label": "生产企业在国家工业和信息化部医药工业百强榜",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "902",
                                    "templateId": "70",
                                    "questionId": "315",
                                    "label": "其他",
                                    "score": 0,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        }
                    ]
                },
                {
                    "id": 6,
                    "templateId": "70",
                    "name": "创新性",
                    "maxScore": 5,
                    "createTime": 1695291937000,
                    "updateTime": 1695291937000,
                    "questionList": [
                        {
                            "id": 0,
                            "templateId": "70",
                            "categoryId": "173",
                            "name": "临床创新",
                            "type": 2,
                            "maxScore": 2,
                            "minScore": 1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "903",
                                    "templateId": "70",
                                    "questionId": "316",
                                    "label": "解决未满足的治疗需求",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "904",
                                    "templateId": "70",
                                    "questionId": "316",
                                    "label": "有附加治疗价值",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        },
                        {
                            "id": 1,
                            "templateId": "70",
                            "categoryId": "173",
                            "name": "证明创新药物的质量证据",
                            "type": 1,
                            "maxScore": 3,
                            "minScore": 1,
                            "remark": "",
                            "createTime": 1695291937000,
                            "updateTime": 1695291937000,
                            "optionList": [
                                {
                                    "id": "905",
                                    "templateId": "70",
                                    "questionId": "317",
                                    "label": "作为创新药上市且有高等质量证据",
                                    "score": 3,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "906",
                                    "templateId": "70",
                                    "questionId": "317",
                                    "label": "作为创新药上市且有中低等质量证据",
                                    "score": 2,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                },
                                {
                                    "id": "907",
                                    "templateId": "70",
                                    "questionId": "317",
                                    "label": "其他新药",
                                    "score": 1,
                                    "createTime": 1695291937000,
                                    "updateTime": 1695291937000
                                }
                            ],
                            "report": None,
                            "reportRemarkList": None
                        }
                    ]
                }
            ]
        }
        # print(data)

        with self.client.post(self.host + 'gateway/yxz-service/template/save', json=data, headers=self.headers,
                              verify=False) as response:
            print(response.content)
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag("输入手机号码分享")
    @task
    def add_test(self):
        data = {"evaluationId": f"{self.templateid}",
                "phoneList": ["13917891535", "16600000001", '16600000002', '16600000003']}
        with self.client.post(self.host + 'gateway/yxz-service/evaluationParticipant/add', json=data,
                              headers=self.headers, verify=False) as response:
            print(response.content.decode('utf-8'))
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag("已邀请的成员")
    @task
    def evaluationId_user(self):
        with self.client.get(
                self.host + f'gateway/yxz-service/evaluationParticipant/list?evaluationId={self.templateid}',
                headers=self.headers, verify=False) as response:
            print(response.content.decode('utf-8'))
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag("开启评分")
    @task
    def start_test(self):
        data = {"id": f"{self.templateid}"}
        # print(data)
        with self.client.post(self.host + 'gateway/yxz-service/evaluation/start', json=data, headers=self.headers,
                              verify=False) as response:
            # print(response.content.decode('utf-8'))
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag('去评分')
    @task
    def pingf_test(self):
        data = {"id": f"{self.templateid}", "list": [
            {"medicineId": "28", "categoryId": "291", "questionId": "558", "optionId": "558", "score": 9.9},
            {"medicineId": "51", "categoryId": "291", "questionId": "558", "optionId": "558", "score": 0},
            {"medicineId": "28", "categoryId": "292", "questionId": "559", "optionId": "1558", "score": 6},
            {"medicineId": "51", "categoryId": "292", "questionId": "559", "optionId": "1559", "score": 5},
            {"medicineId": "28", "categoryId": "290", "questionId": "557", "optionId": "1556", "score": 9},
            {"medicineId": "51", "categoryId": "290", "questionId": "557", "optionId": "1555", "score": 10}],
                "remarkList": [
                    {"id": "232", "userId": "1665609343213477908", "evaluationId": "89", "categoryId": "291",
                     "questionId": "558", "remark": "9.9\n0", "createTime": 1695711722000,
                     "updateTime": 1695711722000},
                    {"id": "233", "userId": "1665609343213477908", "evaluationId": "89", "categoryId": "292",
                     "questionId": "559", "remark": "6\n5", "createTime": 1695711722000, "updateTime": 1695711722000},
                    {"id": "234", "userId": "1665609343213477908", "evaluationId": "89", "categoryId": "290",
                     "questionId": "557", "remark": "9\n10", "createTime": 1695711722000,
                     "updateTime": 1695711722000}], "summary": "全部写完了"}
        # print(data)
        with self.client.post(self.host + 'gateway/yxz-service/evaluation/submit', headers=self.headers, json=data,
                              verify=False) as response:
            # print(response.content.decode('utf-8'))  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))

    @tag('查看报告')
    @task
    def report_test(self):
        with self.client.get(self.host + f'gateway/yxz-service/evaluation/report?id={self.templateid}',
                             headers=self.headers, verify=False) as response:
            # print(response.content.decode('utf-8'))  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))

    @tag('查看评价方案')
    @task
    def chakan_test(self):
        with self.client.get(self.host + f'gateway/yxz-service/evaluation/detail?id={self.templateid}',
                             headers=self.headers, verify=False) as response:
            # print(response.content.decode('utf-8'))  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))

    @tag("退回报告")
    @task
    def start_test(self):
        data = {"id": f"{self.templateid}", "userId": f"{self.userid}", "rejectReason": "不合格"}
        # print(data)
        with self.client.post(self.host + 'gateway/yxz-service/evaluation/reject', json=data, headers=self.headers,
                              verify=False) as response:
            # print(response.content.decode('utf-8'))
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))


class Evaluation(TaskSet):
    host = 'https://test.viatris.cc'
    weight = 1
    headers = {}
    session = ''
    groupid = ''

    def on_start(self):
        print('DoctorHomePage start')
        self.session = self.user.user_data_queue.get()[0]
        self.medcineid = self.user.user_data_queue.get()[1]
        self.headers = {'content-type': 'application/json', 'Authorization': self.session}
        print(self.headers)

    def on_stop(self):
        self.user.user_data_queue.put([self.session, self.medcineid])
        # print('DoctorHomePage end')

    @tag('post更新用户信息')
    @task
    def managementDetail_test(self):
        data = {"name": f"压测{self.session}", "hospital": "仁济医院", "department": "急诊科-1"}
        with self.client.post(self.host + 'gateway/yxz-service/auth/updateMyInfo', json=data, headers=self.headers,
                              verify=False) as response:
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag('post新建药品01')
    @task
    def managementDetail_test(self):
        data = {"name": f"第一药{self.session}", "manufacturer": "第一医药", "category": "CNS药"}
        with self.client.post(self.host + 'gateway/yxz-service/medicine/create', json=data, headers=self.headers,
                              verify=False) as response:
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    @tag('post新建药品02')
    @task
    def managementDetail_test(self):
        data = {"name": f"第二药{self.session}", "manufacturer": "第二医药", "category": "其他药"}
        with self.client.post(self.host + 'gateway/yxz-service/medicine/create', json=data, headers=self.headers,
                              verify=False) as response:
            try:
                if response.status_code != 200:
                    print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                      response.headers[
                                                                                          'eagleeye-traceid'],
                                                                                      self.session))
            except:
                print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content,
                                                                                  response.headers['eagleeye-traceid'],
                                                                                  self.session))

    # @tag('新建模板方案')
    # @task
    # def managementDetail_test(self):
    #     data = {"name": f"方案名称{self.session}", "medicineIdList": [str(self.medcineid)]}
    #     with self.client.post(self.host + 'gateway/yxz-service/medicine/create', json=data, headers=self.headers, verify=False) as response:
    #         print(response.content)
    #         try:
    #             if response.status_code != 200:
    #                 print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content, response.headers['eagleeye-traceid'], self.session))
    #         except:
    #             print('response.content:{},eagleeye-traceid:{},session:{}'.format(response.content, response.headers['eagleeye-traceid'], self.session))

    @tag('2,模板详情')
    @task
    def participatingList_test(self):
        with self.client.get(self.host + 'gateway/yxz-service/template/detail?id=1', headers=self.headers,
                             verify=False) as response:
            print(response.content)  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))

    @tag('5,评分方案详情')
    @task
    def participatingList_test(self):
        with self.client.get(self.host + 'gateway/yxz-service/template/detail?id=1', headers=self.headers,
                             verify=False) as response:
            # print(response.content)  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))


class websitUser(FastHttpUser):
    tasks = [YHomePage, Evaluation]
    wait_time = between(1, 2)
    bd = read_yxz()
    # print(bd)
    user_data_queue = queue.Queue()
    for i in range(5):
        userid = bd[i]['fields']['userid']
        session = bd[i]['fields']['session']
        # session = '93425eb0878e4fbbb4228a7ee761a832'  #观察员
        # session = 'e23dc24afce54cdba57438b9c6b3fd21'  #发起人
        medcineid = bd[i]['fields']['medcineid']
        templateid = bd[i]['fields']['templateid']
        phone = bd[i]['fields']['手机号']
        user_data_queue.put_nowait([session, medcineid, templateid, phone, userid])
        # print(user_data_queue)


if __name__ == '__main__':
    cmd = "locust -f yxz.py --host=https://test.viatris.cc --tags 1,获取当前登录用户信息 2,模板详情 3,我创建的评分方案列表 4,我参与的评分方案列表 5,评分方案详情"
    # cmd = "locust -f yxz.py --host=https://test.viatris.cc --tags 提交评分方案"
    # cmd = "locust -f yxz.py --host=https://test.viatris.cc/ --tags 输入手机号码分享"
    os.system(cmd)
    # websitUser(FastHttpUser)
    # E = Evaluation(SequentialTaskSet)
