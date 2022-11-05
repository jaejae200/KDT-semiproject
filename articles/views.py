from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from django.core.paginator import Paginator

# Create your views here.

@require_safe
def index(request):
    page = request.GET.get('page', '1')
    articles = Article.objects.order_by('-pk')
    paginator = Paginator(articles, 6)
    page_obj = paginator.get_page(page)
    context = {
        'articles': articles, 
        'articles_list' : page_obj,
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user 
            article.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('articles:index')
    else: 
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context=context)

def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': article.comment_set.all(),
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)

@login_required
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user: 
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                messages.success(request, '글이 수정되었습니다.')
                return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        messages.warning(request, '작성자만 수정할 수 있습니다.')
        return redirect('articles:detail', article.pk)

@login_required
def delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('articles:index')

@login_required
def comment_create(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        context = {
            'content': comment.content,
            'userName': comment.user.username
        }
        return JsonResponse(context)

def comment_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()

    return redirect('articles:detail', article_pk)

    

@login_required
def like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user in article.like_users.all(): 
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    context = {'isLiked': is_liked, 'likeCount': article.like_users.count()}
    return JsonResponse(context)