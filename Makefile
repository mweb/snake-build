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
	@echo '  build'
	@echo '  install'
	@echo '  clean'
	@echo '  build-pkg
	@echo '  update-pot'

all: build

build:
	${PYTHON} setup.py build

build-pkg: clean
	mkdir build
	cp * -rf build
	cd build
	make clean
	dpkg-buildpackage

clean:
	-$(PYTHON) setup.py clean --all
	find . \( -name '*.py[cdo]' -o -name '*.so' \) -exec rm -f '{}' ';'
	rm -f build

install:
	${PYTHON} setup.py install --root="$(DESTDIR)/" --prefix="$(PREFIX)" --force

test:
	cd tests && $(PYTHON) run-tests.py

coverage:
	cd coverage && ./run_coverage.sh

update-pot: i18n/snakebuild.pot


i18n/snakebuild.pot:
	$(PYTHON) i18n/snakebuildgettext sb-resourceclient \
		snakebuild/resourceclient/clientcmds > i18n/snakebuild.pot
	echo $(PYFILES) $(BINARY_PYFILES) | xargs \
		xgettext --package-name "snakebuild" \
		--msgid-bugs-address "<mathew.weber@gmail.com>" \
		--copyright-holder "<mathew.weber@gmail.com>" \
		--from-code ISO-8859-1 --join --sort-by-file --add-comments=i18n: \
		-d snakebuild -p i18n -o snakebuild.pot
	$(PYTHON) i18n/posplit i18n/snakebuild.pot

%.po: i18n/snakebuild.pot
	msgmerge --no-location --update $@ $^

.PHONY: help all build clean install build-pkg tests update-pot
