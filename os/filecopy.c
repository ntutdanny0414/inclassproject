#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>

int main(int argc, char *argv[]){
    int read_write[2];
	int Size;
	pid_t pid;

    char text[1024];
	char copy[1024];  

    char* source = argv[1];
    char* dest = argv[2];

    pipe(read_write);
    if (pipe(read_write)== -1){ 
        fprintf(stderr, "Pipe Failed" ); 
        return 1; 
    }  

    pid = fork();
    
    if (pid < 0) { 
        fprintf(stderr, "Fork Failed" ); 
        return 1; 
    } else if (pid > 0) {
	    int sourceNum;
	    ssize_t numBytes; 
        close(read_write[0]);
        sourceNum=open(source, O_RDONLY);
        numBytes=read(sourceNum, text, sizeof(text));
        write(read_write[1],text, numBytes);
        close(read_write[1]);
    } else if (pid == 0){	
    	int destN;
    	ssize_t numBytesChar;
        close(read_write[1]);
        numBytesChar =read(read_write[0], copy, sizeof(copy));
        close(read_write[0]);
        destN=open(dest, O_CREAT | O_WRONLY);
        write(destN, copy, numBytesChar);
    }

    return 0;
}
