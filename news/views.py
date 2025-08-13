from django.shortcuts import render, get_object_or_404
from .models import News
from news.models import News

def news_list(request):
    category = request.GET.get('category')
    if category:
        news_items = News.objects.filter(category=category).order_by('-date')
    else:
        news_items = News.objects.order_by('-date')
    return render(request, 'news/news_list.html', {'news_items': news_items})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.views += 1
    news.save(update_fields=['views'])
    return render(request, 'news/news_detail.html', {'news': news})

def index(request):
    news = News.objects.order_by('-date')[:9]  # последние 9 новостей
    return render(request, 'index.html', {'latest_news': news})
