#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

unsigned long previousMillis = 0;
const long interval = 500; // 5 seconds

int Vo = A1;
int V_LED = 2;  

float Vo_value = 0;
float Voltage = 0;
float dustDensity = 0;

bool displayHumidityTemp = true;

void setup() {
  Serial.begin(9600);
  
  pinMode(A0, INPUT);
  pinMode(V_LED, OUTPUT);
  pinMode(Vo, INPUT);
  
  dht.begin();
}

void loop() {
  unsigned long currentMillis = millis();
  int sv = analogRead(A0);

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    float humi, temp;
    temp = dht.readTemperature();
    humi = dht.readHumidity();

    digitalWrite(V_LED, LOW);
    delayMicroseconds(280);
    Vo_value = analogRead(Vo);
    delayMicroseconds(40);
    digitalWrite(V_LED, HIGH);
    delayMicroseconds(9680);

    Voltage = Vo_value * 5.0 / 1023.0;
    dustDensity = (Voltage - 0.3) / 0.005;

    if (isnan(humi) || isnan(temp)) {
      Serial.println("Failed to read from DHT Sensor!!");
      return;
    }
    
    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.print("°C , Humidity: ");
    Serial.print(humi);
    Serial.print("%, CO2: ");
    Serial.print(sv);
    Serial.print("ppm , PM10: ");
    Serial.print(dustDensity);
    Serial.println(" ug/m3");
  }
}
