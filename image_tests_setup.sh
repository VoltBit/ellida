DIR="/home/smith/projects/poky"
TARGET_BUILD="/home/smith/projects/poky/build/"
TAPDEV_COUNT="2"

# cd $DIR/scripts/
sudo $DIR/runqemu-gen-tapdevs 1000 1000 $TAPDEV_COUNT $TARGET_BUILD/tmp/sysroots-components/x86_64/qemu-helper-native
