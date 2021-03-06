# -*- coding: utf-8 -*-
"""Dynamically generate html for markdown files"""
from django.shortcuts import render
from django.http import HttpResponse
import markdown
import glob
import platform


MD_ROOT = "classnotes_browser/static/classnotes_browser/md_src/"
MD_SHORT_ROOT = "classnotes_browser/md_src/"
separator = "/" if platform.system() != "Windows" else "\\"


def chunker(seq, size):
    """chunker"""
    return [seq[pos:pos + size] for pos in range(0, len(seq), size)]


def homepage(request):
    """renders homepage"""
    print(glob.glob("{}*/".format(MD_ROOT)))
    subjects_available = [
        i.split(separator)[-2] for i in glob.glob("{}*/".format(MD_ROOT))
        ]
    subjects_available = chunker(subjects_available, 3)
    print(subjects_available)
    return render(request, "classnotes_browser/homepage.html", {"subj_list": subjects_available})


def render_md(request, cours, name):
    """renders markdown in html"""
    with open("{}{}/{}.md".format(MD_ROOT, cours, name)) as f:
        md_input = f.read()
        html_output = markdown.markdown(md_input)
    return render(request, "classnotes_browser/md_display.html", {"title": name, "md_in": html_output})


def cours_dir(request, subject):
    """generate links to markdown files"""
    cours_available = chunker(
        [i.split(separator)[-1].split(".")[0] for i in glob.glob("{}/{}/*".format(MD_ROOT, subject)) if "." in i],
        3
    )
    return render(
        request,
        "classnotes_browser/cours_list.html",
        {
            "title": subject, "cours_list": [[
                {
                    "name": name.replace("_", " "), "link": name
                } for name in triplet] for triplet in cours_available
            ]
        }
    )
