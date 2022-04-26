#include <Wire.h>
#include "Adafruit_DRV2605.h"

Adafruit_DRV2605 drv;

int Strength = 0;
int NewStrength = 0;
const int MaxChars = 4;
char strValue[MaxChars+1];
int index = 0;

void setup()
{
  Serial.begin(9600);
  Serial.println("DRV test");
  drv.begin();
  
  drv.selectLibrary(1);
  drv.setMode(DRV2605_MODE_INTTRIG); 
}
void loop(){

  }

// Detects a serial input event, with the input being strength setting of Adafruit

void serialEvent()
{
   while(Serial.available()) 
   {
      char ch = Serial.read();
      Serial.write(ch);
      
      // Reconstructs string of strength number
      
      if(index < MaxChars && isDigit(ch)) { 
            strValue[index++] = ch; 
      } else { 
        // once reconstructed, the Adafruit driver is actuated ONCE at the desired strength setting
            strValue[index] = 0; 
            NewStrength = atoi(strValue); 
            drv.setWaveform(0, NewStrength);
            drv.setWaveform(1, 0);
            drv.go();
            index = 0;
      }  
   }
}
