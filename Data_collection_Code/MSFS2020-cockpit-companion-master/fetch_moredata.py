import requests
import os
import time

# 定义API URL及对应的文件名
api_endpoints = {
    "http://localhost:5000/dataset/compass": "compass_data.txt",
    "http://localhost:5000/dataset/throttle": "throttle_data.txt",
    # 添加其他API URL及对应的文件名
}

def get_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def append_data_to_file():
    while True:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        for url, filename in api_endpoints.items():
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_path, filename)
            data = get_data(url)
            if data:
                with open(file_path, 'a') as file:
                    file.write(f"{current_time} {data}\n")
                print(f"{current_time} finish for {url}")
        time.sleep(5)

if __name__ == "__main__":
    append_data_to_file()
