# Profilers

## Lynis - security audit
[Documentation](https://cisofy.com/documentation/lynis/configuration/#lynis-profiles)

Can be controled through .prf files, example: [default.prf](https://github.com/CISOfy/lynis/blob/master/default.prf)

---

## LTP - general collection of tests
[website](http://linux-test-project.github.io/)
[Documentation](http://ltp.sourceforge.net/documentation/how-to/ltp.php#_3.4)

Controlled via control file:
#Tag       Test case
#---------------------------------------
mtest01     mtest01 -p 10
mmstress    mmstress -x 100
fork01      fork01
chdir01     symlink01 -T chdir01
#----------------------------------------

```
./runltp -p -l result.02.log -f my_command_file
```

---

## LTTng - tracing tool

Requires a complex configuration where instrumentation points are inserted in the software via included libraries. Tracked events can be configured via commands:

[Documentation](http://lttng.org/docs/v2.9/#doc-controlling-tracing)

---

## Phoronix - Linux benchamrking

[Website](https://www.phoronix-test-suite.com/)
[Documentation](http://www.phoronix-test-suite.com/documentation/phoronix-test-suite.pdf)
Uses [openbenchmarking.org](http://openbenchmarking.org/)
