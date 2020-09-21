from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.urls import reverse

from . import util
import markdown2
import re
from random import randrange


class NewEntryForm(forms.Form): 
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def render_entry(request, title):
    entry = util.get_entry(title)
    if entry: 
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry),
            "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": "Entry Doesn't Exist",
            "message": "The page you are looking for does not exist. Please try another page. "
        }, status=404)

def search(request): 
    query = request.GET["q"]
    entry = util.get_entry(query)
    if entry: 
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(entry),
            "title": query
        })
    
    results = util.search_entries(query)
    return render(request, "encyclopedia/search_page.html", {
        "results": results,
        "query": query
    })

def create(request):
    if request.method == "POST": 
        form = NewEntryForm(request.POST)

        if form.is_valid(): 
            title = form.cleaned_data["title"]

            if util.get_entry(title): 
                return render(request, "encyclopedia/error.html", {
                    "title": "Entry Already Exist",
                    "message": "The entry you are trying to create already exist. please try something"
                }, status=404)

            content = form.cleaned_data["content"]
            util.save_entry(title, content)
        return HttpResponseRedirect(f"wiki/{title}")

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm
    })


def edit(request, title):
    content = util.get_entry(title)
    form = NewEntryForm(initial={'title':title, 'content':content })
    return render(request, "encyclopedia/edit.html", {
            "form": form
        })

def random(request): 
    entries = util.list_entries()
    length = len(entries)
    title = entries[randrange(length)]

    return HttpResponseRedirect(f"/wiki/{title}")
