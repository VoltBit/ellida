#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <pwd.h>
#include <unistd.h>

int main()
{
        // rulat ca root, "getuid()" chiar intoarce 0
    if (getpwuid(getuid()) == NULL) {
        printf("errno: %s\n", strerror(errno));
        return 1;
    }

    uid_t id = 0;
    struct passwd *pwd;
    pwd = getpwuid(id);
    printf("name: %s\ndir: %s\n", pwd->pw_name, pwd->pw_dir);
    return 0;
}
