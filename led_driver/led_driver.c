#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>
#include <wiringPi.h>

const int CKI = 22;
const int SDI = 23;
int cntLeds = 10;

void resetLeds(void);
 
int main(int argc, char* argv[])
{
	wiringPiSetupGpio();
	
	pinMode(CKI, OUTPUT);
	pinMode(SDI, OUTPUT);

	if (argc < 3) {
		return 0;
	}

	int index;
 	for(index = 0; index < argc; index++) {
    		printf("The %d is %s\n",index,argv[index]);
  	}

	resetLeds();
	
	/* API: <count_leds> <hexcode_1>...<hexcode_n>*/
	cntLeds  = (int)strtol(argv[1], NULL, 10);
	printf("Setting %i leds\n", cntLeds);

	int i;	
	for (i = 1; i <= cntLeds; i++) {
		char colorHex[50];
		strcpy(colorHex, argv[1 + i]);
		long color = strtol(colorHex, NULL, 0);		
		printf("Setting led #%i with color %d (%s)\n", i+1, color, colorHex);

		int j = 23;
		for (j; j >= 0; j--) {				
			long bitMask = 1 << j;
						
			digitalWrite(CKI, LOW);
			
			if (color & bitMask) {					
				digitalWrite(SDI, HIGH);
			} else {					
				digitalWrite(SDI, LOW);
			}
			
			digitalWrite(CKI, HIGH);
		}	
	}	

	digitalWrite(CKI, LOW);
	delayMicroseconds(1000);

	return 0;
}

void resetLeds()
{				
	int nrLed = 0;
	int count = 10;
	long color = 0x000000;
	
	for (nrLed; nrLed < count; nrLed++) {
		int i = 23;
		for (i; i >= 0; i--) {				
			long bitMask = 1 << i;
			digitalWrite(CKI, LOW);
			
			if (color & bitMask) {					
				digitalWrite(SDI, HIGH);
			} else {					
				digitalWrite(SDI, LOW);
			}
			
			digitalWrite(CKI, HIGH);
		}			
	}
	
	digitalWrite(CKI, LOW);
	delayMicroseconds(3000);				
}
