import requests
import os
import time

# 设置要获取的数据集名称
dataset_name = 'detect'  # 根据需要更改

# 文件路径
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "detect_data.txt")

# 获取数据并追加到文件的函数
def fetch_and_append_data():
    while True:
        response = requests.get(f'http://localhost:5000/dataset/{dataset_name}')
        data = response.json()

        # 获取当前时间
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # 准备要写入的数据
        data_to_write = f'{current_time} {data}\n'

        # 将数据追加到文件中
        with open(file_path, 'a') as file:
            file.write(data_to_write)
            print(f"{current_time} finish")

# 开始获取数据并追加到文件中
fetch_and_append_data()
