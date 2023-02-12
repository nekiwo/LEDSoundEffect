#include "FastLED.h"

#define NUM_LEDS 138
#define PIN_NUM 6

CRGB leds[NUM_LEDS];
int x;
int prev = 1;

int point = 1;

int lowPassFilter(float actual, float target, float value)
{
    return int(floor(actual + ((target - actual) * value)));
}

void setup()
{
    FastLED.addLeds<WS2812, PIN_NUM>(leds, NUM_LEDS);

    Serial.begin(500000);
    Serial.setTimeout(1);
}

void loop()
{
    while (!Serial.available())
        ;
    x = lowPassFilter(prev, Serial.readString().toFloat(), 0.7) % (NUM_LEDS - 1);
    prev = x;

    if (x > 0)
    {
        for (int i = 0; i < x; i++)
        {
            CRGB color = CHSV(255 - 255 * (float((i) % 68) / 68), 255, 50);

            leds[70 + i] = color;
            leds[69 - i] = color;
        }

        for (int i = x; i < 69; i++)
        {
            CRGB color = CRGB(0, 0, 0);

            leds[70 + i] = color;
            leds[69 - i] = color;
        }

        FastLED.show();
    }
}