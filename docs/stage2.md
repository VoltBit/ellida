[Parsable CGL specs](https://wiki.linuxfoundation.org/en/Carrier_Grade_Linux/CGL_Requirements)

Keywords and technologies:

systemtap, LTTng

### Possible features and extensibility requirements

[LTTng Docs](http://lttng.org/docs/v2.9/#doc-what-is-tracing)
![LTTng architectrue](https://static.lwn.net/images/2012/lttng-overview.png)

The Database will have an internal organisation simillar to to a filesystem:
+ A "superblock" JSON file which delcares the supported specifications în the root directory
+ Each subfolder is an organisation element like Layer of Objective
+ Each JSON file is simmilar to an inoode containing metadata and the actual path to th test


Links
[How to add a recipe](https://wiki.yoctoproject.org/wiki/How_do_I#Q:_How_do_I_put_my_recipe_into_Yocto.3F)

[^2](http://stevephillips.me/blog/adding-custom-software-to-bitbake-oe-core)

[^3](https://lists.yoctoproject.org/pipermail/yocto/2015-September/026696.html)

[?] How to I map a test to a JSON file

TODOs:

Each test might need additional files such as C/C++ source files and makefiles. The framework must account for them somehow.


