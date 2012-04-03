# This is the make file to greate the packages, documentation,... for the
# snakebuild application. See help for all possible targets.

PREFIX=/usr/local
export PREFIX
PYTHON=python
PYFILES:=$(shell find snakebuild -name '*.py')
BINARY_PYFILES:=$(ls bin/)
DOCFILES="doc/*.png doc/*.html"

help:
	@echo 'Possible make targets:'
	@echo '  all        - build the app and the documentation'
	@echo '  source     - Create source package'
	@echo '  install    - Install app and doc in respect to PREFIX ($(PREFIX))'
	@echo '  documentation - Create the documentaion from the asciidoc'
	@echo '  clean      - Clean build remobe all files created by other targets'
	@echo '  update-pot - Generate the pot files'

all: documentation source

source:
	${PYTHON} setup.py build
	${PYTHON} setup.py sdist

documentation: doc/snake-build.asciidoc \
   doc/snake-build-dev.asciidoc \
   doc/config.asciidoc \
   doc/communication.asciidoc\
   doc/development.asciidoc
	asciidoc doc/snake-build.asciidoc
	asciidoc doc/snake-build-dev.asciidoc

install:
	${PYTHON} setup.py ${PURE} install --root="${DESTDIR}/" --prefix="${PREFIX}"

clean:
	-$(PYTHON) setup.py clean --all
	find . \( -name '*.py[cdo]' -o -name '*.so' \) -exec rm -f '{}' ';'
	rm -f MANIFEST MANIFEST.in coverage/.coveragerc
	rm -rf test/data/*
	-rm -rf dist
	-rm -rf doc/*.html
	-rm -rf locale
	-rm -rf snakebuild/locale

check: tests

tests:
	cd tests && $(PYTHON) run-tests.py

coverage:
	cd coverage && ./run_coverage.sh

update-pot: i18n/snakebuild.pot


i18n/snakebuild.pot:
	$(PYTHON) i18n/snakebuildgettext sb-resourceclient \
		snakebuild/resourceclient/clientcmds > i18n/snakebuild.pot
	$(PYTHON) i18n/configgettext data/*.conf >> i18n/snakebuild.pot
	echo $(PYFILES) $(BINARY_PYFILES) | xargs \
		xgettext --package-name "snakebuild" \
		--msgid-bugs-address "<mathew.weber@gmail.com>" \
		--copyright-holder "<mathew.weber@gmail.com>" \
		--from-code ISO-8859-1 --join --sort-by-file --add-comments=i18n: \
		-d snakebuild -p i18n -o snakebuild.pot
	$(PYTHON) i18n/posplit i18n/snakebuild.pot

%.po: i18n/snakebuild.pot
	msgmerge --no-location --update $@ $^

.PHONY: help all source clean install tests update-pot
