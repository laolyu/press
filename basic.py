# coding:utf-8
import os

from locust import HttpUser, between, task

import time


class Quickstart(HttpUser):
    wait_time = between(1, 5)

    @task
    def google(self):
        self.client.request_name = "google"
        self.client.get("https://google.com/")

    @task
    def microsoft(self):
        self.client.request_name = "microsoft"
        self.client.get("https://microsoft.com/")

    @task
    def facebook(self):
        self.client.request_name = "facebook"
        self.client.get("https://facebook.com/")


if __name__ == "__main__":
    # run_single_user(zsbgs)
    cmd = "locust -f basic.py"
    os.system(cmd)
   