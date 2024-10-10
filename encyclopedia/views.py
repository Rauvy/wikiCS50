from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django import forms
from django.urls import reverse
import random
import markdown2

from . import util


class NewSearchForm(forms.Form):
    search = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, entry):
    markdown_content = util.get_entry(entry)
    if markdown_content:
        html_content = markdown2.markdown(markdown_content)  
        return render(request, "encyclopedia/display_entry.html", {
            "entry": entry,
            "html_content": html_content  
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested entry does not exist."
        })


def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        try:
            util.save_entry(title, content, edit=False)
            return HttpResponseRedirect(reverse("get_entry", args=[title]))
        except FileExistsError:
            return render(request, "encyclopedia/error.html", {
                'message' : "An entry with this title already exists. Please choose a different title." 
            })
    return render(request, "encyclopedia/new_page.html")
        

def get_random_entry(request):
    entries = util.list_entries()
    if entries:
        random_entry = random.choice(entries)
        return redirect('get_entry', entry=random_entry)
    else:
        return render(request, "encyclopedia/index.html")


def search(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)

        if form.is_valid():
            search_query = form.cleaned_data["search"]
            html_content = util.get_entry(search_query)

            if html_content:
                return redirect(reverse('get_entry', args=[search_query]))
            else:
                all_entries = util.list_entries()
                matching_entries = [entry for entry in all_entries if search_query.lower() in entry.lower()]

                if matching_entries:
                    return render(request, "encyclopedia/search_results.html", {
                        'search_query' : search_query,
                        'matching_entries' : matching_entries
                    })
                else:
                    return render(request, "encyclopedia/display_entry.html", {
                        'entry' : search_query,
                        'html_content' : None,
                        'error_message' : "The requested entry does not exist"
                    })
    else:
        form = NewSearchForm()

    return render(request, "index.html", {'form' : form})


def edit_entry(request, entry):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(entry, content, edit=True) 

        return HttpResponseRedirect(reverse("get_entry", args=[entry]))

    entry_content = util.get_entry(entry)  
    return render(request, "encyclopedia/edit_entry.html", {
        "entry": entry,
        "content": entry_content  
    })
