#!/bin/bash

PYTHON=/usr/bin/python
PYFILES=*.py # TODO search for python files
# create the snakebuild.pot file for translation

cd ..
${PYTHON} i18n/snakebuildgettext ...


# use xgettext
echo ${PYFILES} | xargs \
  xgettext --package-name "snakebuild" \
    --msgid-bugs-address "mathew.weber@gmail.com" \
    --copyright-hodler "Mathias Weber <mathew.weber@gmail.com>" \
    --from-code ISO-8859-1 --join --sort-by-file --add-comments=i18n \
    --d snakebuild -p i18n -o snakebuild.pot

${PYTHON} i18n/posplit i18n/snakebuild.pot
