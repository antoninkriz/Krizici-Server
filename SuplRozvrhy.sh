#!/bin/bash
wget 213.151.86.106/_rozvrh/tridy.pdf
wget 213.151.86.106/_rozvrh/ucitele.pdf
wget 213.151.86.106/_rozvrh/ucebny.pdf

./pdftxt.py

convert tridy.pdf trc.png
convert ucitele.pdf uci.png
convert ucebny.pdf uce.png

mogrify -flatten *.png

optipng *.png

rename 's/trc/imgtridy/g' *.png
rename 's/uci/imgucitele/g' *.png
rename 's/uce/imgucebny/g' *.png

mv img* /var/www/html/files/apps/krizici/
mv json.json /var/www/html/files/apps/krizici/

rm *pdf.*
rm *.pdf
rm *.png

exit 0
