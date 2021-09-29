/*
fopen은 stdio.h에 포함된 c언어 라이브러리
open/read는 fcntl.h/unistd.h에 포함된 리눅스 시스템 라이브러리

open은 named pipe를 열 때 입/출력 모드로 열면 반대 모드로도 파일이 열릴때까지 대기하게 됨
fopen에 r옵션을 주면 안되지만 r+ 옵션을 주면 파일이 바로 열림
open에도 적용되는지 실험 필요 -> possible


리눅스와 윈도우간 통일된 소켓 라이브러리가 없음
 */
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

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
  exit(1);                                         \
}

// 인자로 원하는 프로그램 실행 명령어를 작성
int main(int argc, char **argv) {
  char buf[BUF_SIZE];
  FILE *fp[3]; // 0: input, 1:output 2:error
  // using freopen instead dup2
  // or using popen?
  // this can use stdout 
  fp[0] = freopen(INP_PIPE_DIR, "r", stdin);
  fp[1] = freopen(OUT_PIPE_DIR, "w", stdout);
  // fp[2] = freopen(OUT_PIPE_DIR, "w", stderr);
  // 엥 이러면 출력을 무조건 reader를 통해서 봐야하네?
  // 출력이 동시에 나오게 만들수는 없나?
  // stdout을 읽어서 프린트

  if (argc == 1)
    err("Argument is essential");

  strcpy(buf, argv[1]);
  for (int i = 2; i < argc; i++)
  {
    strcat(buf, " ");
    strcat(buf, argv[i]);
  }
  system(buf);

  fclose(fp[0]);
  fclose(fp[1]);
  return 0;
}