#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

#define TRUE 1
typedef int buffer_item;
#define BUFFER_SIZE 5
buffer_item buffer[BUFFER_SIZE];

pthread_mutex_t mutex;
sem_t empty;
sem_t full;

int insert_Pointer = 0, remove_Pointer = 0;

void *producer(void *param);
void *consumer(void *param);

int insert_item(buffer_item item)
{
    int output = 0;   
	sem_wait(&empty);/*empty*/
	pthread_mutex_lock(&mutex);/*lock*/
	
	if (insert_Pointer < BUFFER_SIZE) {
	   buffer[insert_Pointer++] = item;
	   insert_Pointer = insert_Pointer % 5;
	} else {
       output = -1;
	}
	
	pthread_mutex_unlock(&mutex);/*unlock*/
    sem_post(&full);/*fill*/

	return output;	
}

int remove_item(buffer_item *item)
{
	int output = 0;
	sem_wait(&full);/*full*/
	pthread_mutex_lock(&mutex);/*lock*/
	
	if (insert_Pointer > 0) {
	   *item = buffer[remove_Pointer];/*remove*/
	   buffer[remove_Pointer++] = -1;/*subpointer*/
	   remove_Pointer = remove_Pointer % 5;
    } else {
        output = -1;
    }
	pthread_mutex_unlock(&mutex);/*unlock*/
	sem_post(&empty);/*empty*/

	return output;	
}


int main(int argc, char *argv[])
{
	/*step1*/
	int sleepTime = atoi(argv[1]);
	int producer_Threads = atoi(argv[2]);
	int consumer_Threads = atoi(argv[3]);

	/* Initialize buffer */
    pthread_mutex_init(&mutex, NULL);
    /*flag = 0*/
	sem_init(&empty, 0, 5);/*5 empty*/
	sem_init(&full, 0, 0);/*0 full*/

	/* producer and consumer*/
	for(int i = 0; i < producer_Threads; i++)
	{
		pthread_t tid;
		pthread_attr_t attr;
		pthread_attr_init(&attr);
		pthread_create(&tid, &attr, producer, NULL);
	}

	for(int j = 0; j < consumer_Threads; j++)
	{
		pthread_t tid;
		pthread_attr_t attr;
		pthread_attr_init(&attr);
		pthread_create(&tid, &attr, consumer, NULL);
	}

	/* Sleep */
	sleep(sleepTime);
	return 0;
}

void *producer(void *param)
{
	buffer_item item;
	int rt;
	while(TRUE)
	{
		rt = rand() % 5;/*sleep*/
		sleep(rt);
		item = rand();
		if(insert_item(item)){
			fprintf(stderr, "Report Error");
        } else {
            printf("Producer produced %d \n", item);
        }
	 }

}

void *consumer(void *param)
{
	buffer_item item;
	int rt;
	while(TRUE)
	{
		rt = rand() % 5;
		sleep(rt);

		if(remove_item(&item)){
			fprintf(stderr, "Report Error");
		} else {
			printf("Consumer consumed %d \n", item);
		}
	}
}
