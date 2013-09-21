#!/bin/bash

#Import tools for compiling extension binaries
export PATH=$PATH:/usr/lib/ure/bin/
export PATH=$PATH:/usr/lib/libreoffice/sdk/bin/

#Setup directories 
mkdir "${PWD}"/SMF/
mkdir "${PWD}"/SMF/META-INF/

#Compile the binaries
idlc "${PWD}"/idl/Xsmf.idl
regmerge -v "${PWD}"/SMF/Xsmf.rdb UCR "${PWD}"/idl/Xsmf.urd
rm "${PWD}"/idl/Xsmf.urd

#Copy extension files and generate metadata
cp -f "${PWD}"/src/smf.py "${PWD}"/SMF/
cp -f "${PWD}"/src/ystockquote.py "${PWD}"/SMF/
python "${PWD}"/src/generate_metainfo.py

#Package into oxt file
pushd "${PWD}"/SMF/
zip -r "${PWD}"/SMF.zip ./*
popd
mv "${PWD}"/SMF/SMF.zip "${PWD}"/SMF.oxt
