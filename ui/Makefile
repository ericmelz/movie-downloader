include /env.mak

JS_DIR="dist"
JS_NAMESPACE="SYNO.SDS.App.MovieDownloader"
BUNDLE_JS="dist/movie_downloader.bundle.js"
BUNDLE_CSS="dist/style/movie_downloader.bundle.css"

.PHONY: all $(SUBDIR)

all: $(BUNDLE_JS) style.css $(SUBDIR)

$(BUNDLE_JS):
	/usr/local/tool/snpm i
	/usr/local/tool/snpm build
	$(MAKE) -f Makefile.js.inc JSCompress JS_NAMESPACE=\"${JS_NAMESPACE}\" JS_DIR=${JS_DIR}

$(SUBDIR):
	@echo "===>" $@
	$(MAKE) -C $@ INSTALLDIR=$(INSTALLDIR)/$@ DESTDIR=$(DESTDIR) PREFIX=$(PREFIX) $(MAKECMDGOALS);
	@echo "<===" $@

style.css: $(BUNDLE_JS)
	cp $(BUNDLE_CSS) $@

clean: clean_JSCompress $(SUBDIR)
	rm $(BUNDLE_JS)

install: $(SUBDIR) install_JSCompress
	[ -d $(INSTALLDIR)/texts ] || install -d $(INSTALLDIR)/texts
	cp -a texts $(INSTALLDIR)
	[ -d $(INSTALLDIR)/images ] || install -d $(INSTALLDIR)/images
	cp -a images $(INSTALLDIR)

packageinstall: $(SUBDIR)

include Makefile.js.inc
