#!/bin/sh

docker run -it \
    --volume="$(pwd):/root/pep/input_files:ro" \
    --name pep \
    --hostname pep \
    --rm \
    naturo/pep $@ \

