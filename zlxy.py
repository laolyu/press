# -*- coding: utf-8 -*-
import os
import queue, uuid
from locust import events, TaskSet, SequentialTaskSet, task, between, tag, HttpUser
import json, requests

# proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
requests.packages.urllib3.disable_warnings()


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


class websitUser(HttpUser):
    tasks = [YHomePage, Evaluation]
    wait_time = between(1, 2)


if __name__ == '__main__':
    cmd = "locust -f yxz.py --host=https://test.viatris.cc --tags 1,获取当前登录用户信息 2,模板详情 3,我创建的评分方案列表 4,我参与的评分方案列表 5,评分方案详情"
    # cmd = "locust -f yxz.py --host=https://test.viatris.cc --tags 提交评分方案"
    # cmd = "locust -f yxz.py --host=https://test.viatris.cc/ --tags 输入手机号码分享"
    os.system(cmd)
    # websitUser(FastHttpUser)
    # E = Evaluation(SequentialTaskSet)
