
import sys

from django.template.loader import render_to_string

def save_hard_copy(file_name, template, _dict):
    sys.stderr.write(render_to_string(template, _dict))