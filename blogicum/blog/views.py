from datetime import datetime

from django.shortcuts import get_object_or_404, render

from .models import Category, Post

NUMBER_OF_POSTS = 5


def get_post():
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )


def index(request):
    template_name = 'blog/index.html'
    context = {'post_list': get_post()[:NUMBER_OF_POSTS]}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(get_post(), id=post_id)
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_post().filter(category=category)
    context = {'category': category,
               'post_list': post_list}
    return render(request, template_name, context)
