from django.shortcuts import render
from .models import blog_post

# Create your views here.
def blog(request):
    news = blog_post.objects.all().order_by('-pub_date')
    return render(request, 'blog/blog.html', {
        'title': '<strong>Блог</strong>', 'news': news})