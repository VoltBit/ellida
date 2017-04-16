ellida_devsetup() {
    CONF="alias ls = 'ls --color'"
    cd ~
    echo $CONF > .bashrc
    source .bashrc
}

IMAGE_POSTPROCESS_COMMAND += " ellida_devsetup ; "
