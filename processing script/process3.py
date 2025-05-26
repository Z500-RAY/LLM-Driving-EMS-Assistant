import os

# 清空文件内容的函数
def clear_file_content(file_path):
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 以写入模式打开文件（会清空文件内容）
        with open(file_path, 'w') as file:
            pass  # 直接写入空内容
        print(f"已清空文件内容: {file_path}")
    else:
        print(f"文件未找到: {file_path}")

# 设置文件路径
simulator_data_path = "C:/Users/888/Desktop/simulator_data.txt"
flight_data_log_path = "C:/Users/888/Desktop/0824/flight_data_log.json"

# 清空指定文件的内容
clear_file_content(simulator_data_path)
clear_file_content(flight_data_log_path)