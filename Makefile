# $Id: Makefile,v 1.6 2008/10/29 01:01:35 ghantoos Exp $
include defs.mk

PYTHON=`which python`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/testpool
PROJECT=testpool
export VERSION:=`python ./setup.py --version`

info::
	@echo "version ${VERSION}"

clean::
	python ./setup.py clean
	rm -rf dist build MANIFEST
	find . -name '*.pyc' -delete
	rm -rf ../testpool_* testpool-* deb_dist testpool.egg-info


.PHONY: help
help::
	@echo "make source - Create source package"
	@echo "make install - Install on local system"
	@echo "make build - Generate a rpm package"
	@echo "make clean - Get rid of scratch and byte files"

build::
	python ./setup.py build
