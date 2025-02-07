#!/bin/bash

source /pkgscripts/include/pkg_util.sh

package="MovieDownloader"
version="1.0.0-0001"
displayname="Movie Downloader"
os_min_ver="7.0-40000"
maintainer="Eric Melz"
arch="$(pkg_get_platform)"
description="Download a PDF of movies in the /video/movies folder"
dsmuidir="ui"
[ "$(caller)" != "0 NULL" ] && return 0
pkg_dump_info
