from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Article, Comment
from .forms import ArticleForm, CommentForm
from django.db.models import Q

# Create your views here.


def home(request):
    articles = Article.objects.all()
    return render(request, 'templates/home.html', {'articles': articles})


def article_detail(request, pk):
    # Retrieve the article from the database based on its primary key (pk) in the URL, or return a 404 error if not found
    article = get_object_or_404(Article, pk=pk)

    # Retrieve all comments associated with the article
    comments = article.comments.all()

    if request.method == 'POST':
        # If the request method is POST (i.e., the user has submitted a form), create a new comment
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a new comment object from the form data, but don't save it to the database yet (commit=False)
            comment = form.save(commit=False)

            # Set the article and author fields of the comment to the current article and user, respectively
            comment.article = article
            comment.author = request.user

            # Save the comment to the database
            comment.save()

            # Display a success message to the user
            messages.success(request, 'Your comment has been added!')

            # Redirect the user back to the article detail page (to avoid form resubmission on page refresh)
            return redirect('article_detail', pk=pk)
    else:
        # If the request method is not POST (i.e., the user is just viewing the page), create a new, empty comment form
        form = CommentForm()

    # Render the article detail template, passing in the article, comments, and comment form as context variables
    return render(request, 'templates/article_detail.html', {'article': article, 'comments': comments, 'form': form})


def articles_by_category(request, category_pk):
    # Get the category with the matching primary key (category_pk) from the database, or return a 404 error if it doesn't exist
    category = get_object_or_404(Category, pk=category_pk)

    # Get all articles associated with this category
    articles = category.articles.all()

    # Render the articles_by_category template, passing in the category and articles as context variables
    return render(request, 'templates/articles_by_category.html', {'category': category, 'articles': articles})


@login_required
def create_article(request):
    if request.method == 'POST':
        # Get form data and validate
        form = ArticleForm(request.POST)
        if form.is_valid():
            # Create article with the current user as the author
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            # Save many-to-many relationships
            form.save_m2m()
            # Display success message and redirect to newly created article detail page
            messages.success(request, 'Your article has been created!')
            return redirect('article_detail', pk=article.pk)
    else:
        # Empty form for creating a new article
        form = ArticleForm()
    return render(request, 'templates/create_article.html', {'form': form})


@login_required
def edit_article(request, pk):
    # Get the article to be edited
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        # Get form data and validate
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            # Update article with the current user as the author
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            # Save many-to-many relationships
            form.save_m2m()
            # Display success message and redirect to edited article detail page
            messages.success(request, 'Your article has been updated!')
            return redirect('article_detail', pk=article.pk)
    else:
        # Pre-populate form with the information of the article to be edited
        form = ArticleForm(instance=article)
    return render(request, 'templates/edit_article.html', {'form': form})


@login_required
def delete_article(request, pk):
    # Get the article to be deleted
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.author:
        # If the user is the author, delete the article and display a success message
        article.delete()
        messages.success(request, 'Your article has been deleted!')
    else:
        # If the user does not have permission, display an error message
        messages.error(request, 'You do not have permission to delete this')


def search_articles(request):
    query = request.GET.get('q')
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query))
    else:
        articles = Article.objects.none()
    return render(request, 'templates/search.html', {'articles': articles, 'query': query})
