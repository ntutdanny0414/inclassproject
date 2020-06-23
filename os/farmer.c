#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <pthread.h>
#include <strings.h>
#include <semaphore.h>

#define MAX_WAIT 3 // how many seconds each car will wait at most

typedef struct FARMER {
    pthread_t t;
    int isNorth;
    int idx;//ID
    int waitfor;//time
} FARMER;

sem_t sem; // bridge


void enter_bridge(char* direction, int idx) {
     printf("1 %s Farmers %d enter\n", direction, idx);
     sem_wait(&sem);
     printf("2 %s Farmers %d has entered\n", direction, idx);
}

void exit_bridge(char* direction, int idx) {
     printf("5 %s Farmers %d left\n", direction, idx);
     sem_post(&sem);
}

void* pass_bridge(void* param) {
     FARMER* f = (FARMER*) param;
     char* direction = f->isNorth ? "North" : "South";

     enter_bridge(direction, f->idx);
     printf("3 %s Farmers %d take %d seconds\n", direction, f->idx, f->waitfor);
     sleep(f->waitfor);
     printf("4 %s Farmers %d has passed\n", direction, f->idx);

     exit_bridge(direction, f->idx);
}

int main(int argc, char *argv[]) {
     int i;
     FARMER* f_north;
     FARMER* f_south;

     int nNorthFarmers, nSouthFarmers;

     nNorthFarmers = atoi(argv[1]);
     nSouthFarmers = atoi(argv[2]);

     f_north = (FARMER*)malloc(sizeof(FARMER) * nNorthFarmers);
     f_south = (FARMER*)malloc(sizeof(FARMER) * nSouthFarmers);

     sem_init(&sem, 0, 1);

     for (i = 0; i < nNorthFarmers; ++i) {
        f_north[i].isNorth = 1;
        f_north[i].idx = i;
        f_north[i].waitfor = rand() % MAX_WAIT;
        pthread_create(&(f_north[i].t), 0, pass_bridge, &(f_north[i]));
     }

     for (i = 0; i < nSouthFarmers; ++i) {
        f_south[i].isNorth = 0;
        f_south[i].idx = i;
        f_south[i].waitfor = rand() % MAX_WAIT;
        pthread_create(&(f_south[i].t), 0, pass_bridge, &(f_south[i]));
     }

     for (i = 0; i < nNorthFarmers; ++i) {
        pthread_join(f_north[i].t, NULL);
     }

     for (i = 0; i < nSouthFarmers; i++) {
        pthread_join(f_south[i].t, NULL);
     }

     sem_destroy(&sem);
    
     free(f_north);
     free(f_south);

     return 0;
}
