#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import json
import codecs
from xml.etree import ElementTree as Et


def main():
    pattern_table = re.compile(r'<table class="common">[\s\S]+?(?=</table>)')
    pattern_a1 = re.compile(r'<a href=".*">')
    pattern_a2 = re.compile(r'</a>')

    with open("./contacts.html", 'r') as fp:
        html_file = fp.read()

    html = unicode(html_file, "ISO-8859-2").encode('utf-8')
    matches = re.search(pattern_table, html)

    if matches is not None:
        table = matches.group(0) + '</table>'
        table = table.replace("<thead>", "").replace("</thead>", "").replace("<tbody>", "").replace("</tbody>", "").replace(
            "<strong>", "").replace("</strong>", "")
        table = re.sub(pattern_a1, "", table)
        table = re.sub(pattern_a2, "", table)

        table = Et.XML(table)
        rows = iter(table)
        headers = [col.text for col in next(rows)]

        arr = []

        for row in rows:
            values = [col.text for col in row]
            res = dict(zip(headers, values))
            arr.append(res)

        arr.pop(len(arr) - 1)
        json_result = json.dumps(arr)

        if len(json_result) > 100:
            with codecs.open('contacts.json', 'wb') as fp:
                fp.write(json_result)
            print ("Contacts to JSON - SUCCESS")
        else:
            print ("Contacts to JSON - FAILED - Length not OK")
    else:
        print ("Contacts to JSON - FAILED - Matches not OK")


if __name__ == '__main__':
    sys.exit(main())

