from django.shortcuts import render
import markdown
import random
from . import util

def convert_to_html(entry):
    content = util.get_entry(entry)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })


def search(request):
    if request.method == "POST":
        search_result = request.POST["q"]
        convert_entry = convert_to_html(search_result)
        if convert_entry is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": search_result,
                "content": convert_entry
            })
        else:
            entries = util.list_entries()
            recommended = []
            for entry in entries:
                if search_result.lower() in entry.lower():
                    recommended.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entries": recommended
            })

        

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        in_entry = util.get_entry(title)
        if in_entry is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry already exists"
            })
        else:
            util.save_entry(title, content)
            convert_entry = convert_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": convert_entry
            })


def edit(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
        
        
def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        convert_entry = convert_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": convert_entry
        })
    
def rand(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    convert_entry = convert_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
            "title": random_entry,
            "content": convert_entry
    })
