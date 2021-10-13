#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define TEST_INP_PIPE_DIR "/tmp/tip"
#define TEST_OUT_PIPE_DIR "/tmp/top"
#define INP_PIPE_DIR "/tmp/pmdb_ipipe"
#define OUT_PIPE_DIR "/tmp/pmdb_opipe"
#define BUF_SIZE 1024

#define err(mess) {                              \
  fprintf(stderr, "[Reader/Error] %s.\n", mess); \
  exit(1);                                       \
}

int open_pipe(char *path) {
  int fd;
  if ( (fd = open(path, O_RDWR)) < 0) {
    printf("[Reader] pipe \"%s\" not found, create new one.\n", path);
    printf("[Reader] pipe mkfifo status: %d\n", mkfifo(path, 0666));
    fd = open(path, O_RDWR);
  }
  printf("[Reader] open pipe \"%s\"\n", path);

  return fd;
}


int main(int argc, char **argv) {
  int fd, n;
  char buf[BUF_SIZE];
  memset(buf, 0, BUF_SIZE);

  if (argc < 2) {
    err("Argment is incorrect");
  }

  switch (argv[1][0]) {
    case 'i':
      if (argc == 3 && argv[2][0] == 'd') {
        fd = open_pipe(TEST_INP_PIPE_DIR);
      } else {
        fd = open_pipe(INP_PIPE_DIR);
      }
      break;

    case 'o':
      if (argc == 3 && argv[2][0] == 'd') {
        fd = open_pipe(TEST_OUT_PIPE_DIR);
      } else {
        fd = open_pipe(OUT_PIPE_DIR);
      }
      break;

    case 's':
      fd = STDIN_FILENO;
      break;
  }

  while ( (n = read(fd, buf, BUF_SIZE) ) > 0 ) {
    if ( write(STDOUT_FILENO, buf, n) != n) {
      perror("write");
    }
  }

  printf("[reader] terminate\n");
  close(fd);

  return 0;
}