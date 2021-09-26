/*
fopen은 stdio.h에 포함된 c언어 라이브러리
open/read는 fcntl.h/unistd.h에 포함된 리눅스 시스템 라이브러리

open은 named pipe를 열 때 입/출력 모드로 열면 반대 모드로도 파일이 열릴때까지 대기하게 됨
fopen에 r옵션을 주면 안되지만 r+ 옵션을 주면 파일이 바로 열림
TODO: open에도 적용되는지 실험 필요


리눅스와 윈도우간 통일된 소켓 라이브러리가 없음
 */
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define DEV
#ifdef DEV
#define INP_PIPE_DIR "./ipipe"
#define OUT_PIPE_DIR "./opipe"
#else
#define INP_PIPE_DIR "/tmp/smdb/ipipe"
#define OUT_PIPE_DIR "/tmp/smdb/opipe"
#endif

#define BUF_SIZE 1024

#define err(mess)                          \
  {                                        \
    fprintf(stderr, "Error: %s.\n", mess); \
    exit(1);                               \
  }

FILE *open_pipe(char *path);
void close_conn(FILE **fp);

// 인자로 원하는 프로그램 실행 명령어를 작성
int main(int argc, char **argv)
{

  FILE *fp[2]; // 0: input, 1:output
  fp[0] = open_pipe(INP_PIPE_DIR);
  fp[1] = open_pipe(OUT_PIPE_DIR);

  dup2(fileno(fp[0]), STDIN_FILENO);
  dup2(fileno(fp[1]), STDOUT_FILENO);

  // TODO: 쓰레드를 나누던 프로세스를 분기하던 입력 루프와 출력 루프를 나누기
  // TODO: 기본 입출력 fd를 바꾸었을 때 system() 등으로 실행시킨 프로그램에도 적용되는지 확인
  char buf[BUF_SIZE];
  while (feof(stdin) == 0)
  {
    printf("tick\n");
    if (fgets(buf, BUF_SIZE, stdin) == NULL)
    {
      fprintf(stderr, "Error: %s.\n", "read");
    }
    else
    {
      fprintf(stdout, "He said: %s\n", buf);
    }
  }
  // if (argc > 1) {

  //   exec(argv[1], argv++);
  // }

  fclose(fp[0]);
  fclose(fp[1]);
  return 0;
}

FILE *open_pipe(char *path)
{
  FILE *fp;

  if ((fp = fopen(path, "r+")) == NULL)
  {
    fprintf(stdout, "[attacher]: pipe \"%s\" not found, create new one.\n", path);
    printf("output pipe mkfifo status:%d\n", mkfifo(path, 0666)); //make pipe
    fp = fopen(path, "r+");
  }

  return fp;
}