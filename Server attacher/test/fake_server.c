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
  time_t t;
  struct tm *td;

  printf("[FakeServer] Ping thread start, pid: %d, tid: %d\n", pid, tid);

  for(int i=0; i<10; i++) {
    time(&t);
    timeData = localtime(&t);
    printf("[FakeServer] [%s:%s:%s] ping\n", td->tm_hour, td->tm_min, td->tm_sec);
    fflush(stdout);
    sleep(1);
  }

  pthread_exit(NULL);
}

void *communicate(void *data) {
  char buf[BUF_SIZE];

  while (fgets(buf, BUF_SIZE, stdin) != NULL) {
    if (strcmp(buf, "quit")) break;

    fprintf(stderr, "[FakeServer/Error] recive %s", buf);
    printf("[FakeServer] recive %s\n", buf);
    fflush(stdout);

    memset(buf, '\0', BUF_SIZE);
  }

  pthread_exit(NULL);
}

int main() {
  pthread_t pingThread, commThread;
  pthread_attr_t attr;
  int thread_id

  fprintf(stderr, "[FakeServer/Error] start fake server");
  // need to configure buffer size or not to use buffer
  printf("[FakeServer] start fake server\n");
  fflush(stdout); //printf has buffer. need to fflush

  pthread_attr_init(&attr);
  pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

  pthread_create(&pingThread, &attr, ping, NULL);
  pthread_create(&commThread, &attr, communicate, NULL);

  pthread_attr_destroy(&attr);
  
  return 0;
}