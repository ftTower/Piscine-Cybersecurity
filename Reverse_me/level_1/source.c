#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(void) {

    char key[256];

    printf("Please enter key: ");
    scanf("%255s", key);
    if (strcmp(key, "__stack_check"))
        printf("Nope.\n");
    else
        printf("Good job.\n");
    return (0);
}

