# coding:utf-8

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                print('交换',arr[j + 1], arr[j])
                swapped = True
        print(f'执行次数{i+1},{arr}')
        # 如果在整个内部循环中都没有交换，则数组已经是排序好的
        if not swapped:
            break
    return arr


if __name__ == '__main__':
    # 测试示例
    arr = [4, 34, 25, 102, 202, 303, 90]
    sorted_arr = bubble_sort(arr)
    print("排序后的数组:", sorted_arr)
