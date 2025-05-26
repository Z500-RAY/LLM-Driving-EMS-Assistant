import json
import time
import pyttsx3

# 初始化TTS引擎
engine = pyttsx3.init()

# 设置JSON文件路径
json_file_path = "flight_data_log.json"

# 用于记录已读取的条目数
last_line_count = 0

def read_json_and_speak_notices():
    global last_line_count
    
    while True:
        try:
            # 打开并读取JSON文件
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # 检查新添加的条目
            if len(data) > last_line_count:
                new_entries = data[last_line_count:]
                
                for entry in new_entries:
                    notice = entry.get("instrument", "")
                    if notice:
                        # 朗读notice字段
                        engine.say(notice)
                        print("work")
                        engine.runAndWait()
                
                # 更新已处理的条目数
                last_line_count = len(data)
        
        except Exception as e:
            print(f"Error reading file or processing data: {e}")
        
        # 每隔几秒钟检查文件更新
        time.sleep(1)

if __name__ == "__main__":
    read_json_and_speak_notices()
