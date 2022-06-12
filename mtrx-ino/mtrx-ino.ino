#include <FastLED.h>
#include "SerialData.h"
#include "MatrixHandler.h"

#define DATA_TERM '\n'
#define POWER_UP_DELAY 3000
#define DIN 5
#define N_LED 64
#define BRIGHTNESS 1
#define LED_TYPE WS2811
#define COLOR_ORDER GRB
#define UPDATES_PER_SECOND 100

CRGB leds[N_LED];
long index = 0;
String receivedData;
SerialData data;
MatrixHandler matrix(leds, N_LED);

void setup() {

  delay(POWER_UP_DELAY);
  pinMode(13, OUTPUT);
  FastLED.addLeds<LED_TYPE, DIN, COLOR_ORDER>(matrix.getLeds(), N_LED).setCorrection(TypicalLEDStrip);
  Serial.begin(9600);
  matrix.clear();
}


void loop() {
  
  if(!data.getConnectionInStable()) data.startConnection(OUT_CONNECTION_STARTER, IN_CONNECTION_STARTER, MIN_DATA_IN);
  else
  {

    receivedData = data.receive(DATA_TERM);
    data.parseData(receivedData, matrix.getLeds());
    matrix.turn(ON, matrix.getLeds());

  }
}

