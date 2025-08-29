NAME=ledtrix
VERSION?=$(shell grep '^version=' library.properties | cut -d'=' -f2)

build:
	@if [ -z "${VERSION}" ]; then \
		echo "ERROR: VERSION is not set and could not be determined from library.properties!"; \
		exit 1; \
	fi
	@if ! echo "${VERSION}" | grep -Eq "^[0-9]+\.[0-9]+\.[0-9]+$$"; then \
		echo "ERROR: VERSION must be in major.minor.patch format (e.g., 1.2.3). Was '${VERSION}'"; \
		exit 1; \
	fi
	sed -i "s/^version=.*/version=${VERSION}/" library.properties
	python3 ./generate/main.py
	rm -rf ${NAME}-${VERSION}.zip ${NAME}-${VERSION}.tar.gz; \
	zip -rq ${NAME}-${VERSION}.zip frame.c frame.h ledtrix.c ledtrix.h keywords.txt library.properties LICENSE README.md examples/; \
	tar -czf ${NAME}-${VERSION}.tar.gz frame.c frame.h ledtrix.c ledtrix.h keywords.txt library.properties LICENSE README.md examples/; \

clean:
	rm -rf ${NAME}-${VERSION}.zip ${NAME}-${VERSION}.tar.gz