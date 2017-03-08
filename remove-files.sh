#! /bin/sh

version=$1

[ -z $version ] && exit 1

dir=matplotlib-${version}
file=matplotlib-${version}.tar.gz
result=matplotlib-${version}-without-copyrighted.tar.xz

test -f $file || exit 1

rm -rf matplotlib-${version}
tar xzf $file

# https://github.com/matplotlib/matplotlib/issues/8034
rm -vr matplotlib-${version}/lib/matplotlib/mpl-data/sample_data/necked_tensile_specimen.png
rm -vr matplotlib-${version}/examples/images_contours_and_fields/interpolation_none_vs_nearest.py

rm -f $result
tar cJf $result $dir
