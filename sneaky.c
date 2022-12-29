#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/mount.h>

int main(void)
{
  int mounting;
  char buffer[32];
  printf("Device to mount to /mnt: ");
  gets(buffer);
  mounting = mount(buffer, "/mnt", "vfat", MS_MGC_VAL, " ");
  if (mounting != 0)
    printf("ERROR: Unable to mount\n");
}
