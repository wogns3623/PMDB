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

void printfd(int fd, char *name) {
  struct stat st;
  if ( fstat(fd, &st) == -1 ) {
    perror("");
    err("fstat");
  }

  fprintf(stderr, "[Attacher/Error] information about the file descriptor %d name %s\n", fd, name);
  fprintf(stderr, "st_dev : %ld, ", st.st_dev);
  fprintf(stderr, "st_ino : %ld\n", st.st_ino);
  // fprintf(stderr, "st_mode : \t\t%p", st.st_mode);
  // fprintf(stderr, "st_nlink : \t\t%p", st.st_nlink);
  // fprintf(stderr, "st_uid : \t\t%p", st.st_uid);
  // fprintf(stderr, "st_gid : \t\t%p", st.st_gid);
  // fprintf(stderr, "st_rdev : \t\t%p", st.st_rdev);
  // fprintf(stderr, "st_size : \t\t%p", st.st_size);
}

// 인자로 원하는 프로그램 실행 명령어를 작성
// https://www.ibm.com/docs/en/zos/2.2.0?topic=redirection-using-global-standard-streams
// 스트림 변경 사항이 어디까지 영향을 미치는지
int main(int argc, char **argv) {
  char buf[BUF_SIZE];
  printfd(STDIN_FILENO, "stdin");
  printfd(STDOUT_FILENO, "stdout");

  // using freopen instead dup2
  // or using popen?
  // this can use stdout?

  // using freopen
  // can't use initial stdin/out
  // FILE *fp[3]; // 0:input, 1:output, 2:error
  // fp[0] = freopen(INP_PIPE_DIR, "r", stdin);
  // fp[1] = freopen(OUT_PIPE_DIR, "w", stdout);
  // fp[2] = freopen(OUT_PIPE_DIR, "w", stderr);
  // 엥 이러면 출력을 무조건 reader를 통해서 봐야하네?
  // 출력이 동시에 나오게 만들수는 없나?
  // stdout을 읽어서 프린트
  // 프로그램 내부에서 stdin에 쓸 수 있나?


  // using fopen and direct assignment
  // FILE *fp[4]; // 0:input pipe, 1:output pipe, 2:stdin, 3:stdout
  // fp[2] = stdin;
  // if ( (fp[0] = fopen(INP_PIPE_DIR, "r")) == NULL ) {
  //   err("Cannot open ipipe");
  // } else {
  //   stdin = fp[0];
  // }

  // fp[3] = stdout;
  // if ( (fp[1] = fopen(OUT_PIPE_DIR, "r+")) == NULL ) {
  //   err("Cannot open opipe");
  // } else {
  //   stdout = fp[1];
  // }

  //using dup
  int fd[4]; // 0:input pipe, 1:output pipe, 2: stdin, 3:stdout
  //backup standard io
  fd[2] = dup(STDIN_FILENO);
  fd[3] = dup(STDOUT_FILENO);
  
  //open pipe
  if ( (fd[0] = open(INP_PIPE_DIR, O_RDWR)) == -1 ) {
    perror("");
    err("open");
  }
  if ( (fd[1] = open(OUT_PIPE_DIR, O_RDWR)) == -1 ) {
    perror("");
    err("open");
  }

  // change standard io into pipe
  dup2(fd[0], STDIN_FILENO);
  dup2(fd[1], STDOUT_FILENO);

  printfd(fd[2], "fd[2]");
  printfd(fd[3], "fd[3]");
  printfd(STDIN_FILENO, "stdin");
  printfd(STDOUT_FILENO, "stdout");
  printfd(fd[0], "fd[0]");
  printfd(fd[1], "fd[1]");

  if (argc == 1)
    err("Argument is essential");

  strcpy(buf, argv[1]);
  for (int i = 2; i < argc; i++)
  {
    strcat(buf, " ");
    strcat(buf, argv[i]);
  }
  system(buf);

  // fclose(fp[0]);
  // fclose(fp[1]);
  close(fd[0]);
  close(fd[1]);

  return 0;
}