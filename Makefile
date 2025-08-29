NAME=ledtrix
VERSION?=unset
VERSION_STRIPPED=$(shell echo $(VERSION) | sed 's/^v//')

build:
	@if [ "$(VERSION)" = "unset" ]; then \
		echo "ERROR: VERSION must be provided!"; \
		exit 1; \
	fi
	@if ! echo "$(VERSION_STRIPPED)" | grep -Eq "^[0-9]+\.[0-9]+\.[0-9]+$$"; then \
		echo "ERROR: VERSION must be in major.minor.patch format (e.g., 1.2.3). Was '$(VERSION_STRIPPED)'"; \
		exit 1; \
	fi
	sed -i "s/^version=.*/version=${VERSION}/" library.properties
	python3 ./generate/main.py
	rm -rf ${NAME}-${VERSION}.zip ${NAME}-${VERSION}.tar.gz; \
	zip -rq ${NAME}-${VERSION}.zip frame.c frame.h ledtrix.c ledtrix.h keywords.txt library.properties LICENSE README.md examples/; \
	tar -czf ${NAME}-${VERSION}.tar.gz frame.c frame.h ledtrix.c ledtrix.h keywords.txt library.properties LICENSE README.md examples/; \

clean:
	rm -rf ${NAME}-*.zip ${NAME}-*.tar.gz