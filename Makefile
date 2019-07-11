.PHONY: build build-and-upload build-PPA build-python-dists build-docs clean-build \
	clean test-all upload-twine upload-PPA upload-AUR

build: build-python-dists build-PPA build-arch-package build-windows-installer build-docs

build-and-upload: build upload-twine upload-AUR upload-PPA

VERSION = $(shell grep -Po "(?<=^__version__ = \").*(?=\")" polibeepsync/__init__.py)


# Building
#
build-PPA:
	$(info Building PPA)
	mkdir -p packaging/ubuntu/deb
	python3 setup.py --command-packages=stdeb.command sdist_dsc \
		--with-python3=true \
		--with-python2=false \
		-x packaging/ubuntu/stdeb.cfg \
		-d packaging/ubuntu/deb
	rsync -r packaging/ubuntu/polibeepsync-template/* packaging/ubuntu/deb/polibeepsync-$(VERSION)
	cd packaging/ubuntu/deb/polibeepsync-$(VERSION) && \
		dpkg-source --commit . add_desktop_file_and_icon && \
		debuild -S -k205ABB76D38C4928714ACD3CDAE2A4AB08E9C765
	rm -rf dist poliBeePsync-$(VERSION).tar.gz

build-arch-package:
	$(info Building arch package)
	mkdir -p packaging/arch/build
	echo not implemented
	sed -i "s/pkgver=.*/pkgver=$(VERSION)/" packaging/arch/PKGBUILD
	cd distro_packaging/arch; \
	makepkg --printsrcinfo > .SRCINFO; \
	makepkg

build-windows-installer:
	$(info Building windows installer)
	mkdir -p packaging/windows
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

upload-twine: build-python-dists
	$(info Uploading to pypi)
	twine upload -r pypi packaging/pypi/poliBeePsync-$(VERSION)*

upload-AUR: build-arch-package
	$(info Uploading to AUR)
	cd distro_packaging/arch; \
	git add PKGBUILD .SRCINFO; \
	git commit \
	git push

upload-PPA: build-PPA
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
