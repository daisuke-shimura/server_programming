from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from helloworld.models import Helloworld, User, Lecture, Review
from helloworld.forms import SnippetForm

# Create your views here.
def top(request):
    #snippets = Helloworld.objects.all()
    lectures = Lecture.objects.all()
    manager_exists = User.objects.filter(is_manager=True).exists()
    context = {
        #'snippets': snippets,
        'lectures': lectures,
        'manager_exists': manager_exists,
    }
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
            return redirect('lectures_index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'snippets/signup.html', {'form': form})


#管理人新規登録
from .forms import ManagerForm
def manager_signup(request):
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_manager = True
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = ManagerForm()
    return render(request, 'snippets/manager/signup.html', {'form': form})


#講義
from .forms import LectureForm
def lecture_new(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.save()
            return redirect('/lectures/')
    else:
        form = LectureForm()
    return render(request, 'snippets/lectures/new.html', {'form': form})


def lecture_index(request):
    #lectures = Lecture.objects.all()
    search = request.GET.get('q')  # 検索キーワード
    if search:
        lectures = Lecture.objects.filter(name__icontains=search)
    else:
        lectures = Lecture.objects.all()
    context = {
        'lectures': lectures,
        'search': search,
    }
    return render(request, 'snippets/lectures/index.html', context)

def lecture_show(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    reviews = lecture.review_set.all()
    context = {
        'lecture': lecture,
        'reviews': reviews
    }
    return render(request, 'snippets/lectures/show.html', context)

def lecture_edit(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    #if lecture.created_by_id != request.user.id:
        #return HttpResponseForbidden('このスニペットの編集は許可されていません．')
    if request.method == 'POST':
        form = LectureForm(request.POST, instance=lecture)
        if form.is_valid():
            form.save()
            return redirect('lectures_show', lecture_id=lecture_id)
    else:
        form = LectureForm(instance=lecture)
    return render(request, 'snippets/lectures/edit.html', {'form': form})


#レビュー
from .forms import ReviewForm
from django.db.models import Avg
def review_new(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.lecture = lecture
            review.user = request.user
            review.save()
            lecture.reviews_count += 1
            lecture.average_score = Review.objects.filter(lecture=lecture).aggregate(Avg('score'))['score__avg']
            lecture.save()
            return redirect('lectures_show', lecture_id=lecture.id)
    else:
        form = ReviewForm()
    return render(request, 'snippets/reviews/new.html', {'form': form})

def review_edit(request, lecture_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    lecture = get_object_or_404(Lecture, id=lecture_id)
    #if review.created_by_id != request.user.id:
        #return HttpResponseForbidden('このスニペットの編集は許可されていません．')
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            lecture.average_score = Review.objects.filter(lecture=lecture).aggregate(Avg('score'))['score__avg']
            lecture.save()
            return redirect('lectures_show', lecture_id=lecture_id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'snippets/reviews/edit.html', {'form': form})

def review_delete(request, lecture_id, review_id):
    review = get_object_or_404(Review, pk=review_id)
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if request.method == 'POST':
        review.delete()
        lecture.average_score = Review.objects.filter(lecture=lecture).aggregate(Avg('score'))['score__avg']
        lecture.save()
        return redirect('lectures_show', lecture_id=lecture_id)
    else:
        return redirect('lectures_show', lecture_id=lecture_id)

#ログイン後の管理者判別
'''
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        print("manager変数:", user.is_manager)
        if user.is_manager:
            return '/'  # 管理者用ページへ
        else:
            return '/'  # 一般ユーザー用ページへ
'''
