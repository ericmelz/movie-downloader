# Copyright (c) 2000-2020 Synology Inc. All rights reserved.

## You can use CC CFLAGS LD LDFLAGS CXX CXXFLAGS AR RANLIB READELF STRIP after include env.mak
include /env.mak

EXEC= testPkg1
OBJS= testPkg1.o
PYTHON_SCRIPT= test1.py

SUBDIR=ui WIZARD_UIFILES

.PHONY: all install $(SUBDIR)

all: $(EXEC) $(SUBDIR)

$(SUBDIR):
	@echo "===>" $@
	GenerateModuleFiles.php $@ $@
	$(MAKE) -C $@ INSTALLDIR=$(INSTALLDIR)/$@ DESTDIR=$(DESTDIR) PREFIX=$(PREFIX) $(MAKECMDGOALS);
	@echo "<===" $@

packageinstall: $(SUBDIR)

install: $(EXEC) $(SUBDIR)
	mkdir -p $(DESTDIR)/usr/local/bin/
	install $< $(DESTDIR)/usr/local/bin/
	install -m 755 $(PYTHON_SCRIPT) $(DESTDIR)/usr/local/bin/

clean:
	rm -rf *.o $(EXEC)
