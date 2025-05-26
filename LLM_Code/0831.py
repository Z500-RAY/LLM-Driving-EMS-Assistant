from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document
import faiss
import os
from uuid import uuid4
from langchain_core.tools import tool
import langchain
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import SequentialChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

import os

os.environ["OPENAI_API_KEY"] = "" # YOUR OPENAI_API_KEY
os.environ["LANGCHAIN_API_KEY"] = "" # YOUR LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "aviation"



from langchain.vectorstores import FAISS
# 使用合适的嵌入模型，例如 OpenAIEmbeddings 或其他你使用的嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5", 
                                   encode_kwargs={"normalize_embeddings": True})

# 加载 vector_store，并允许危险的反序列化
vector_store = FAISS.load_local("vectorstore.db", embeddings, allow_dangerous_deserialization=True)

# Create retriever
retriever = vector_store.as_retriever()


##prompt change
import serial
import time
import os
import json
import pyttsx3
from typing import Dict, Any
import langchain
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import SequentialChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
import re

ser = serial.Serial('COM3', 9600) 

# File path for simulator data
file_path = "C:/Users/888/Desktop/simulator_data.txt"
# file_path = "simulator_data_1s1.txt"

# Initialize file size for monitoring
last_file_size = 0

# Initialize the OpenAI model
llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0)
langchain.verbose = True

# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define LLM chains
first_prompt = ChatPromptTemplate.from_template("""
You will be given {flight_data}. 
The pilot is required to first execute a 45° steep turn to the right, completing a 360° turn, and then execute a 45° steep turn to the left, completing another 360° turn. 
Analyze flight data and determine the current phase of the steep turn with the data of angle of bank, pitch and heading. 
Return the current flight status as a string. Please strictly follow the category: 
1. Straight-and-Level Flying: Bank angle is close to 0 degrees, heading is stable.
2. Entry: Bank angle is increasing towards 40 degrees, heading is changing rapidly.
3. Maintaining the turn: Bank angle is maintained close to 45 degrees, heading is changing steadily, altitude is maintained.
4. Recovery: Heading is approaching 340 degrees, bank angle is decreasing towards 0 degrees, preparing to return to straight-and-level flight.
"""
)

chain_one = LLMChain(llm=llm, prompt=first_prompt, output_key="flight_status")


def getMyPrompt():
    prompt_template = """Use the following pieces of context to answer the users question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    There are multiple answers, provide each answer and the source file for each answer.
    \n\n{context}\n\nQuestion: Retrieve the related operational and attention guidance for the current status: {question}.  \n\n Answer:"""
    
    MyPrompt = PromptTemplate(
        template=prompt_template, input_variables=["context","question"]
    )
    return MyPrompt


chain_type_kwargs = {"prompt": getMyPrompt()}

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(),
    chain_type="stuff",
    input_key="flight_status",
    output_key="retrieved_guidance",
    chain_type_kwargs=chain_type_kwargs
)

third_prompt = ChatPromptTemplate.from_template(
    """
    Based on the {retrieved_guidance}, recommend specific joystick movements and the instruments to focus to optimize flight performance according to the current phase and maneuver.
    Strictly output the instruction as follows:
    flight_status= the current flight status
    pitch = forward/back/no
    roll = left/right/no
    instrument = 请在高度表/速度表/方向指示器/姿态指引仪选取一个目前最应该关注的仪表，请用中文给出需要注意的仪表名称。
    """
)

chain_three = LLMChain(llm=llm, prompt=third_prompt, output_key="answer")

overall_chain = SequentialChain(
    chains=[chain_one, qa, chain_three],
    input_variables=["flight_data"],
    output_variables=["flight_status", "retrieved_guidance", "answer"],
    verbose=True
)

# Track previous flight status
previous_flight_status = None

def save_to_file(data, file_path="flight_data_log.json"):
    # Check if the file exists
    print("1")
    if not os.path.exists(file_path):
        # Create a new file with an empty list if it doesn't exist
        with open(file_path, 'w') as f:
            json.dump([], f)

    # # Load the existing data, append the new data, and save it back
    # with open(file_path, 'r+') as f:
    #     print("2")
    #     file_data = json.load(f) # Load existing data
    #     file_data.append(data)     # Append new data
    #     f.seek(0)                  # Move the cursor to the beginning of the file
    #     json.dump(file_data, f, ensure_ascii=False, indent=4)  # Save updated data

    try:
        # Load the existing data
        with open(file_path, 'r+', encoding='utf-8') as f:
            try:
                file_data = json.load(f)  # Try to load existing data
            except json.JSONDecodeError:
                # Handle the case where the file is empty or contains invalid JSON
                file_data = []
                
            file_data.append(data)     # Append new data
            f.seek(0)                  # Move the cursor to the beginning of the file
            json.dump(file_data, f, ensure_ascii=False, indent=4)  # Save updated data
            f.truncate()               # Ensure the file is truncated if new data is shorter

    except IOError as e:
        print(f"An error occurred while handling the file: {e}")


def extract_flight_controls(response: Dict[str, Any]) -> Dict[str, str]:
    answer = response["answer"]
    print(f"Type of answer: {type(answer)}")
    answer = answer.replace("*", "")
    answer = answer.replace(":", " = ")
    
    # Use regular expressions to extract the relevant parts
    flight_status_match = re.search(r"flight_status\s*=\s*(.*)", answer)
    pitch_match = re.search(r"pitch\s*=\s*(forward|back|no)", answer)
    roll_match = re.search(r"roll\s*=\s*(left|right|no)", answer)
    # notice_match = re.search(r"Notice\s*=\s*(.*)", answer)
    instrument_match = re.search(r"instrument\s*=\s*([\u4e00-\u9fff，。！？、]*.*)", answer)
    
    # Extracted values
    flight_status = flight_status_match.group(1).strip() if flight_status_match else "Unknown"
    pitch = pitch_match.group(1).strip() if pitch_match else "Unknown"
    roll = roll_match.group(1).strip() if roll_match else "Unknown"
    instrument = instrument_match.group(1).strip() if instrument_match else ""

    return {
        "flight_status": flight_status,
        "pitch": pitch,
        "roll": roll,
        "instrument": instrument
    }

# Function to send data to the LLM and retrieve responses
def send_message_to_llm(flight_data: str):
    global previous_flight_status
    try:
        response = overall_chain({"flight_data": flight_data})
        
        # Debugging: Print the raw response to see what LLM returns
        print("Raw LLM Response:", response)

        # Ensure response is not empty and is valid JSON
        if not response:
            raise ValueError("LLM returned an empty response.")
        
        try:
            # Assuming the response needs to be parsed as JSON
            extracted_controls = extract_flight_controls(response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON. Error: {e}")
            return

        current_flight_status = extracted_controls["flight_status"]

        data_to_save = {
            "flight_status": current_flight_status,
            "pitch": extracted_controls["pitch"],
            "roll": extracted_controls["roll"],
            "instrument": extracted_controls.get("instrument", "")
        }

        if current_flight_status == previous_flight_status:
            # 仅包含pitch
            data_to_send = f"ppitch={extracted_controls['pitch']}"
            ser.write(data_to_send.encode('utf-8'))
            print(f"Sent1: {data_to_send}")
        else:
            # 包含pitch和roll
            # data_to_send = f"ppitch={extracted_controls['pitch']},roll={extracted_controls['roll']}"
            data_to_send = f"ppitch=no,roll={extracted_controls['roll']}"
            # data_to_send = f"ppitch={extracted_controls['pitch']}"
            ser.write(data_to_send.encode('utf-8'))
            print(f"Sent2: {data_to_send}")

            # if extracted_controls["notice"]:
            #     tts_announce(extracted_controls["notice"])

        save_to_file(data_to_save)

        previous_flight_status = current_flight_status

    except Exception as e:
        print(f"Failed to get a response from the LLM. Error: {e}")

# Function to announce messages using TTS
# def tts_announce(notice: str):
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 150)
#     engine.setProperty('volume', 0.9)
#     engine.say(notice)
#     engine.runAndWait()

# Continuously monitor the file for updates using readline
with open(file_path, 'r') as file:
    file.seek(0, os.SEEK_END)  # Move to the end of the file to read new lines

    while True:
        new_lines = []
        while True:
            line = file.readline()
            if not line:
                break
            new_lines.append(line.strip())

        if new_lines:
            # Process only the last line of the update
            last_line = new_lines[-1]
            print(f"Sending new content to LLM: {last_line}")
            send_message_to_llm(last_line)