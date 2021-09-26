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
  #define INP_PIPE_DIR "/home/smdb/ipipe"
  #define OUT_PIPE_DIR "/home/smdb/opipe"
#endif

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
  char buf[BUF_SIZE];
  int fd, n;

  if (argc != 2) {
    err("Argment is incorrect");
  } else if (strcmp(argv[1], "i") == 0) {
    fd = open_pipe(INP_PIPE_DIR);
  } else if (strcmp(argv[1], "o") == 0) {
    fd = open_pipe(OUT_PIPE_DIR);
  } else if (strcmp(argv[1], "s") == 0) {
    fd = STDIN_FILENO;

    while (fgets(buf, BUF_SIZE, stdin) != NULL) {
      printf("[Reader] recive message: %s", buf);
      memset(buf, '\0', n);
    }

    printf("[Reader] terminate\n");
    close(fd);

    return 0;
  }

  while ( (n = read(fd, buf, BUF_SIZE) ) > 0 ) {
    if ( write(STDOUT_FILENO, buf, n) != n) {
      perror("write");
    }
    memset(buf, '\0', n);
  }

  printf("[reader] terminate\n");
  close(fd);

  return 0;
}