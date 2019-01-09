// gcc HW1b.c -o HW1b -fno-stack-protector -m32
#include <stdio.h>

void secretFunction()
{
    printf("Congratulations!\n");
    printf("You have entered in the secret function!\n");
}

void echo()
{
    char buffer[20];

    printf("Get to the secret function:%p\n", &secretFunction);
    scanf("%19s", buffer); //Reads in only up to 19 characters now
    printf("You entered: %s\n", buffer);    
}

int main()
{
    echo();

    return 0;
}

