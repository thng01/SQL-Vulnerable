#include <unistd.h>
void main(){
	setreuid(1009,1009);
	setregid(1009,1009);
	system("more /home/queen/msg");
}
