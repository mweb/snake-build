# This is the make file to greate the packages, documentation,... for the
# snakebuild application. See help for all possible targets.

PREFIX=/usr/local
export PREFIX
PYTHON=python
PYFILES:=$(shell find snakebuild -name '*.py')
BINARY_PYFILES:=$(ls bin/)

help:
	@echo 'Possible targets:'
	@echo '  all'
	@echo '  source - Create source package'
	@echo '  install - Install on local system'
	@echo '  clean - Get rid of scratch and byte files'
	@echo '  buildrpm - Generate a rpm package'
	@echo '  builddeb - Generate a deb package'
	@echo '  update-pot - Generate the pot files'

all: source

source:
	${PYTHON} setup.py sdist ${COMPILE}

install:
	${PYTHON} setup.py install --root ${DESTDIR} ${COMPILE}

buildrpm:
	${PYTHON} setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

builddeb:
	# build the source package in the parent diretory
	# then rename it to project_version.orig.tar.gz
	${PYTHON} setup.py sdist $(COMPILE) --dist-dir=../ --prune
	rename -f 's/${PROJECT}-(.*)\.tar\.gz/${PROJECT}_$$1\.orig\.tar\.gz/' ../*
	# build the package
	dpkg-buildpackage -i\.git\|.*png -rfakeroot

build-pkg: clean
	mkdir build_pkg
	-cp * -rf build_pkg
	cd build_pkg
	dpkg-buildpackage

clean:
	-$(PYTHON) setup.py clean --all
	${MAKE} -f ${CURDIR}/debian/rules clean
	find . \( -name '*.py[cdo]' -o -name '*.so' \) -exec rm -f '{}' ';'
	-rm -rf build MANIFEST

test:
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

.PHONY: help all source clean install builddeb buildrmp tests update-pot
