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
  
}
