#include <stdio.h>

#define BUF_SIZE 1024

char buf[BUF_SIZE];

int main() {
  setbuf(stdout, NULL);
  printf("[server] start fake server\n"); //printf has buffer. need to fflush
  // fflush(stdout);
  // need to configure buffer size or not to use buffer
  perror("[server stderr] start fake server");
  for (int i=0; i<10; i++) {
    fgets(buf, BUF_SIZE, stdin);
    fprintf(stderr, "[server stderr] recive %s", buf);
    printf("[server] %s\n", buf);
    // fflush(stdout);
  }
  return 0;
}