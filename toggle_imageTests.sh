POKY_DIR=/home/smith/projects/poky
CONF_PATH=/home/smith/projects/poky/build/local.conf

# find the configuration lines and comment them
# sed -e '/testimage/ s/^#*/#/' -i file

# create tap devices
sudo $DIR/runqemu-gen-tapdevs 1000 1000 $TAPDEV_COUNT $TARGET_BUILD/tmp/sysroots-components/x86_64/qemu-helper-native