unsigned long setupCompletionTime;  // 用于存储 setup() 函数执行完成的时间

int status1 = 0;
int status2 = 0;
int status3 = 0;
int status4 = 0;
int judgeStatus = 0;
int judgePitch = 0;
int judgeRoll = 0;

// 定义继电器控制引脚
const int relay1 = 2;
const int relay2 = 3;
const int relay3 = 4;
const int relay4 = 5;
const int relay5 = 6;
const int relay6 = 7;
const int relay7 = 8;
const int relay8 = 9;

const int relay9 = 10;
const int relay10 = 11;
const int relay11 = 12;
const int relay12 = 13;

// 四个中的最小力度
const int strength = 6;

//1号机的大小与strength的差值
const int strength1 = 0;
//2号机的大小与strength的差值
const int strength2 = 3;
//3号机的大小与strength的差值
const int strength3 = 3;
//4号机的大小与strength的差值
const int strength4 = 2; 

const int addTimes = strength - 1;
const int minusTimes = strength - 2;
const int addClock = 40 * addTimes;
const int adjustTime = 4000 - addClock;
const int minusTime = 2500 - addClock;
const int minusTimeAverage = minusTime / minusTimes;
const int maintainTime = minusTimeAverage - 20;


void setup() {
  Serial.begin(9600); // 初始化串口通信，波特率为9600

  // 初始化继电器控制引脚为输出模式
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A5, OUTPUT);

  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  pinMode(relay5, OUTPUT);
  pinMode(relay6, OUTPUT);
  pinMode(relay7, OUTPUT);
  pinMode(relay8, OUTPUT);

  pinMode(relay12, OUTPUT);
  pinMode(relay11, OUTPUT);
  pinMode(relay10, OUTPUT);
  pinMode(relay9, OUTPUT);

  // 确保继电器初始为关闭状态
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A5, LOW);

  digitalWrite(relay1, LOW);
  digitalWrite(relay2, LOW);
  digitalWrite(relay3, LOW);
  digitalWrite(relay4, LOW);
  digitalWrite(relay5, LOW);
  digitalWrite(relay6, LOW);
  digitalWrite(relay7, LOW);
  digitalWrite(relay8, LOW);

  digitalWrite(relay12, LOW);
  digitalWrite(relay11, LOW);
  digitalWrite(relay10, LOW);
  digitalWrite(relay9, LOW);


  // //right
  delay(20000);
  digitalWrite(A5, HIGH);
  delay(500);
  digitalWrite(A5, LOW);
  delay(500);

  digitalWrite(A0, HIGH);
  delay(200);
  digitalWrite(A0, LOW);
  delay(1000);
  blinkPin(A1, 6, 30);
  for (int i = 0; i < 9; i++){
    digitalWrite(relay3, HIGH);
    delay(20);
    digitalWrite(relay3, LOW);
    delay(20);
  }

  digitalWrite(relay11, HIGH);
  delay(1000);
  for (int i = 0; i < minusTimes; i++){
    digitalWrite(relay4, HIGH);
    delay(20);
    digitalWrite(relay4, LOW);
    delay(maintainTime);
  }
  digitalWrite(relay11, LOW);

  // //left
  // delay(2000);
  // digitalWrite(A5, HIGH);
  // delay(500);
  // digitalWrite(A5, LOW);
  // delay(500);

  // digitalWrite(A0, HIGH);
  // delay(200);
  // digitalWrite(A0, LOW);
  // delay(1000);
  // blinkPin(A1, 6, 30);
  // for (int i = 0; i < 8; i++){
  //   digitalWrite(relay7, HIGH);
  //   delay(20);
  //   digitalWrite(relay7, LOW);
  //   delay(20);
  // }

  // digitalWrite(relay9, HIGH);
  // delay(2000);
  // for (int i = 0; i < minusTimes; i++){
  //   digitalWrite(relay8, HIGH);
  //   delay(20);
  //   digitalWrite(relay8, LOW);
  //   delay(maintainTime);
  // }
  // digitalWrite(relay9, LOW);

  // //forward
  // delay(2000);
  // digitalWrite(A5, HIGH);
  // delay(500);
  // digitalWrite(A5, LOW);
  // delay(500);

  // digitalWrite(A0, HIGH);
  // delay(200);
  // digitalWrite(A0, LOW);
  // delay(1000);
  // blinkPin(A1, 6, 30);
  // for (int i = 0; i < 9; i++){
  //   digitalWrite(relay5, HIGH);
  //   delay(20);
  //   digitalWrite(relay5, LOW);
  //   delay(20);
  // }

  // digitalWrite(relay10, HIGH);
  // delay(2000);
  // for (int i = 0; i < minusTimes; i++){
  //   digitalWrite(relay4, HIGH);
  //   delay(20);
  //   digitalWrite(relay4, LOW);
  //   delay(maintainTime);
  // }
  // digitalWrite(relay10, LOW);

    // // // back
    // delay(2000);
    // digitalWrite(A5, HIGH);
    // delay(500);
    // digitalWrite(A5, LOW);
    // delay(500);

    // digitalWrite(A0, HIGH);
    // delay(200);
    // digitalWrite(A0, LOW);
    // delay(1000);
    // blinkPin(A1, 6, 30);
    // for (int i = 0; i < 6; i++){
    //   digitalWrite(relay1, HIGH);
    //   delay(20);
    //   digitalWrite(relay1, LOW);
    //   delay(20);
    // }

    // digitalWrite(relay12, HIGH);
    // delay(2000);
    // for (int i = 0; i < minusTimes; i++){
    //   digitalWrite(relay4, HIGH);
    //   delay(20);
    //   digitalWrite(relay4, LOW);
    //   delay(maintainTime);
    // }
    // digitalWrite(relay12, LOW);


  digitalWrite(A0, HIGH);
  delay(200);
  digitalWrite(A0, LOW);

}

void loop() {
  while (!Serial) {
    ; 
  }
  if (Serial.available() > 0) {

    Serial.read();

    digitalWrite(A5, HIGH);
    delay(20);
    digitalWrite(A5, LOW);
 
    String input = Serial.readStringUntil('\n');

    Serial.println(input);

    Serial.println(input);

    parseMessage(input);

    if (judgeStatus == 0) {
      delay(500);
      Serial.println("JudgeStatus is 0, waiting for next message...");
    } else if (judgeStatus == 1) {
      executeOperations(strength,strength1,strength2,strength3,strength4);
      if (status1 == 1){
        digitalWrite(relay12, HIGH);
        delay(1500);
        for (int i = 0; i < minusTimes; i++){
          digitalWrite(relay2, HIGH);
          delay(20);
          digitalWrite(relay2, LOW);
          delay(maintainTime);
        }
        digitalWrite(relay12, LOW);
      }
      if (status2 == 1){
        digitalWrite(relay11, HIGH);
        delay(1500);
        for (int i = 0; i < minusTimes; i++){
          digitalWrite(relay4, HIGH);
          delay(20);
          digitalWrite(relay4, LOW);
          delay(maintainTime);
        }
        digitalWrite(relay11, LOW);

      }
      if (status3 == 1){
        digitalWrite(relay10, HIGH);
        delay(1500);
        for (int i = 0; i < minusTimes; i++){
          digitalWrite(relay6, HIGH);
          delay(20);
          digitalWrite(relay6, LOW);
          delay(maintainTime);
        }
        digitalWrite(relay10, LOW);

      }
      if (status4 == 1){
        digitalWrite(relay9, HIGH);
        delay(1800);
        for (int i = 0; i < minusTimes; i++){
          digitalWrite(relay8, HIGH);
          delay(20);
          digitalWrite(relay8, LOW);
          delay(maintainTime);
        }
        digitalWrite(relay9, LOW);
      }
      digitalWrite(A0, HIGH);
      delay(1000);
      digitalWrite(A0, LOW);
    } else if (judgeStatus == 2) {
      // 当 judgeStatus 不为 0 时，执行后续操作
      executeOperations(strength,strength1,strength2,strength3,strength4);
      if (judgePitch > 0 && judgeRoll > 0) {
        digitalWrite(relay11, HIGH);
        digitalWrite(relay12, HIGH);
        delay(1500);
        for (int i = 0; i < minusTimes ; i++){
          digitalWrite(relay2, HIGH);
          digitalWrite(relay4, HIGH);
          delay(20);
          digitalWrite(relay2, LOW);
          digitalWrite(relay4, LOW);
          delay(maintainTime);
        }
        digitalWrite(relay11, LOW);
        digitalWrite(relay12, LOW);
      } else if (judgePitch > 0 && judgeRoll < 0) {
        digitalWrite(relay9, HIGH);
        digitalWrite(relay12, HIGH);
        delay(1500);
        for (int i = 0; i < minusTimes ; i++){
          digitalWrite(relay2, HIGH);
          digitalWrite(relay8, HIGH);
          delay(20);
          digitalWrite(relay2, LOW);
          digitalWrite(relay8, LOW);
          delay(maintainTime);
        }
        digitalWrite(relay9, LOW);
        digitalWrite(relay12, LOW);
      } else if (judgePitch < 0 && judgeRoll > 0) {
        digitalWrite(relay10, HIGH);
        digitalWrite(relay11, HIGH);
        delay(1500);
        for (int i = 0; i < minusTimes ; i++){
          digitalWrite(relay4, HIGH);
          digitalWrite(relay6, HIGH);
          delay(20);
          digitalWrite(relay4, LOW);
          digitalWrite(relay6, LOW);
          delay(maintainTime);
        }
        digitalWrite(relay10, LOW);
        digitalWrite(relay11, LOW);
      } else if (judgePitch < 0 && judgeRoll < 0) {
        digitalWrite(relay9, HIGH);
        digitalWrite(relay10, HIGH);
        delay(1500);
        for (int i = 0; i < minusTimes ; i++){
          digitalWrite(relay6, HIGH);
          digitalWrite(relay8, HIGH);
          delay(20);
          digitalWrite(relay6, LOW);
          digitalWrite(relay8, LOW);
          delay(maintainTime);
        }
        digitalWrite(relay9, LOW);
        digitalWrite(relay10, LOW);
      }
      digitalWrite(A0, HIGH);
      delay(1000);
      digitalWrite(A0, LOW);
    }
    status1 = 0;
    status2 = 0;
    status3 = 0;
    status4 = 0;  
    judgeStatus = 0;
    judgePitch = 0;
    judgeRoll = 0;
    input = "";
  }
  
}

void blinkPin(int pin, int times, int delayTime) {
  for (int i = 0; i < times; i++) {
    digitalWrite(pin, HIGH);
    delay(delayTime);
    digitalWrite(pin, LOW);
    delay(delayTime);
  }
}

void parseMessage(String message) {
  String pitchDir = "no";  // 默认值
  String rollDir = "no";   // 默认值


 // 查找并提取 pitch 值
  int pitchIndex = message.indexOf("pitch=");
  if (pitchIndex != -1) {
    pitchDir = extractValue(message, pitchIndex + 6);  // 从 "pitch=" 后开始提取值
  }

  // 查找并提取 roll 值
  int rollIndex = message.indexOf("roll=");
  if (rollIndex != -1) {
    rollDir = extractValue(message, rollIndex + 5);  // 从 "roll=" 后开始提取值
  }

  parseInput(pitchDir, rollDir);
}

String extractValue(String data, int startIndex) {
  // 从起始位置查找到下一个逗号或者字符串结束
  int commaIndex = data.indexOf(",", startIndex);
  if (commaIndex == -1) {
    // 如果没有找到逗号，返回到字符串结束
    return data.substring(startIndex);
  } else {
    // 提取从起始位置到逗号之间的值
    return data.substring(startIndex, commaIndex);
  }
}

void parseInput(String pitchDir, String rollDir) {
  if (pitchDir == "no"){
    status1 = 0;
    status3 = 0;
  } else if (pitchDir == "back") {
    status1 = 1;
    status3 = 0;
  } else if (pitchDir == "forward") {
    status1 = 0;
    status3 = 1;
  }

  if (rollDir == "no"){
    status2 = 0;
    status4 = 0;
  } else if (rollDir == "right") {
    status2 = 1;
    status4 = 0;
  } else if (rollDir == "left") {
    status2 = 0;
    status4 = 1;
  }
  // 根据status的值控制是否执行操作
  judgeStatus = status1 + status2 + status3 + status4;
  judgePitch = status1 - status3;
  judgeRoll = status2 - status4;
}

void executeOperations(int times,int times1,int times2,int times3,int times4){
  digitalWrite(A0, HIGH);
  delay(200);
  digitalWrite(A0, LOW);
  delay(1000);
  blinkPin(A1, 6, 30);

  // int addTimes = times - 2;
   int addTimes = times ;

  for (int i = 0; i < addTimes; i++){
    digitalWrite(relay1, HIGH);
    digitalWrite(relay3, HIGH);
    digitalWrite(relay5, HIGH);
    digitalWrite(relay7, HIGH);
    delay(20);
    digitalWrite(relay1, LOW);
    digitalWrite(relay3, LOW);
    digitalWrite(relay5, LOW);
    digitalWrite(relay7, LOW);
    delay(20);
  }
  for (int i = 0; i < times1; i++){
    digitalWrite(relay1, HIGH);
    delay(20);
    digitalWrite(relay1, LOW);
    delay(20);
  }
  for (int i = 0; i < times2; i++){
    digitalWrite(relay3, HIGH);
    delay(20);
    digitalWrite(relay3, LOW);
    delay(20);
  }
  for (int i = 0; i < times3; i++){
    digitalWrite(relay5, HIGH);
    delay(20);
    digitalWrite(relay5, LOW);
    delay(20);
  }
  for (int i = 0; i < times4; i++){
    digitalWrite(relay7, HIGH);
    delay(20);
    digitalWrite(relay7, LOW);
    delay(20);
  }
}

