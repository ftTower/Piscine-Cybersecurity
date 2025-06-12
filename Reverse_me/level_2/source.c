#include <unistd.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

void ok()
{
    puts("Good job.");
    return;
}

void no()
{
    puts("Nope.");
    return;
}

int main(void)
{
    int scanf_ret = 0;
    int index_1 = 0; //! movl   $0x0,-0x8(%ebp)
    int index_2 = 0;
    char buffer_1[9];  //!
    char buffer_2[24]; //! mov    %ebx,-0x40(%ebp)
    char buffer_3[4];  //!

    bool bool_1;
    size_t var_1;

    printf("Please enter key: "); //! call   0x1060 <printf@plt>

    scanf_ret = scanf("%23s", buffer_2); //! call   0x10c0 <__isoc99_scanf@plt>

    if (scanf_ret != 1) //! cmp    -0xc(%ebp),%eax
        no();
    if (buffer_2[1] != '0') //! cmp    %ecx,%eax
        no();
    if (buffer_2[0] != '0') //! cmp    %ecx,%eax
        no();
    fflush(0); //! call   0x1070 <fflush@plt>

    memset(buffer_1, 0, 9); //!call   0x10b0 <memset@plt>
    buffer_1[0] = 'd'; //!movb   $0x64,-0x1d(%ebp)
    buffer_3[3] = '\0'; //! movb   $0x0,-0x36(%ebp)
    index_2 = 2; //! movl   $0x2,-0x14(%ebp)
    index_1 = 1; //! movl   $0x1,-0x10(%ebp)
    while   (true)
    {
        bool_1 = false;
        if (strlen(buffer_1) < 8) // !call   0x10a0 <strlen@plt> && cmp    $0x8,%ecx
        {
            var_1 = index_2; //!mov    %al,-0x41(%ebp)
            bool_1 = var_1 < strlen(buffer_2); //!call   0x10a0 <strlen@plt> && cmp    %ecx,%eax
        }
        if (!bool_1) //! test   $0x1,%al
            break;
        buffer_3[0] = buffer_2[index_2]; //! mov    %al,-0x39(%ebp)
        buffer_3[1] = buffer_2[index_2 + 1]; //! mov    %al,-0x38(%ebp)
        buffer_3[2] = buffer_2[index_2 + 2]; //! %al,-0x37(%ebp)
        buffer_1[index_1] = atoi(buffer_3); //! call   0x10d0 <atoi@plt>
        index_2 += 3; //! add    $0x3,%eax
        index_1++; //! add    $0x1,%eax
    } //!jmp    0x13ad <main+221>
    buffer_1[index_1] = '\0'; //!movb   $0x0,-0x1d(%ebp,%eax,1)

    if (!strcmp(buffer_1, "delabere")) //! call   0x1040 <strcmp@plt>
        ok(); //! call   0x12a0 <ok>
    else
        no(); //! call   0x1220 <no>
    return (0);
}