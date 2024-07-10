# coding:utf-8
import os

from locust import events, FastHttpUser, TaskSet, task, between, tag


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print('===测试结束了提示===')


class BaiduPage(TaskSet):
    host = 'http://www.baidu.com'
    weight = 10
    headers = {}
    session = ''

    @tag('搜索百度一下')
    @task
    def bd_test(self):
        self.client.get(
            self.host + '/sugrec?ie=utf-8&json=1&prod=pc&wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B',
            headers=self.headers, catch_response=False)  # 不用等待接口响应


class WebsitUser(FastHttpUser):
    tasks = [BaiduPage]
    wait_time = between(1, 3)  # 用户行为间隔为0，实现高并发


if __name__ == '__main__':
    cmd = "locust -f q3.py --host=http://www.baidu.com --tags 搜索百度一下"
    os.system(cmd)
