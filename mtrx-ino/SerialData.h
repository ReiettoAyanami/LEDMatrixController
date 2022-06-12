#include <FastLED.h>
#define MIN_DATA_IN 50
#define OUT_CONNECTION_STARTER 17
#define IN_CONNECTION_STARTER "17"
#define IN_CONNECTION_CONFIRM 18

class SerialData{

    public:
        
        
        SerialData();
        ~SerialData();

        bool getConnectionInStable();

        String receive(const char);
        void startConnection(const uint8_t, const String, const uint8_t);
        void parseData(String, CRGB*);
        
    
    private:
        uint8_t dataInCount = 0;
        bool connectionInStarted = false;
        bool connectionInStable = false;
    

};

SerialData::SerialData(){

}
SerialData::~SerialData(){
    
}

bool SerialData::getConnectionInStable(){
    return this -> connectionInStable;
}


void SerialData::parseData(String dataIn, CRGB* leds){
    if(dataIn.startsWith(".")){
        uint8_t i = dataIn.substring(1,4).toInt();
        leds[i] =  CRGB(dataIn.substring(4,7).toInt(), dataIn.substring(7,10).toInt(),dataIn.substring(10,13).toInt());
    }
}

void SerialData::startConnection(const uint8_t startDataOut, const String startDataIn, const uint8_t minDataIn){

    if(Serial.availableForWrite()){

        Serial.write(startDataOut);

    }
    if(Serial.available()){

        if(Serial.readStringUntil('\n').equalsIgnoreCase(startDataIn)){

            this -> dataInCount++;
            this -> connectionInStarted = true;

        }
        
        if(this -> dataInCount == minDataIn){

            
            
            if(Serial.availableForWrite()){

                Serial.write(IN_CONNECTION_CONFIRM);
                this -> connectionInStable = true;
                
            }



        }



    }


}



String SerialData::receive(const char termChar){

    if(Serial.available() >= 0){
        //this -> isReceiveing = true;
        return Serial.readStringUntil(termChar);
        //Serial.write("Connection ongoing\n");

    }
    else{
        //this -> isReceiveing = false;
        return ".000000000000";
    }

}

