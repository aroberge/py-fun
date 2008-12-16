"""  file_service.py

Provides the means to save and load a file.
"""

import os
import sys
import urllib

from xml.etree.ElementTree import SubElement

DEBUG = False

def filtered_dir(request, _filter=None):
    '''returns the file listing from a directory,
       satisfying a given filter function,
       in a form suitable for the jquery FileTree plugin.'''
    ul = ['<ul class="jqueryFileTree" style="display: none;">']
    # request.data is of the form "dir=SomeDirectory"
    try:
        d = urllib.unquote(request.data)[4:]
        d = urllib.unquote(d)  # apparently need to call it twice on windows
        for f in os.listdir(d):
            if _filter(f, d):
                continue
            ff = os.path.join(d, f)
            if os.path.isdir(ff):
                ul.append('<li class="directory collapsed">'
                          '<a href="#" rel="%s/">%s</a></li>' % (ff, f))
            else:
                ext = os.path.splitext(f)[1][1:] # get .ext and remove dot
                ul.append('<li class="file ext_%s">'
                          '<a href="#" rel="%s">%s</a></li>' % (ext, ff, f))
        ul.append('</ul>')
    except Exception,e:
        ul.append('Could not load directory: %s' % str(e))
    ul.append('</ul>')
    request.wfile.write(''.join(ul))
    return

def insert_file_tree(page, elem, uid, action, callback, title, label):
    '''inserts a file tree object in a page.'''
    if not page.includes("jquery_file_tree"):
        page.add_include("jquery_file_tree")
        page.insert_js_file("/javascript/jquery.filetree.js")
        page.insert_css_file("/css/jquery.filetree.css")
    else:
        return
    tree_id = "tree_" + uid
    form_id = "form_" + uid
    root = os.path.splitdrive(__file__)[0] + "/"  # use base directory for now
    js_code =  """$(document).ready( function() {
        $('#%s').fileTree({
          root: '%s',
          script: '%s',
          expandSpeed: -1,
          collapseSpeed: -1,
          multiFolder: false
        }, function(file) {
            document.getElementById('%s').value=file;
        });
    });
    """ % (tree_id, root, action, form_id)
    page.add_js_code(js_code)
    elem.text = title
    elem.attrib['class'] = "filetree_wrapper"

    form = SubElement(elem, 'form', name='url', size='80', method='get',
                       action=callback)
    SubElement(form, 'input', name='url', size='80', id=form_id)
    input_ = SubElement(form, 'input', type='submit',
                           value=label)
    input_.attrib['class'] = 'crunchy'

    file_div = SubElement(elem, 'div')
    file_div.attrib['id'] = tree_id
    file_div.attrib['class'] = "filetree_window"
    return


def save_file_request_handler(request):
    '''extracts the path & the file content from the request and
       saves the content in the path as indicated.'''
    if DEBUG:
        print("Entering save_file_request_handler.")
    data = request.data
    request.send_response(200)
    request.end_headers()
    # We've sent the file (content) and filename (path) in one
    # "document" written as path+"_::EOF::_"+content; the assumption
    # is that "_::EOF::_" would never be part of a filename/path.
    #
    # There could be more robust ways, like perhaps sending a string
    # containing the path length separated from the path and the content by
    # a separator where we check to make sure the path recreated
    # is of the correct length - but it probably would be an overkill.
    info = data.split("_::EOF::_")
    if DEBUG:
        print("info = ")
        print(info)
    path = info[0].decode("utf-8")
    try:
        path = path.encode(sys.getfilesystemencoding())
    except:
        print("   Could not encode path.")
    #path = info[0]
    # the following is in case "_::EOF::_" appeared in the file content
    content = '_::EOF::_'.join(info[1:])
    save_file(path, content)
    return path

def load_file_request_handler(request):
    ''' reads a local file - most likely a Python file that will
        be loaded in an EditArea embeded editor.'''
    if DEBUG:
        print("Entering load_file_request_handler.")
    try:
        content = read_file(request.args['path'])
    except:
        print("  Exception found.")
        print("  path = " + request.args['path'])
        return 404
    request.send_response(200)
    request.end_headers()
    request.wfile.write(content)
    request.wfile.flush()

def save_file(full_path, content):  # tested
    """saves a file
    """
    if DEBUG:
        print("Entering save_file.")
    #full_path = full_path.encode(sys.getfilesystemencoding)
    try:
        f = open(full_path, 'w')
        f.write(content)
        f.close()
    except:
        print("  Could not save file; full_path =")
        print(full_path)
    if DEBUG:
        print("Leaving save_file")

def read_file(full_path):  # tested
    """reads a file
    """
    if DEBUG:
        print("Entering read_file.")
    try:
        f = open(full_path)
        content = f.read()
    except:
        print("  Could not open file " + full_path)
        return None
    if DEBUG:
        print("  full_path in read_file = " + full_path)
    return content

def save_file_python_interpreter_request_handler(request):
    '''extracts the path & the file content from the request and
       saves the content in the path as indicated.'''
    if DEBUG:
        print("Entering save_file_python_interpreter_request_handler.")
    data = request.data
    request.send_response(200)
    request.end_headers()
    info = data.split("_::EOF::_")
    path = info[1]
    try:
        path = path.encode(sys.getfilesystemencoding())
    except:
        print("  Could not encode path.")

    content = '_::EOF::_'.join(info[2:])
    save_file(path, content)
    if DEBUG:
        print "info =", info
    return path
