#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <errno.h>


volatile int running_threads = 0;
pthread_t thread[3];
int num;
struct Results{
	int min;
	int max;
	int average;
}Results;
void *findMin(void *array){
	int *data = (int*)array; 
	Results.min = data[0]; 
	for(int i = 0; i < num; i++){
		if(data[i] < Results.min){
			Results.min = data[i];
		}
    }  
	running_threads -= 1;
}
void *findMax(void *array){
	int *data = (int*)array;
	for(int i = 0; i < num; i++){
		if(data[i] > Results.max){
			Results.max = data[i];
		}
	}
	running_threads -= 1;
}
void *findAve(void *array){
	int *data = (int*)array;
	for(int i = 0; i < num; i++){
		Results.average += data[i];
	}
	Results.average = Results.average/num;
	running_threads -= 1;
}
void joinThreads(int numThreads){
	int s;
	while(numThreads >= 0){
		s = pthread_join(thread[numThreads], NULL);
		 numThreads--;
	}
}
void createThreads(int *array){	
	int s;
    s = pthread_create(&thread[0], NULL, findMin, (void *)array);
	running_threads += 1;
    s = pthread_create(&thread[1], NULL, findMax, (void *)array);
    running_threads += 1;
    s = pthread_create(&thread[2], NULL, findAve, (void *)array);	 
    running_threads += 1;
}
int main(){
    num = 7;
	int *array = malloc(num * sizeof(int));
	array[0] = 90;
	array[1] = 81;
	array[2] = 78;
	array[3] = 95;
	array[4] = 79;
	array[5] = 72;
	array[6] = 85;
    createThreads(array);
	joinThreads(2);
    printf("\nThe average is %d\nThe minimum is %d\nThe maximum is %d\n",Results.average, Results.min, Results.max);

	return(0);

}
