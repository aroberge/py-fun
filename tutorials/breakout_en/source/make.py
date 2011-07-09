#!/usr/bin/env python
from glob import glob
from mako.template import Template
from mako.lookup import TemplateLookup
from sys import argv
from os import unlink
from xml.etree import ElementTree

TAGS = ["js_code", "explain_before", "explain_after", "experiment", "title",
                        "hidden_code", "library", "fullgame"]

PAGES = ["index", "ball", "colour", "move", "library_", "bounce", "sound", 
         "mute", "paddle", "keyboard", "mouse", "bricks", "finish", "resources",
         "test"]

def clean():
    '''removes existing html files'''
    for f in glob("../*.html"): unlink(f)

def required(page, required_vars):
    '''ensures a list of required variables have an entry in a dict'''
    for var in required_vars: 
        page[var] = page.get(var, "")

def tag_content(elem):
    '''extract the content for a given xml element'''
    tag = elem.tag
    tag_length = len(elem.tag) + 2
    return ElementTree.tostring(elem, encoding="utf-8").strip()[tag_length: 
                                                                -(tag_length+1)]

def build(offline=False):
    '''create new set of html files for entire project'''
    #pages = eval(file("data.py").read())

    pages = []
    for name in PAGES:
        with open(name + '.xml', 'r') as f:
            tree = ElementTree.parse(f)
        page = {}
        page["name"] = name
        for tag in TAGS:
            elem = tree.find(tag)
            if elem is not None:
                page[tag] = tag_content(elem)
            else:
                page[tag] = ""
        pages.append(page)


    toc = [(page["title"], page["name"]+".html") for page in pages]

    for i, page in enumerate(pages):
        if page["name"] != "test":
            page["prev"] = pages[i-1]["name"] if i > 0 else ""
            page["next"] = pages[i+1]["name"] if i+1 < len(pages) else ""
            page["toc"]  = toc
        if offline:
            page["jquery"] = "../js/jquery-1.5.1.min.js"
            page["jquery_ui"] = "../js/jquery-ui-1.8.13.custom.min.js"
        else:
            page["jquery"] = "http://ajax.googleapis.com/ajax/libs" \
                             "/jquery/1.6.1/jquery.min.js"
            page["jquery_ui"] = "http://ajax.googleapis.com/ajax/libs" \
                                "/jqueryui/1.8.14/jquery-ui.min.js"

        file('../' + page['name'] + '.html', 'w').write(
            Template(filename="template.mak",
                     lookup=TemplateLookup(directories=['.'])).render(**page))

if __name__ == "__main__":
    clean()
    offline = False
    if argv[-1].lower() == "offline":
        offline = True
    build(offline)
