/*
fopen은 stdio.h에 포함된 c언어 라이브러리
open/read는 fcntl.h/unistd.h에 포함된 리눅스 시스템 라이브러리

open은 named pipe를 열 때 입/출력 모드로 열면 반대 모드로도 파일이 열릴때까지 대기하게 됨
fopen에 r옵션을 주면 안되지만 r+ 옵션을 주면 파일이 바로 열림
open에도 적용되는지 실험 필요 -> possible

리눅스와 윈도우간 통일된 소켓 라이브러리가 없음

attacher -> program
po -> pipe -> a -> opipe & stdout
 */
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// #define DEV
#ifdef DEV
  #define INP_PIPE_DIR "./ipipe"
  #define OUT_PIPE_DIR "./opipe"
#else
  #define INP_PIPE_DIR "/tmp/smdb_ipipe"
  #define OUT_PIPE_DIR "/tmp/smdb_opipe"
#endif

#define BUF_SIZE 1024

#define err(mess) {                                \
  fprintf(stderr, "[Attacher/Error] %s.\n", mess); \
  perror("");                                      \
}

typedef struct _ioStruct {
  int *isRunning;
  int inputFd;
  int stdoutFd;
  int namedPipeFd;
} ioStruct;

void printfd(int fd, char *name);
void *ioworker(void *data);

int main(int argc, char **argv) {
  if (argc == 1) {
    err("Argument is essential");
    exit(1);
  }

  
  int *isRunning = malloc(sizeof(int));
  *isRunning = 1;

  setvbuf(stdout, NULL, _IONBF, 0);
  // printfd(STDIN_FILENO, "stdin");
  // printfd(STDOUT_FILENO, "stdout");

  // using dup & pipe
  int fd[4]; // 0:input pipe, 1:output pipe, 2: stdin, 3:stdout
  // backup standard io
  // fd[2] = dup(STDIN_FILENO);
  fd[3] = dup(STDOUT_FILENO);

  // open named pipe
  if ( (fd[0] = open(INP_PIPE_DIR, O_RDWR)) == -1 ) {
    err("open INP_PIPE_DIR");
    exit(1);
  }
  if ( (fd[1] = open(OUT_PIPE_DIR, O_RDWR)) == -1 ) {
    err("open OUT_PIPE_DIR");
    exit(1);
  }

  // change standard io into pipe
  dup2(fd[0], STDIN_FILENO);
  // dup2(fd[1], STDOUT_FILENO);

  int pd[2]; // output pipe
  if (pipe(pd) == -1) {
    err("pipe1");
    exit(1);
  }
  // connect stdout to pipe input
  dup2(pd[1], STDOUT_FILENO);


  // create thread to handle io
  pthread_t ioThread;
  ioStruct *ioData = malloc(sizeof(ioStruct));
  ioData->isRunning = isRunning;
  ioData->inputFd = pd[0];
  ioData->namedPipeFd = fd[1];
  ioData->stdoutFd = fd[3];

  pthread_create(&ioThread, NULL, ioworker, (void *)ioData);


  char command[BUF_SIZE];
  memset(command, 0, sizeof(command));

  strcpy(command, "stdbuf -oL");
  for (int i = 1; i < argc; i++) {
    strcat(command, " ");
    strcat(command, argv[i]);
  }

  system(command);

  pthread_join(ioThread, NULL);

  // cleanup
  free(ioData);
  close(fd[0]);
  close(fd[1]);

  return 0;
}

void printfd(int fd, char *name) {
  struct stat st;
  if ( fstat(fd, &st) == -1 ) {
    err("fstat");
    return;
  }

  fprintf(stderr, "[Attacher/Error] fd %d name %s, ", fd, name);
  fprintf(stderr, "st_dev : %ld, ", st.st_dev);
  fprintf(stderr, "st_ino : %ld\n", st.st_ino);
}

void *ioworker(void *rawData) {
  ioStruct *data = (ioStruct*)rawData;
  int n;
  char buf[BUF_SIZE];
  memset(buf, 0, sizeof(buf));

  // FILE *inputFp = fdopen(data->inputFd, "r");
  while( *(data->isRunning) ) {

    // if ( fgets(buf, BUF_SIZE, inputFp) == NULL ) {
    //   err("read");
    //   fprintf(stderr, "[Attacher/Error] read data2\n");
    // } else {
    //   fprintf(stderr, "[Attacher/Error] read data3\n");
    //   n = strlen(buf);
    //   write(data->namedPipeFd, buf, n);
    //   write(data->stdoutFd, buf, n);
    // }

    if ( (n = read(data->inputFd, buf, BUF_SIZE)) == -1 ) {
      err("read");
    } else {
      write(data->namedPipeFd, buf, n);
      write(data->stdoutFd, buf, n);
    }
  }

  pthread_exit(NULL);
}
