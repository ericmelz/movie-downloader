# Copyright (c) 2000-2020 Synology Inc. All rights reserved.

## You can use CC CFLAGS LD LDFLAGS CXX CXXFLAGS AR RANLIB READELF STRIP after include env.mak
include /env.mak

SUBDIR=ui WIZARD_UIFILES

PYTHON_SCRIPT=backend/app/main.py

.PHONY: all install $(SUBDIR)

all: $(SUBDIR)

$(SUBDIR):
	@echo "===>" $@
	GenerateModuleFiles.php $@ $@
	$(MAKE) -C $@ INSTALLDIR=$(INSTALLDIR)/$@ DESTDIR=$(DESTDIR) PREFIX=$(PREFIX) $(MAKECMDGOALS);
	@echo "<===" $@

packageinstall: $(SUBDIR)

install: $(SUBDIR)
	mkdir -p $(DESTDIR)/backend
        cp -r backend $(DESTDIR)

