.PHONY: build build-and-upload build-PPA build-python-dists build-docs clean-build \
	clean test-all

build: build-python-dists build-PPA build-arch-package build-windows-installer build-docs

build-and-upload: build twine-upload AUR-upload PPA-upload

VERSION = $(shell grep -Po "(?<=^__version__ = \").*(?=\")" polibeepsync/__init__.py)


# Building
#
build-PPA:
	$(info Building PPA)
	mkdir -p packaging/ubuntu
	python3 setup.py --command-packages=stdeb.command bdist_deb
	rsync deb_dist packaging/ubuntu
	rm -rf deb_dist dist poliBeePsync-$(VERSION).tar.gz

build-arch-package:
	$(info Building arch package)
	mkdir -p packaging/arch/build
	echo not implemented
	sed -i "s/pkgver=.*/pkgver=$(VERSION)/" packaging/arch/PKGBUILD
	#cd distro_packaging/arch; \
	#makepkg --printsrcinfo > .SRCINFO; \
	#makepkg

build-windows-installer:
	$(info Building windows installer)
	mkdir -p build/windows
	# Pretty fragile and will change the python version too if it comes before the
	# application version
	sed -i "0,/^version=/s/^version=.*/version=$(VERSION)/" packaging/windows/installer.cfg
	pynsist packaging/windows/installer.cfg

build-python-dists:
	$(info Building python dists)
	mkdir -p packaging/pypi
	python3 setup.py sdist -d packaging/pypi bdist_wheel -d packaging/pypi

build-docs:
	make html -C docs

# Testing

test-all:
	$(info Testing poliBeePSync:$(VERSION))
	./scripts/sanity_check.sh

# Uploading

twine-upload: build-python-dists
	$(info Uploading to pypi)
	twine upload -r pypi packaging/pypi/poliBeePsync-$(VERSION)*

AUR-upload: build-arch-package
	$(info Uploading to AUR)
	echo Not implemented

PPA-upload: build-PPA
	$(info Uploading to Launchpad)
	dput ppa:jacotsu/polibeepsync packaging/ubuntu/deb_dist/polibeepsync_$(VERSION)-1_source.changes

# Cleaning

clean-build: clean build

clean:
	$(info Cleaning builds)
	rm -rf docs/build
	rm -rf packaging/ubuntu
	rm -rf packaging/pypi
	rm -rf packaging/windows/build
