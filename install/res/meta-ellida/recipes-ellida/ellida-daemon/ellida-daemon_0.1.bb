DESCRIPTION = "Daemon process that manages communication between the engine and the target"
SECTION	= "ellida"
LICENSE	= "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"
SRC_URI = "file://setup.py \
			file://ellida_daemon.py \
				file://ellidadaemon/__init__.py \
				file://ellidadaemon/daemon.py"
S = "${WORKDIR}"
# DEPENDS += "python-pyzmq \
#             python-daemonize"

# inherit pypi setuptools
# inherit pypi setuptools3
# inherit setuptools3
inherit setuptools

RDEPENDS_${PN} += "\
        python-pyzmq \
        python-daemonize"


# export PYTHONPATH="/usr/lib/python3.5/site-packages/:/usr/lib/python3.5/site-packages/"

# do_configure() {
#     export PYTHONPATH=/usr/lib/python3.5/site-packages/:$PYTHONPATH
# }

# export PYTHONPATH=/usr/lib/python3.5/site-packages/:$PYTHONPATH

do_install_append() {
    # export PYTHONPATH=/usr/lib/python3.5/site-packages/:/usr/lib/python/site-packages/:$PYTHONPATH
	install -d ${D}${bindir}
    install -m 0755 ellida_daemon.py ${D}${bindir}
}
