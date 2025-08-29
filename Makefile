NAME=ledtrix
VERSION?=$(shell grep '^version=' library.properties | cut -d'=' -f2)

build:
	@if [ -z "${VERSION}" ]; then \
		echo "ERROR: VERSION is not set and could not be determined from library.properties!"; \
		exit 1; \
	fi
	sed -i "s/^version=.*/version=${VERSION}/" library.properties
	python3 ./generate/main.py
	rm -rf ${NAME}-${VERSION}.zip ${NAME}-${VERSION}.tar.gz; \
	zip -r ${NAME}-${VERSION}.zip frame.c frame.h ledtrix.c ledtrix.h keywords.txt library.properties LICENSE README.md examples/; \
	tar -czvf ${NAME}-${VERSION}.tar.gz frame.c frame.h ledtrix.c ledtrix.h keywords.txt library.properties LICENSE README.md examples/; \