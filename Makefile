.PHONY: build build-and-upload build-debian-package build-python-dists build-docs clean-build \
	clean test-all

build: build-debian-package build-python-dists build-docs

build-and-upload: build twine-upload AUR-upload PPA-upload


# Building
#
build-debian-package:
	mkdir -p build/debian

build-arch-package:
	mkdir -p build/arch

build-python-dists:
	mkdir -p build/python
	python3 setup.py -d build/python sdist bdist_wheel

build-docs:
	make html -C docs

# Testing

test-all:
	./scripts/sanity_check.sh

# Uploading

twine-upload:
	twine upload -r pypi build/python/*

AUR-upload: build-arch-package
	echo kek

PPA-upload: build-debian-package
	dput ppa:jacotsu/polibeepsync hello_2.10-0ubuntu1.changes

# Cleaning

clean-build: clean build

clean:
	rm -rf docs/build
	rm -rf build
