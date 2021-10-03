#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>


#define BUF_SIZE 1024


void *pingworker(void *data);
void *ioworker(void *data);

int main() {
  pthread_t pingThread, ioThread;
  pthread_attr_t attr;
  int thread_id;
  int *isRunning = malloc(sizeof(int));
  *isRunning = 1;

  fprintf(stderr, "[FakeServer/Error] start fake server\n");
  fprintf(stderr, "[FakeServer/Error] stdin is \t%p\n", stdin);
  fprintf(stderr, "[FakeServer/Error] stdout is \t%p\n", stdout);
  printf("[FakeServer] start fake server\n");

  pthread_attr_init(&attr);
  pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
  // pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);

  pthread_create(&pingThread, &attr, pingworker, isRunning);
  pthread_create(&ioThread, &attr, ioworker, isRunning);

  pthread_join(ioThread, NULL);
  pthread_join(pingThread, NULL);
  
  pthread_attr_destroy(&attr);
  return 0;
}

void *pingworker(void *data) {
  pid_t pid = getpid();
  pthread_t tid = pthread_self();
  printf("[FakeServer] Ping thread start, pid: %d, tid: %ld\n", pid, tid);

  time_t t;
  struct tm *td;
  int *isRunning = (int*)data;

  while (*isRunning) {
    time(&t);
    td = localtime(&t);
    printf("[FakeServer] [%d:%d:%d] ping\n", td->tm_hour, td->tm_min, td->tm_sec);
    // fflush(stdout);
    sleep(1);
  }

  pthread_exit(NULL);
}

void *ioworker(void *data) {
  pid_t pid = getpid();
  pthread_t tid = pthread_self();
  printf("[FakeServer] Communicate thread start, pid: %d, tid: %ld\n", pid, tid);

  char buf[BUF_SIZE];
  memset(buf, 0, BUF_SIZE);
  int *isRunning = (int*)data;

  while (fgets(buf, BUF_SIZE, stdin) != NULL) {
    if (strcmp(buf, "quit\n") == 0) {
      printf("[FakeServer] quit program\n");
      *isRunning = 0;
      break;
    }
    printf("[FakeServer] recive %s", buf);
  }

  pthread_exit(NULL);
}