from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.urls import reverse




class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()  # Utiliser RichTextField pour le contenu riche
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    @property
    def get_absolute_url(self):
        return reverse('article-details', kwargs={'slug': self.slug})
    
    @property
    def get_plain_text_content(self):
        return strip_tags(self.content)

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=True)
    
    likes_count = models.PositiveIntegerField(default=0)  # Compteur de "likes"
    unlikes_count = models.PositiveIntegerField(default=0)  # Compteur de "unlikes"

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'