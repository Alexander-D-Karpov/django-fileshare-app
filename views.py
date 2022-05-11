from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .services.delete_file import del_file
from .services.file_upload import file_upload
from .services.get_file import get_file
from .services.get_file_list import get_file_list
from .services.get_groups_list import get_group_list


def file_list(request):
    if request.method == "POST":
        file_upload(request.FILES.getlist("file"), request.user, request.POST["name"], request.POST["description"])
        return redirect("file.index")
    elif request.method == "GET":
        if request.user.is_authenticated:
            groups = get_group_list(request.user)
            files = get_file_list(request.user)
        else:
            groups = get_group_list()
            files = get_file_list()

        p = Paginator(files, 19)
        page_number = request.GET.get("page")
        try:
            files = p.get_page(page_number)
        except PageNotAnInteger:
            files = p.page(1)
        except EmptyPage:
            files = p.page(p.num_pages)

        return render(
            request,
            "file/index.html",
            context={"files": files, "p": p, "groups": groups},
        )


def view_file(request, slug):
    # if "Bot" in request.headers["User-Agent"]:
    #    file = get_file(slug)["file"]
    #    return HttpResponse(open(file.file.path, "rb"), content_type=file.type)

    if request.user.is_authenticated:
        return render(
            request,
            "file/file_view.html",
            context=get_file(slug, request.user),
        )
    return render(
        request,
        "file/file_view.html",
        context=get_file(slug),
    )


def delete_file(request, slug):
    if request.user.is_authenticated:
        del_file(slug, request.user)
    return redirect("file.index")


def group(request, slug):
    if request.method == "POST":
        file_upload(request.FILES.getlist("file"), request.user, request.POST["name"], request.POST["description"], slug)
        return redirect("file_group", slug)
    elif request.method == "GET":
        files = get_file_list(group_slug=slug)

        p = Paginator(files, 19)
        page_number = request.GET.get("page")
        try:
            files = p.get_page(page_number)
        except PageNotAnInteger:
            files = p.page(1)
        except EmptyPage:
            files = p.page(p.num_pages)

        return render(
            request,
            "file/index.html",
            context={"files": files, "p": p},
        )
