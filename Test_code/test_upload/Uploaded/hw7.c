/*	Name: Ruijie Geng
	Section: 4
	Side: B
	Date: 2018/2/16

	Gain: 0.5
	Port pin: 1.4

	File name: hw7.c
	Description: 
	Use changable resistor to change the voltage input. And use AD_value to calculate the 
	input voltage. print the AD_value and voltage input

*/

#include <c8051_SDCC.h>// include files. This file is available online
#include <stdio.h>
#include <math.h>


//-----------------------------------------------------------------------------
// Function Prototypes
//-----------------------------------------------------------------------------
void ADC_Init(void);
void Port_Init(void);
unsigned char read_AD_input(unsigned char pin_number);



//-----------------------------------------------------------------------------
// Global Variables
//-----------------------------------------------------------------------------

int input_voltage;
unsigned char AD_value;


//***************
void main(void)
{
	Sys_Init();      // System Initialization
	putchar(' ');    // the quote fonts may not copy correctly into SiLabs IDE
	Port_Init(); 
	ADC_Init(); 	
	printf("Start \r\n");
    while (1) 
    {
		printf("enter key to read A/D input \r\n");
		getchar();

		// add code necessary to complete the homework
		AD_value = read_AD_input(4);	// my input port is 4
		input_voltage = (int) (1000.0 * AD_value * 2.4 / 256 / 0.5);

		printf("This is my input millivoltage %d \r\n", input_voltage);	// print statement as required by homework
		printf("This is my AD value %d \r\n", AD_value );	// print statement as required by homework

    }
}


//
// add the initialization code needed for the ADC1
//
void ADC_Init(void)
{
	REF0CN = 0x03;	 	// set reference and biase 
	ADC1CF &= ~0x03;	// clear the gain
	ADC1CF |= 0x00; 	// set gain to 0.5
	ADC1CN = 0x80;		// set ADC1 enable
}
//
// function that completes an A/D conversion
//
unsigned char read_AD_input(unsigned char pin_number)
{
	AMX1SL = pin_number;
	ADC1CN &= ~0x20;
	ADC1CN |= 0x10;
	while(ADC1CN & 0x20 == 0);
	return ADC1; 
}

//
// add Port initialization code
//
void Port_Init(void)
{
	P1MDIN &= ~0x10;
	P1MDOUT &= ~0x10;
	P1 |= 0x10; 
}

