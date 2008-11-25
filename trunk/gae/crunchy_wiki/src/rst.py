# Author: Andre Roberge <andre.roberge@gmail.com>
# Copyright: This module has been placed in the public domain.

from docutils import core, io

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
