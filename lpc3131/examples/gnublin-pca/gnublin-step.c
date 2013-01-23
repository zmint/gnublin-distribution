
#include <stdio.h> 
#include <stdlib.h>
#include <fcntl.h> 
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <unistd.h>
#include <getopt.h>


#define ADDR 0x20

unsigned int position = 0;
int c,hflag;
char *filename = "/dev/i2c-1"; 
int slave_address = ADDR; 
int json_flag = 0;



void parse_opts(int argc, char **argv)
{	
	
	while((c = getopt(argc,argv,"hjp:d:a:")) != -1)
	{
		switch(c)
		{
			case 'h' : hflag = 1;                               break;				/* help */
			case 'p' : position = atoi(optarg);                 break;
			case 'd' : filename = optarg;                       break;
			case 'a' : slave_address = strtol (optarg,NULL,16); break;
			case 'j' : json_flag = 1;                           break;
		}

	}
	if (hflag)
	{
		printf("This program is designed, to easily interact with port expanders connected to the GNUBLIN.\n-h\t\t\tShow this help\n-d <device>\t\tSpecify the i2c-device.default=1\n-j\t\t\tConvert output to json format.\n-a <I2C-address>\tSpecify the port expanders I2C-address.default=0x20\n-p <pin>\t\tSpecify the desired pin\n\nExample:\ngnublin-step -a 0x60 -p 3000  <-Drive the motor to position 3000 and use I2C-address 0x60.\n\nA complete rotation is position 3200, two rotations 6400 and so on.\n");		
	exit(1);
		
	}
}


int main (int argc, char **argv) { 

    int fd; 
    unsigned char buffer[128];
    unsigned char rx_buf[128];
    unsigned int n, err,test; 
    
    parse_opts(argc, argv);
    
    
    if (argc == 0) {
	printf("This program is designed, to easily interact with a stepper-motor connected to the GNUBLIN.\n-h\t\t\tShow this help\n-f <device>\t\tSpecify the i2c-device.default=/dev/i2c-1\n-j\t\t\tConvert output to json format.\n-a <I2C-address>\tSpecify the stepper modules I2C-address.default=0x60\n-p <Position>\t\tSpecify the desired position\n\nExample:\ngnublin-step -a 0x60 -p 3000  <-Drive the motor to position 3000 and use I2C-address 0x60.\n\nA complete rotation is position 3200, two rotations 6400 and so on.\n");
      //exit(1);
		}





    if ((fd = open(filename, O_RDWR)) < 0) { 
      if (json_flag == 1)
          printf("{\"error_msg\" : \"Failed to open i2c device \",\"result\" : \"-1\"}\n");
      else
        printf("Failed to open i2c device"); 
        return -1; 
    } 

    if (ioctl(fd, I2C_SLAVE, slave_address) < 0) { 
      if (json_flag == 1)
          printf("{\"error_msg\" : \"Failed to open i2c device \",\"result\" : \"-1\"}\n");
      else
        printf("ioctl I2C_SLAVE error"); 
        return -1; 
    } 


    
      //GestFullStatus1 Command: This Command must be executed before Operating
      buffer[0] = 0x81;   

      if (write(fd, buffer, 1) != 1) {
      if (json_flag == 1)
          printf("{\"error_msg\" : \"GetFullStatus1 error\",\"result\" : \"-2\"}\n");
      else
         printf("GetFullStatus1 error\n"); 
         return -1; 
      } 
     
     sleep(1);
     
    
      //RunInit command:  This Command must be executed before Operating
      buffer[0] = 0x88; 

      if (write(fd, buffer, 1) != 1) { 
      if (json_flag == 1)
          printf("{\"error_msg\" : \"RunInit error\",\"result\" : \"-3\"}\n");
      else
         printf("RunInit error\n"); 
         return -1; 
      } 


//      if (json_flag == 1)
//          printf("{\"result\" : \"Position is %i\"}\n", position);
//     else
//     printf("Position is: %i\n", position); //Print the Position
        
      
//SetPosition
buffer[0] = 0x8B;   // SetPosition Command
buffer[1] = 0xff;   // not avialable
buffer[2] = 0xff;   // not avialable 
buffer[3] = (unsigned char) (position >> 8);  // PositionByte1 (15:8)
buffer[4] = (unsigned char)  position;       // PositionByte2 (7:0)


      if (write(fd, buffer, 5) != 5) { 
      if (json_flag == 1)
          printf("{\"error_msg\" : \"SetPosition error\",\"result\" : \"-4\"}\n");
      else
         printf("SetPosition error\n"); 
         return -1; 
      } 

      if (json_flag == 1)
          printf("{\"result\" : \"0\"}\n");
      else
          printf("Step done.\n");


close(fd);
}