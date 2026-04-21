from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# f:\PyCharm\django\my_project\myapp\views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Article, Comment

def article_list(request):
    """文章列表"""
    # 处理搜索
    search_query = request.GET.get('q', '')
    if search_query:
        articles = Article.objects.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
    else:
        articles = Article.objects.all()
    
    # 分页
    paginator = Paginator(articles, 5)  # 每页显示5篇文章
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'myapp/article_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

def article_detail(request, pk):
    """详情页：显示单篇文章和评论"""
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()  # 获取文章的所有评论
    return render(request, 'myapp/article_detail.html', {'article': article, 'comments': comments})

@login_required
def add_comment(request, pk):
    """添加评论"""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        content = request.POST['content']
        Comment.objects.create(
            article=article,
            user=request.user,
            content=content
        )
    return redirect('article_detail', pk=article.pk)

def like_article(request, pk):
    """点赞文章"""
    article = get_object_or_404(Article, pk=pk)
    
    # 检查用户是否已经点赞过
    liked_articles = request.session.get('liked_articles', [])
    if pk not in liked_articles:
        # 增加点赞数
        article.likes += 1
        article.save()
        # 记录用户已经点赞过
        liked_articles.append(pk)
        request.session['liked_articles'] = liked_articles
    
    return redirect('article_detail', pk=article.pk)

@login_required
def create_article(request):
    """创建文章"""
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Article.objects.create(title=title, content=content)
        return redirect('article_list')
    return render(request, 'myapp/create_article.html')

@login_required
def edit_article(request, pk):
    """编辑文章"""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        article.title = title
        article.content = content
        article.save()
        return redirect('article_detail', pk=article.pk)
    return render(request, 'myapp/edit_article.html', {'article': article})

@login_required
def delete_article(request, pk):
    """删除文章"""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'myapp/delete_article.html', {'article': article})

def register(request):
    """用户注册"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def user_login(request):
    """用户登录"""
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('article_list')
        else:
            error_message = '用户名或密码错误'
    return render(request, 'myapp/login.html', {'error_message': error_message})

def user_logout(request):
    """用户退出"""
    logout(request)
    return redirect('article_list')