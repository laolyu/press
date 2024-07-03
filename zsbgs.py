import os

from locust import task, run_single_user, tag, between, events, FastHttpUser, TaskSet


@events.test_start.add_listener
def on_test_start(**kwargs):
    print('===测试最开始提示===')


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print('===测试结束了提示===')

class ZsbgsPage(TaskSet):
    host = "https://zsbgs.zlxy.edu.cn"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "zsbgs.zlxy.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "sec-ch-ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    @tag('AAA')
    @task
    def t(self):
        with self.client.request(
                "GET",
                "/",
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Cookie": "JSESSIONID=4C9D59F59E0D1231A0E515D125BE214E",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "cross-site",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                },
                catch_response=True,
        ) as resp:
            pass
        with self.client.request(
                "GET",
                "/images/top_01.gif",
                headers={
                    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                    "Cookie": "JSESSIONID=4C9D59F59E0D1231A0E515D125BE214E",
                    "Referer": "https://zsbgs.zlxy.edu.cn/",
                    "Sec-Fetch-Dest": "image",
                    "Sec-Fetch-Mode": "no-cors",
                    "Sec-Fetch-Site": "same-origin",
                },
                catch_response=True,
        ) as resp:
            pass
        with self.client.request(
                "GET",
                "/images/16/04/27/6lywtqf3w4/5.jpg",
                headers={
                    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                    "Cookie": "JSESSIONID=DE2ADD319D0393F2A588F014E08755BE",
                    "Referer": "https://zsbgs.zlxy.edu.cn/",
                    "Sec-Fetch-Dest": "image",
                    "Sec-Fetch-Mode": "no-cors",
                    "Sec-Fetch-Site": "same-origin",
                },
                catch_response=True,
        ) as resp:
            pass
        with self.client.request(
                "GET",
                "/images/16/04/27/6lywtqf3w4/1.jpg",
                headers={
                    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                    "Cookie": "JSESSIONID=F707746B9D5CFB857347C6EA32A699F2",
                    "Referer": "https://zsbgs.zlxy.edu.cn/",
                    "Sec-Fetch-Dest": "image",
                    "Sec-Fetch-Mode": "no-cors",
                    "Sec-Fetch-Site": "same-origin",
                },
                catch_response=True,
        ) as resp:
            pass
        with self.client.request(
                "GET",
                "/zszc/zk.htm",
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Cookie": "JSESSIONID=F707746B9D5CFB857347C6EA32A699F2",
                    "Referer": "https://zsbgs.zlxy.edu.cn/",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                },
                catch_response=True,
        ) as resp:
            pass
        with self.client.request(
                "GET",
                "/images/listbg_04.gif",
                headers={
                    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                    "Cookie": "JSESSIONID=F707746B9D5CFB857347C6EA32A699F2",
                    "Referer": "https://zsbgs.zlxy.edu.cn/zszc/zk.htm",
                    "Sec-Fetch-Dest": "image",
                    "Sec-Fetch-Mode": "no-cors",
                    "Sec-Fetch-Site": "same-origin",
                },
                catch_response=True,
        ) as resp:
            pass

class websitUser(FastHttpUser):
    tasks = [ZsbgsPage]
    wait_time = between(1, 3)


if __name__ == "__main__":
    # run_single_user(zsbgs)
    cmd = "locust -f zsbgs.py --host=https://zsbgs.zlxy.edu.cn"
    os.system(cmd)
