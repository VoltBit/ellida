
sudo /home/smith/projects/poky/scripts/runqemu-gen-tapdevs 1000 1000 1 /home/smith/projects/poky/build/tmp/sysroots/x86_64-linux
grep -q -F 'INHERIT += "testimage"' /home/smith/projects/poky/build/conf/local.conf || (echo '' >> /home/smith/projects/poky/build/conf/local.conf && echo 'INHERIT += "testimage"' >> /home/smith/projects/poky/build/conf/local.conf)
if grep -q -F 'TEST_SUITES' /home/smith/projects/poky/build/conf/local.conf
then
    sed -i 's/.*TEST_SUITES.*/TEST_SUITES = "dummy2 dummy1"/' /home/smith/projects/poky/build/conf/local.conf
else
    echo 'TEST_SUITES = "dummy2 dummy1"' >> /home/smith/projects/poky/build/conf/local.conf
fi
