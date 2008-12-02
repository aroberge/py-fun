# -*- coding: utf-8 -*-
#
# Copyright 2008 André Roberge
#
# Some of the code has been adapted from wiki.py in cccwiki app
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

import os
import re
import sys
from xml.etree.ElementTree import tostring, fromstring

from django.template.loader import render_to_string
from docutils import core, io

from src import crunchy_rst
from src import vlam

static_path = os.path.normpath(os.path.join(
                            os.path.dirname(__file__), '..', 'static', 'html'))

DTD = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '\
'"http://www.w3.org/TR/xhtml1/DTD/strict.dtd">\n'

def rst_to_html(input_string, source_path=None, destination_path=None,
               input_encoding='unicode', doctitle=1, initial_header_level=1):
    """
    Given an input string, returns it as the body of an html document.

    Adapted from example.py included in docutils distribution.
    """
    overrides = {'input_encoding': input_encoding,
                 'doctitle_xform': doctitle,
                 'initial_header_level': initial_header_level,
                 # the next two are for security reasons, to prevent malicious
                 # insertion of raw html code.
                 'file_insertion_enabled': False,
                 'raw_enabled': False,
                 }
    parts = core.publish_parts(
        source=input_string, source_path=source_path,
        destination_path=destination_path,
        writer_name='html', settings_overrides=overrides)
    return parts['html_body']

def to_html(page_content, page_name):
    # need to use "safe" in view.html with django 1.0 and the following:

    content = rst_to_html(page_content, page_name)

    for transform in [WikiWords(), ExternalLink()]:
        content = transform.run(content)

    save_hard_copy(page_name, "view.html", {"page_name": page_name,
                                            "content": content})
    return content

def save_hard_copy(file_name, template, _dict):
    '''saves a hard copy of a processed page to a default static directory'''
    page = vlam.CrunchyPage(render_to_string(template, _dict).replace(
        ' xmlns="http://www.w3.org/1999/xhtml"', ''))
    path = os.path.join(static_path, file_name+'.html')
    f = open(path, 'w')
    f.write(page.read())
    f.close()

    #out = fromstring(render_to_string(template, _dict).replace(
    #    ' xmlns="http://www.w3.org/1999/xhtml"', ''))
    #path = os.path.join(static_path, file_name+'.html')
    #f = open(path, 'w')
    #f.write(tostring(out))
    #f.close()

    return


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


def to_wiki_link(name):
    return '<a class="wikiword" href="/%s">%s</a>' % (name, name)

def linkify_list(pages):
    new_pages = []
    for page in pages:
        new_pages.append({'name':to_wiki_link(page.name)})
    return new_pages

class ExternalLink(Transform):
    """A transform that make external hyperlinks open in new window/tab
       depending on browser configuration."""

    def __init__(self):
        self.regexp = re.compile(r'href="(http[^"]+)"')

    def replace(self, match):
        url = match.group(1)
        return 'href="' + url + '" target="_blank"><img src="/static/images/external.png"/'