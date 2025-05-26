#  FlightAxis

## Description

This repository contains the data and the code described in the paper ["Hand by Hand: LLM Driving EMS Assistant for Operational Skill Learning"](https://github.com/Z500-RAY/LLM-Driving-EMS-Assistant/blob/main/IJCAI__25_Submitting.pdf) by Wei Xiang, Ziyue Lei, Haoyuan Che, Fangyuan Ye, Xueting Wu and Lingyun Sun, to appear in Proceedings of the 34th International Joint Conference on Artificial Intelligence (IJCAI 2025), Special Track on: Human-Centred Artificial Intelligence: Multidisciplinary Contours and Challenges of Next-Generation AI Research and Applications., 16-22 August, Montreal, Canada.

## Directory structure
- **Main_Code**  
  Contains three primary Python scripts that drive the system:
  - `process1.py` activates the Python environment and runs the code that invokes the LLM.
  - `process2.py` activates the Python environment and runs the code that extracts flight data from Microsoft Flight Simulator.
  - `process3.py` saves the user’s in-flight data locally so that it can be retrieved and analyzed by the LLM.

- **Data_collection_code**  
  Based on the open-source project MSFS2020-cockpit-companion, this folder houses the code that collects user flight data via Microsoft Flight Simulator’s official SimConnect interface. A locally deployed Flask server streams simulator data in real time. We adapted this project (and followed the SimConnect documentation: https://learn.microsoft.com/en-us/previous-versions/microsoft-esp/cc526981(v=msdn.10)) to select the relevant data fields, set the polling frequency, and store the results locally for subsequent LLM analysis.

- **LLM_Code**  
  Contains the programs that send collected flight data to the LLM, use Retrieval-Augmented Generation (RAG) over professional flight-training materials to assess task performance, and generate feedback:
  - `0831.py` transmits the locally recorded simulator data to the LLM. It leverages LangChain’s LLM tools (https://www.langchain.com/) and employs a step-by-step RAG approach to improve judgment accuracy.
  - `0903.py` extracts the LLM’s assessment and issues voice-based prompts to the user.

- **Arduino_Code**  
  Includes two modules for electrical muscle stimulation (EMS):
  - **CalibrationEMS**: for calibrating the EMS device.
  - **EmpiricalStudyEMS**: for converting the LLM’s guidance into stimulation signals during the actual experiment.

-  **Flight_Simulator_Experiment_Materials**
    Includes questionnaires evaluating participants' experiences and knowledge, along with data on their performance and progress.  This folder also contains valuable knowledge bases that support the simulation environment.

## How to run the project

1. **Create Python virtual environments**  
   - `aviation` and `mfs2020`, and install the required dependencies.

2. **Calibrate the EMS device**  
   - Affix the electrode patches to the designated positions on the user’s arm.  
   - Run `./Arduino_Code/CalibrationEMS/CalibrationEMS.ino` and adjust the stimulation-intensity parameters in the code and/or the electrode placement until the desired feedback level is achieved.

3. **Initialize data-logging files**  
   - Run `process3.py` to create, on your desktop, two files for recording (a) raw simulator data and (b) LLM assessment results.

4. **Prepare the simulator**  
   - Launch Microsoft Flight Simulator on your PC and configure it so the aircraft is ready for takeoff.

5. **Start the LLM-invocation process**  
   - Run `process1.py` and, in the simulator’s UI, click “Start Flight” to begin the session.

6. **Begin data extraction**  
   - Immediately after the flight starts, run `process2.py` to extract in-flight telemetry via SimConnect.

7. **Verify successful operation**  
   - If the user perceives electrical-muscle-stimulation feedback (i.e. the LLM’s guidance), the system is running correctly.  
   - The raw flight data and the LLM’s judgments will be saved respectively in `simulator_data.txt` and `flight_data_log.json`, both created by `process3.py`.

## Contacts

For any inquiry about FlightAxis, you can send an email to: <wxiang@zju.edu.cn>, <zy_lei@zju.edu.cn>, <chaoyuan0116@zju.edu.cn>, <yefangyuanzju@gmail.com>.