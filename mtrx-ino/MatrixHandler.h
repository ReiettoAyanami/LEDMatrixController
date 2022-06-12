#include <FastLED.h>
#define ON true
#define OFF false


class MatrixHandler{

    public:

        MatrixHandler(CRGB*, const uint8_t);
        ~MatrixHandler();
        void clear();
        void turn(bool, CRGB*);
        void setLeds(CRGB*);
        void setLedsLastState(CRGB*);
        CRGB* getLeds();
        CRGB* getLedsLastState();

    private:

        CRGB* leds;
        uint8_t size;

};

MatrixHandler::MatrixHandler(CRGB* l, const uint8_t s){

    this -> leds = l;
    this -> size = s;

}

MatrixHandler::~MatrixHandler(){

}


CRGB* MatrixHandler::getLeds(){
    return this -> leds;
}

void MatrixHandler::setLeds(CRGB* new_leds){

    this -> leds = new_leds;

}


void MatrixHandler::clear(){


    for(uint8_t i = 0; i < this -> size; ++i){

        this -> leds[i] = CRGB(0,0,0);

    }

}

void MatrixHandler::turn(bool sw,CRGB* ledState){

    if(sw){

        FastLED.show();
        
    }

}


