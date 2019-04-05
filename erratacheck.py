#!/usr/bin/env python3
# ---------------------------------------------------------------
# erratacheck.py: Check for new OpenBSD errata
# Copyright (c) 2018 Jason J.A. Stephenson <jason@sigio.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# ---------------------------------------------------------------

# Download the OpenBSD Errata and report if there are new errata.

from configparser import ConfigParser
from html.parser import HTMLParser
import datetime, os.path, re, time, urllib.request, urllib.error

# Globals:
# The last id in the patch sequence for this release.
sequence = 0

class MyHTMLParser (HTMLParser):
    def __init__(self, last_seq):
        HTMLParser.__init__(self)
        self.last_sequence = last_seq
        self.item = None
        self.have_strong = False
        self.have_italics = False
        self.have_break = False
        self.sequence = 0
        self.what = None
        self.when = None
        self.arch = None
        self.description = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            if self.item != None:
                if int(self.sequence) > self.last_sequence:
                    self.report()
                self.description = ''
                self.have_break = False
            for (name, value) in attrs:
                if name == 'id':
                    self.item = value
        if tag == 'strong':
            self.have_strong = True
        if tag == 'i':
            self.have_italics = True
        if tag == 'br' and self.item != None and not self.have_break:
            self.have_break = True

    def handle_endtag(self, tag):
        if tag == 'ul':
            self.item = None
            if int(self.sequence) > self.last_sequence:
                self.report()
        if tag == 'strong':
            self.have_strong = False
        if tag == 'i':
            self.have_italics = False

    def handle_data(self, data):
        if self.have_strong and self.item != None:
            (self.sequence, self.what, self.when) = data.split(': ')
        if self.have_italics and self.item != None:
            self.arch = data
            self.have_arch = True
        if self.have_break:
            self.description = self.description + data

    def close(self):
        global sequence
        sequence = int(self.sequence)

    def report(self):
        print(self.sequence + ": " + self.what + ": " + self.when + ": " + self.arch)
        print(re.sub('\n+', '\n', self.description))

### End of MyHTMLParser ###

if __name__ == '__main__':
    # Load the configuration.
    config_path = os.path.expanduser('~/erratacheck.ini')
    config = ConfigParser()
    config.read(config_path)
    # Get the last sequence value.
    sequence = config['Errata'].getint('sequence')
    # Get a datetime object for the If-Modified-Since header
    since_when = datetime.datetime.utcfromtimestamp(config['Errata'].getfloat('unixstamp'))
    headers = {
        'If-Modified-Since': since_when.strftime("%A, %d-%b-%y %H:%M:%S GMT") 
    }
    try:
        request = urllib.request.Request(config['Errata']['URL'], headers=headers)
        u = urllib.request.urlopen(request)
        parser = MyHTMLParser(sequence)
        parser.feed(u.read().decode('latin_1'))
        parser.close()
        # Update the configuration file.
        config['Errata']['unixstamp'] = str(time.time())
        config['Errata']['sequence'] = str(sequence)
        with open(config_path, 'w') as f:
            config.write(f)
    except urllib.error.HTTPError as e:
        print("{0} {1}".format(e.code(), e.reason()))
