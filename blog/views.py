from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import get_object_or_404
from .models import PostModel
from .forms import PostModelForm


def post_model_list_view(request):
    qs = PostModel.objects.all()

    template = "blog/list-view.html"
    context = {
        "object_list": qs,
    }
    return render(request, template, context)


def post_model_create_view(request):
    template = "blog/create-view.html"
    form = PostModelForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        context = {
            "form": PostModelForm()
        }
    return render(request, template, context)


def post_model_update_view(request, id=None):
    template = "blog/update-view.html"
    post = get_object_or_404(PostModel, id=id)
    if request.method == "POST":
        form = PostModelForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:detail', args=(id)))
    else:
        form = PostModelForm(instance=post)

    context = {
        "form": form,
        "post": post,
        "post_id": id,
    }

    return render(request, template, context)


def post_model_detail_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    context = {"object": obj, }
    template = "blog/detail-view.html"
    return render(request, template, context)


def post_model_delete_view(request, id=None):
    template = "blog/delete-view.html"
    post = get_object_or_404(PostModel, id=id)

    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse('blog:list'))

    context = {
        "post_id": id,
        "post": post
    }
    return render(request, template, context)
