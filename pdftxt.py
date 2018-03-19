#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import re
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

rng = [0, 1, 2]
krizik = 'Vyšší odborná škola a Střední průmyslová škola elektrotechnická Františka Křižíka'
files = ['./ucitele.pdf', './tridy.pdf', './ucebny.pdf']
pattern = [krizik + " ((\S+ \S+)|(\S+))",
           krizik + "(\n\n(\d[A-C])| (V\d))", "UČebna:  (.+)"]


def main():
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()

    result = [[],[],[]]

    for r in rng:
        device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        with file(files[r], 'r') as fp:
            for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0, password='', caching=True, check_extractable=True):
                interpreter.process_page(page)
        text = retstr.getvalue()
        matched = re.findall(pattern[r], text)

        for m in matched:
            if r == 0:
                result[r].append(m[0])
            elif r == 1:
                if m[2] == '':
                    result[r].append(m[1])
                else:
                    result[r].append(m[2])
            else:
                result[r].append(m)

        device.close()

    retstr.close()

    json_result = json.dumps({'ucitele': result[0], 'tridy': result[1], 'ucebny': result[2]})

    with codecs.open('json.json', 'wb') as fp:
        fp.write(json_result)

    print ("PDFs to JSON - SUCCESS")

    return


if __name__ == '__main__':
    sys.exit(main())
