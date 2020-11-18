#include <Wire.h>
#include <Adafruit_AMG88xx.h>

Adafruit_AMG88xx amg;

float pixels[AMG88xx_PIXEL_ARRAY_SIZE];

void setup() {
    Serial.begin(115200);
    while (!Serial);

    bool status;

    status = amg.begin();
    if (!status) {
        Serial.println("AMG88xx sensor missing");
        while (1);
    }
    delay(100);
}

void loop() { 
    amg.readPixels(pixels);

    for(int i=1; i<=AMG88xx_PIXEL_ARRAY_SIZE; i++){
      Serial.print(pixels[i-1]);
      Serial.print(" ");
    }
    Serial.println();

    delay(5000);
}
