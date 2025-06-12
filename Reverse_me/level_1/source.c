#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(void) {

    const char comp[] = "__stack_check";
    char key[256];

    printf("Please enter key: ");
    scanf("%255s", key);
    if (strcmp(key, comp))
        printf("Nope.\n");
    else
        printf("Good job.\n");
    return (0);
}

