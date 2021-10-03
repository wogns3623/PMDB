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

#define err(mess) {                              \
  fprintf(stderr, "[Writer/Error] %s.\n", mess); \
  exit(1);                                       \
}

int open_pipe(char *path) {
  int fd;
  if ( (fd = open(path, O_RDWR)) < 0) {
    printf("[Writer] pipe \"%s\" not found, create new one.\n", path);
    printf("[Writer] pipe mkfifo status: %d\n", mkfifo(path, 0666));
    fd = open(path, O_RDWR);
  }
  printf("[Writer] open pipe \"%s\"\n", path);

  return fd;
}


int main(int argc, char **argv) {
  int fd, n;
  char buf[BUF_SIZE];
  memset(buf, 0, BUF_SIZE);

  if (argc != 2) {
    err("Argment is incorrect");
  } else if (strcmp(argv[1], "i") == 0) {
    fd = open_pipe(INP_PIPE_DIR);
  } else if (strcmp(argv[1], "o") == 0) {
    fd = open_pipe(OUT_PIPE_DIR);
  } else if (strcmp(argv[1], "s") == 0) {
    fd = STDOUT_FILENO;
  }

  while( (n = read(STDIN_FILENO, buf, BUF_SIZE) ) >= 0) {
    int d;
    if ( (d=write(fd, buf, n)) != n) { 
      err("write");
    }
  }
  
  printf("[Writer] terminate\n");
  close(fd);

  return 0;
}