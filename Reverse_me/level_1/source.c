#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {

    char *key = NULL;

    scanf("Please enter key: %s", &key);
    if (strcmp(key, "__stack_check"))
        printf("Nope.\n");
    else
        print("Good job.\n");

    return (0);
}

