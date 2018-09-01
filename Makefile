# $Id: Makefile,v 1.6 2008/10/29 01:01:35 ghantoos Exp $
include defs.mk

PYTHON=`which python`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/testpool
PROJECT=testpool
export VERSION:=`git describe --abbrev=0 --tag`


##
# Use find when __init__.py does not exist in the directory.
PYTHON_FILES+=*.py testpoolclient examples 
##

info::
	@echo "version ${VERSION}"
	@echo "PYTHON_FILES=${PYTHON_FILES}"

clean::
	python ./setup.py clean
	rm -rf dist build MANIFEST
	find . -name '*.pyc' -delete
	rm -rf ../testpool_* testpool-* deb_dist testpool_client.egg-info


.PHONY: help
help::
	@echo "make source - Create source package"
	@echo "make install - Install on local system"
	@echo "make build - Generate a rpm package"
	@echo "make clean - Get rid of scratch and byte files"

pycodestyle::
	pycodestyle --exclude=testpool/db/testpooldb/migrations $(PYTHON_FILES)

build::
	python ./setup.py sdist
