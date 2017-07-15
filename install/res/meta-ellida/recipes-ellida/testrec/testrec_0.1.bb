BB_STRICT_CHECKSUM = "0"
SUMMARY = "Simple helloworld application"
SECTION = "examples"
LICENSE = "MIT"

SRC_URI = "git://git@github.com/voltbit/ellida.git;branch=master;protocol=ssh"
SRCREV = "master"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

S="${WORKDIR}/git"

do_compile() {
    true
}

do_compile() {
    # make
}

do_install() {
	# install -d ${D}${bindir}
    # install -m 0744 dummy_server ${D}${bindir}
}

python do_ellidatest() {
    import sys
    sys.path.append("/home/smith/projects/ellida/engine")
    sys.path.append("/home/smith/projects/ellida/manager")
    from ellida_engine import EllidaEngine
    from ellida_manager import EllidaManager

    engine = EllidaEngine()
    manager = EllidaManager()
    engine.start_engine()
    manager.start_manager()
}
addtask ellidatest

do_testimage[nostamp] = "1"
do_testimage[depends] += "${TESTIMAGEDEPENDS}"
