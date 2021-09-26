#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 512
#define INP_PIPE_DIR "./ipipe"
#define OUT_PIPE_DIR "./opipe"

#define err(mess) { fprintf(stderr,"Error: %s.\n", mess); exit(1); }

int main(int argc, char **argv) {
  char buf[BUF_SIZE];
  int fd, n;
  char *path = INP_PIPE_DIR;
  if (argc == 2 && strcmp(argv[0], "o")) {
    path = OUT_PIPE_DIR;
  }
  printf("path is %s\n", path);

  // unlink(path);
  printf("%d\n", mkfifo(path, 0666));

  if ( (fd = open(path, O_WRONLY)) < 0)
    err("open")
  printf("open %s\n", path);

  while( (n = read(STDIN_FILENO, buf, BUF_SIZE) ) > 0) {
    if ( write(fd, buf, n) != n) { 
      err("write")
    }
  }
  
  write(STDOUT_FILENO, "terminate\n", 10);
  close(fd);

  // FILE* fp;
  // int n;
  // if ( (fp = fopen("fifo_x", "r+")) == NULL)
  //   err("open")

  // while( feof(stdin) == 0 ) {
  //   if ( fgets(buf, BUF_SIZE, stdin) == NULL)
  //     err("read")

  //   // printf("%s", buf);
  //   fprintf(fp, "%s", buf);
  //   fflush(fp);
  //   // if ( fprintf(fp, "%s", buf) != n)
  //   //   err("write")
  // }
  // fclose(fp);

  return 0;
}