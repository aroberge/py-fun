
# Create your views here.
from crunchy_wiki.wiki.models import Page
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms

from src import transform

class SearchForm(forms.Form):
    text = forms.CharField(label="Enter search Term")
    search_content = forms.BooleanField(label="Search content", required=False)

def search_page(request):
    if request.method == "POST":
        pages = []
        contents = []
        nothing = []
        f = SearchForm(request.POST)
        if not f.is_valid():
            return render_to_response("search.html", {"form": f})
        else:
            if f.cleaned_data["text"] == "*":
                pages = transform.linkify_list(Page.objects.filter())
            else:
                pages = transform.linkify_list(Page.objects.filter(
                                       name__contains = f.cleaned_data["text"]))
                if f.cleaned_data["search_content"]:
                    contents = transform.linkify_list(Page.objects.filter(
                                    content__contains = f.cleaned_data["text"]))

            if not (contents or pages):
                nothing = ['dummy value']
            return render_to_response("search.html",
                                      {"form": f, "pages": pages,
                                       "contents": contents, "nothing": nothing})
    f = SearchForm()
    return render_to_response("search.html", {"form": f})

special_pages = {"SearchPage": search_page}

def view_page(request, page_name):
    if page_name in special_pages:
        return special_pages[page_name](request)
    try:
        page = Page.objects.get(pk=page_name)
    except Page.DoesNotExist:
        return render_to_response("create.html", {"page_name": page_name})

    content = transform.to_html(page.content, page_name)

    return render_to_response("view.html", {"page_name": page_name,
                                            "content": content})

def edit_page(request, page_name):
    try:
        page = Page.objects.get(pk=page_name)
        content = page.content
    except Page.DoesNotExist:
        content = ''
    return render_to_response("edit.html", {"page_name": page_name,
                                                "content": content})

def save_page(request, page_name):
    content = request.POST["content"]
    try:
        page = Page.objects.get(pk=page_name)
        page.content = content
    except Page.DoesNotExist:
        page = Page(name=page_name, content=content)
    page.save()
    return HttpResponseRedirect("/%s/" % page_name)

def delete_page(request, page_name):
    try:
        page = Page.objects.get(pk=page_name)
        page.delete()
    except Page.DoesNotExist:
        page = Page(name=page_name, content=content)
    return HttpResponseRedirect("/%s/" % page_name)