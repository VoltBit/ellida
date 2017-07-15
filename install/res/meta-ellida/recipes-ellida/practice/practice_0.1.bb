DESCRIPTION = "Simple helloworld application"
SECTION	= "ellida"
LICENSE	= "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"
SRC_URI = "file://mitza.c"
S = "${WORKDIR}"
do_compile() {
	${CC} ${LDFLAGS} mitza.c -o mitza
}

do_install() {
	install	-d ${D}${bindir}
	install	-m 0755 mitza ${D}${bindir}
}
