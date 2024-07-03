# coding:utf-8
import re


def is_prime(n):
    # 素数必须大于1
    if n <= 1:
        return False
    # 2是唯一的偶数素数
    if n == 2:
        return True
    # 排除所有偶数
    if n % 2 == 0:
        return False
    # 检查从3到sqrt(n)的奇数是否能整除n
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


# 示例使用
number = 7
print(f"{number} 是素数: {is_prime(number)}")

A = re.search('super', 'AsuperB')
B = re.search('super', 'superAB')
C = re.match('super', 'AsuperB')
D = re.match('super', 'superAB')


def result(D):
    if D:
        print(D.span())
    else:
        print(D)


result(D)

import base64

encoded_string = "5nBUI6LcEFqLfuiWjQ6B0Mpakdc="
try:
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')  # 尝试将字节解码为UTF-8字符串
    print(decoded_string)
except Exception as e:
    print("解码失败:", e)
