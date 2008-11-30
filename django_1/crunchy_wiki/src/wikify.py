#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2008 André Roberge
#
# adapted from wiki.py in cccwiki app
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

class Transform(object):
    """Abstraction for a regular expression transform.

    Transform subclasses have two properties:
       regexp: the regular expression defining what will be replaced
       replace(MatchObject): returns a string replacement for a regexp match

    We iterate over all matches for that regular expression, calling replace()
    on the match to determine what text should replace the matched text.

    The Transform class is more expressive than regular expression replacement
    because the replace() method can execute arbitrary code to, e.g., look
    up a WikiWord to see if the page exists before determining if the WikiWord
    should be a link.
    """
    def run(self, content):
        """Runs this transform over the given content.

        We return a new string that is the result of this transform.
        """
        parts = []
        offset = 0
        for match in self.regexp.finditer(content):
            parts.append(content[offset:match.start(0)])
            parts.append(self.replace(match))
            offset = match.end(0)
        parts.append(content[offset:])
        return ''.join(parts)


class WikiWords(Transform):
    """Translates WikiWords to links.
    """
    def __init__(self):
        self.regexp = re.compile(r'[A-Z][a-z0-9]+([A-Z][a-z0-9]+)+')

    def replace(self, match):
        wikiword = match.group(0)

        return '<a class="wikiword" href="/%s">%s</a>' % (wikiword, wikiword)

        #if Page.exists(wikiword):
        #    return '<a class="wikiword" href="/%s">%s</a>' % (wikiword, wikiword)
        #else:
        #    return wikiword

def to_wiki_link(name):
    return '<a class="wikiword" href="/%s">%s</a>' % (name, name)

class AutoLink(Transform):
    """A transform that auto-links URLs."""
    def __init__(self):
            self.regexp = re.compile(r'([^"])\b((http|https)://[^ \t\n\r<>\(\)&"]+' \
                               r'[^ \t\n\r<>\(\)&"\.])')

    def replace(self, match):
        url = match.group(2)
        return match.group(1) + '<a class="autourl" href="%s">%s</a>' % (url, url)


class ExternalLink(Transform):
    """A transform that make external hyperlinks open in new window/tab
       depending on browser configuration."""

    def __init__(self):
        self.regexp = re.compile(r'href="(http[^"]+)"')

    def replace(self, match):
        url = match.group(1)
        return 'href="' + url + '" target="_blank" class="external_link"'