#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>


#define BUF_SIZE 1024

void *ping(void *data) {
  pid_t pid = getpid();
  pthread_t tid = pthread_self();
  printf("[FakeServer] Ping thread start, pid: %d, tid: %ld\n", pid, tid);

  time_t t;
  struct tm *td;
  int *is_running = (int*)data;

  while (*is_running) {
    time(&t);
    td = localtime(&t);
    printf("[FakeServer] [%d:%d:%d] ping\n", td->tm_hour, td->tm_min, td->tm_sec);
    fflush(stdout);
    sleep(1);
  }

  pthread_exit(NULL);
}

void *communicate(void *data) {
  pid_t pid = getpid();
  pthread_t tid = pthread_self();
  printf("[FakeServer] Communicate thread start, pid: %d, tid: %ld\n", pid, tid);

  char buf[BUF_SIZE];
  int *is_running = (int*)data;

  while (fgets(buf, BUF_SIZE, stdin) != NULL) {
    if (strcmp(buf, "quit\n") == 0) {
      printf("[FakeServer] quit program\n");
      *is_running = 0;
      break;
    }

    fprintf(stderr, "[FakeServer/Error] recive %s", buf);
    printf("[FakeServer] recive %s", buf);

    memset(buf, '\0', BUF_SIZE);
  }

  pthread_exit(NULL);
}

int main() {
  pthread_t pingThread, commThread;
  pthread_attr_t attr;
  int thread_id;
  int *is_running = malloc(sizeof(int));
  *is_running = 1;

  fprintf(stderr, "[FakeServer/Error] start fake server\n");
  printf("[FakeServer] start fake server\n");

  pthread_attr_init(&attr);
  pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
  // pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

  pthread_create(&pingThread, &attr, ping, is_running);
  pthread_create(&commThread, &attr, communicate, is_running);

  pthread_join(commThread, NULL);
  pthread_join(pingThread, NULL);
  
  pthread_attr_destroy(&attr);
  return 0;
}