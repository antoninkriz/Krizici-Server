#!/bin/bash
#Download PDFs and HTML table with all contacts
wget 213.151.86.106/_rozvrh/tridy.pdf
wget 213.151.86.106/_rozvrh/ucitele.pdf
wget 213.151.86.106/_rozvrh/ucebny.pdf
wget "http://vosaspsekrizik.cz/cs/kontakty/vyhledavani.ep/?name=&subject_id=0&x=23&y=7&action=search" -O contacts.html

#Get contacts list from website to JSON
./contxt.py

#Export data from PDFs
./pdftxt.py

#Convert PDF to PNG
convert tridy.pdf trc.png
convert ucitele.pdf uci.png
convert ucebny.pdf uce.png

#Make PNGs smaller
mogrify -flatten *.png
optipng *.png

#Rename PNG files
rename 's/trc/imgtridy/g' *.png
rename 's/uci/imgucitele/g' *.png
rename 's/uce/imgucebny/g' *.png

#Move all to desired folder
mv img* /var/www/html/files/apps/krizici/
mv *.json /var/www/html/files/apps/krizici/

#Clean
rm *pdf.*
rm *.pdf
rm *.png
rm *.html
rm *.json

exit 0
