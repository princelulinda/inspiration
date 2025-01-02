from django.shortcuts import render
from .models import Article, Tag
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Article, Comment
from .forms import CommentForm
# Create your views here.


def details(request, slug): 
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.filter(approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            
            return redirect(reverse('article-details', kwargs={'slug': article.slug}))
    else:
        form = CommentForm()
    
    context = {
        "title": "Details",
        "article": article,
        'comments': comments,
        'form': form
    }
    return render(request, 'core/details.html', context)

def tag_details(request, slug):
    tag = Tag.objects.get(slug=slug)
    articles = Article.objects.filter(tags=tag)
    tags = Tag.objects.all()
    
    context = {
        'tag_n': tag,
        'articles': articles,
        'tags': tags
    }
    return render(request, 'core/tag-details.html', context)

def get_articles(request, slug):
    tag = Tag.objects.get(slug=slug)
    articles = Article.objects.filter(tags=tag)

    articles_data = [
        {
            'title': article.title,
            'slug': article.slug,
            'image': article.image.url,
            'contentSnippet': article.get_plain_text_content()[:100]  # Adjust snippet length as needed
        }
        for article in articles
    ]

    return JsonResponse({'articles': articles_data})

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    session_key = f'comment_{comment_id}_liked'

    # Vérifier si l'utilisateur a déjà liké ce commentaire
    if not request.session.get(session_key, False):
        comment.likes_count += 1
        comment.save()
        request.session[session_key] = True  # Marquer comme liké dans la session

    return redirect(request.META.get('HTTP_REFERER', 'article-details'))

def unlike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    session_key = f'comment_{comment_id}_unliked'

    # Vérifier si l'utilisateur a déjà unliké ce commentaire
    if not request.session.get(session_key, False):
        comment.unlikes_count += 1
        comment.save()
        request.session[session_key] = True  # Marquer comme unliké dans la session

    return redirect(request.META.get('HTTP_REFERER', 'article-details'))