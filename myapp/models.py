from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# f:\PyCharm\django\my_project\myapp\models.py

# Article模型将页面中存储的这些文字转换成 SQL 语句
class Article(models.Model):
    # objects = None
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    likes = models.IntegerField('点赞数', default=0)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_at']  # 按创建时间倒序排列

    def __str__(self):
        return self.title

# 评论模型
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField('评论内容')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_at']  # 按创建时间正序排列

    def __str__(self):
        return f'{self.user.username} 评论了 {self.article.title}'