
import os
import time
import thread

import sublime
import sublime_plugin
# todo:
# * fix lag
# * glob modules subfolder for languages and dynamically load - remove the current ugly hardcodedness

import sublimelint.modules.python as python

drawType = sublime.DRAW_EMPTY_AS_OVERWRITE | sublime.DRAW_OUTLINED
languages = [python]
lineMessages = {}
queue = {}

def run(linter, view):
    '''run a linter on a given view'''
    vid = view.id()

    text = view.substr(sublime.Region(0, view.size()))
    
    if view.file_name():
        filename = os.path.split(view.file_name())[-1]
    else:
        filename = 'untitled'
    
    underline, lines, errorMessages, clear_outlines = linter.run(text, view, filename)
    lineMessages[vid] = errorMessages

    erase_all_lint(view, clear_outlines)

    if underline:
        view.add_regions('lint-underline', underline, 'keyword', drawType)
    if lines:
        outlines = [view.full_line(view.text_point(lineno, 0)) for lineno in lines]
        view.add_regions('lint-outlines', outlines, 'keyword', drawType)
    
def erase_all_lint(view, clear_outlines):
    '''erase all "lint" error marks from view'''
    #view.erase_regions('lint-syntax')
    #view.erase_regions('lint-syntax-underline')
    view.erase_regions('lint-underline')
    if clear_outlines:
        view.erase_regions('lint-outlines')

def select_linter(view):
    '''selects the appropriate linter to use based on language in current view'''
    for module in languages:
        if module.language in view.settings().get("syntax"):
            return module
    return None

def run_linter(view):
    '''runs the appropriate linter on a given view'''
    linter = select_linter(view)
    if linter is not None:
        run(linter, view)

def queue_linter(view):
    '''Put the current view in a queue to be examined by a linter
       if it exists'''
    if select_linter(view) is None:
        erase_all_lint(view)# may have changed file type and left marks behind
        return
    queue[view.id()] = view

def background_linter():
    '''An infinite loop meant to periodically
       update the view after running the linter in a background thread
       so as to not slow down the UI too much.'''
    while True:
        time.sleep(0.5)
        for vid in dict(queue):
            _view = queue[vid]
            def _update_view():
                try:
                    run_linter(_view)
                except RuntimeError, excp:
                    print excp
            sublime.set_timeout(_update_view, 100)
            try: 
                del queue[vid]
            except: 
                pass

thread.start_new_thread(background_linter, ())

class pyflakes(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        sublime_plugin.EventListener.__init__(self, *args, **kwargs)
        self.lastCount = {}
    
    def on_modified(self, view):
        queue_linter(view)
        return
    
    def on_load(self, view):
        queue_linter(view)
    
    def on_post_save(self, view):
        queue_linter(view)
    
    def on_selection_modified(self, view):
        vid = view.id()
        lineno = view.rowcol(view.sel()[0].end())[0]
        if vid in lineMessages and lineno in lineMessages[vid]:
            view.set_status('pyflakes', '; '.join(lineMessages[vid][lineno]))
        else:
            view.erase_status('pyflakes')
