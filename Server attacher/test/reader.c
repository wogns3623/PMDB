#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

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

  if ( (fd = open(path, O_RDONLY)) < 0)
    err("open")
  printf("open %s\n", path);

  while( (n = read(fd, buf, BUF_SIZE) ) > 0 ) {
    if ( write(STDOUT_FILENO, buf, n) != n) { 
      err("write")
    }
  }

  write(STDOUT_FILENO, "terminate\n", 10);
  close(fd);
  
  // FILE *fp;
  // size_t n;
  // if ( (fp = fopen("fifo_x", "rb")) == NULL )
  //   err("open")
  
  // while ( feof(fp) == 0 ) {
  //   if (fgets(buf, BUF_SIZE, fp) == NULL) {
  //     fprintf(stderr,"Error: %s.\n", "read");
  //   } else {
  //     printf("%s", buf);
  //   }
  // }

  // fclose(fp);

  return 0;
}