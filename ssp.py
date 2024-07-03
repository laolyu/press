# coding:utf-8
# import os
import queue
from locust import events, FastHttpUser, TaskSet, SequentialTaskSet, task, between, tag, HttpUser
# import json, requests
# from requests.packages.urllib3.exceptions import InsecureRequestWarning


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print('===测试结束了提示===')


class sspPage(TaskSet):
    host = 'http://ssp.7654.com'
    weight = 10
    headers = {}
    session = ''

    # def on_start(self):
    #     # print('DoctorHomePage start')
    #     curdata = self.user.user_data_queue.get()
    #     self.session = curdata[0]
    #     self.medcineid = curdata[1]
    #     self.templateid = curdata[2]
    #     self.phone = curdata[3]
    #     self.userid = curdata[4]
    #     self.headers = {'content-type': 'application/json', 'Authorization': self.session}
    #     # print(self.headers)
    #     print('-------------')
    #
    # def on_stop(self):
    #     self.user.user_data_queue.put(self.session)
    #     # print('DoctorHomePage end')

    @tag('pb广告')
    @task
    def userInfo_test(self):
        with self.client.get(
                self.host + '/ssp/v2/ads?qid=xiaoyu&ad=xiaoyu_pingbao_1&browser=IE11&uid=CC06967FDA52AC4B46E7D2C1E52C0854&time=1648799743356&mixData=cnJrk4xEHwebcpWgjC2ggGKY1P7mkFumzBDQkaEiLchtwM3g7/EQWJVXUkpjuwcRH46LONeC09JMK0gMkc5J5nEeMYh4uj3y/pXLYmwKSZp+ptHX4R7CzoJDG9EheW/wrHprdII27so/OkWX5qsqpwrE/PU=&product_category=25',
                headers=self.headers,
                verify=False) as response:
            # print(response.content)  # 调试加入这一行
            try:
                if response.status_code != 200:
                    print('ok')
                    print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                             response.headers['eagleeye-traceid'],
                                                                             self.session))
            except:
                print('fail')
                print('response.content:{},traceid:{},session:{}'.format(response.content,
                                                                         response.headers['eagleeye-traceid'],
                                                                         self.session))


class websitUser(HttpUser):
    tasks = [sspPage]
    wait_time = between(1, 3)
    # bd = read_yxz()
    # print(bd)
    user_data_queue = queue.Queue()
    # for i in range(5):
    #     userid = bd[i]['fields']['userid']
    #     session = bd[i]['fields']['session']
    #     # session = '93425eb0878e4fbbb4228a7ee761a832'  #观察员
    #     # session = 'e23dc24afce54cdba57438b9c6b3fd21'  #发起人
    #     medcineid = bd[i]['fields']['medcineid']
    #     templateid = bd[i]['fields']['templateid']
    #     phone = bd[i]['fields']['手机号']
    #     user_data_queue.put_nowait([session, medcineid, templateid, phone, userid])
    print(user_data_queue)


if __name__ == '__main__':
    # cmd = "locust -f ssp.py --host=http://ssp.7654.com --tags pb广告 --master"
    # cmd = "locust -f yxz.py --host=https://test.viatris.cc --tags 提交评分方案"
    # cmd = "locust -f yxz.py --host=https://test.viatris.cc/ --tags 输入手机号码分享"
    # os.system(cmd)
    # websitUser(FastHttpUser)
    # E = Evaluation(SequentialTaskSet)
    print('--------')
