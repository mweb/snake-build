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
	@echo '  clean      - Clean build remobe all files created by other targets'
	@echo '  update-pot - Generate the pot files'

all: source doc

source:
	${PYTHON} setup.py sdist

doc:
	echo "TODO"

install:
	${PYTHON} setup.py ${PURE} install --root="${DESTDIR}/" --prefix="${PREFIX}"

clean:
	-$(PYTHON) setup.py clean --all
	find . \( -name '*.py[cdo]' -o -name '*.so' \) -exec rm -f '{}' ';'
	rm -f MANIFEST MANIFEST.in coverage/.coveragerc
	rm -rf test/data/*
	-rm -rf dist

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
