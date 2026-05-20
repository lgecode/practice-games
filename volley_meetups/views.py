from django.shortcuts import render

from volley_meetups.services.playwright_fb import get_fb_posts


def index(request):
    """列出FB目前有的徵臨打貼文"""
    alive_fb_posts = get_fb_posts()
    print(alive_fb_posts)
    return render(request, "volley_meetups/index.html", {"posts": alive_fb_posts})
