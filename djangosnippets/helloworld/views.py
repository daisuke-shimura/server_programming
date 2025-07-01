from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from helloworld.models import Helloworld
from helloworld.forms import SnippetForm

# Create your views here.
def top(request):
    snippets = Helloworld.objects.all()
    context = {'snippets':snippets}
    return render(request, 'snippets/top.html', context)

@login_required  # このデコレータのある機能はログインが必要
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:
        form = SnippetForm()
    return render(request, 'snippets/snippet_new.html', {'form': form})


@login_required  # このデコレータのある機能はログインが必要
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Helloworld, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden('このスニペットの編集は許可されていません．')
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippet_detail', snippet_id=snippet_id)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, 'snippets/snippet_edit.html', {'form': form})


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Helloworld, pk=snippet_id)
    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})


from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 自動ログイン
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'snippets/signup.html', {'form': form})
