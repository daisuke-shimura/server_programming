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

#会員に関すること
from django.contrib.auth import login
from .forms import CustomUserCreationForm
#新規登録
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

#ユーザ一覧
def user_index(request):
    users = User.objects.all()

    context = {
        'users': users,
    }
    return render(request, 'snippets/users/index.html', context)

#垢BAN
def user_active_switch(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('users_index')

#マイページ
def user_show(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    reviews = user.review_set.all()
    context = {
        'user': user,
        'reviews': reviews,
    }
    return render(request, 'snippets/users/show.html', context)

#会員情報編集
from .forms import CustomUserEditForm
def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_show', user_id=user_id)
    else:
        form = CustomUserEditForm(instance=user)
    return render(request, 'snippets/users/edit.html', {'form': form})


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
    search_name = request.GET.get('q_name') or "" # 検索キーワード
    search_year = request.GET.get('q_year') or ""
    search_university = request.GET.get('q_university') or ""
    sort = request.GET.get('sort')

    lectures = Lecture.objects.all()

    if search_name:
        lectures = lectures.filter(name__icontains=search_name)

    if search_year:
        lectures = lectures.filter(school_year=int(search_year))

    if search_university:
        lectures = lectures.filter(university__icontains=search_university)

    #並び替え
    if sort == 'review_count_desc':
        lectures = lectures.order_by('-reviews_count')  # レビュー高い順
    elif sort == 'review_count_asc':
        lectures = lectures.order_by('reviews_count')  # レビュー低い順
    elif sort == 'average_score_desc':
        lectures = lectures.order_by('-average_score')  # 評価高い順
    elif sort == 'average_score_asc':
        lectures = lectures.order_by('average_score')  # 評価低い順

    context = {
        'lectures': lectures,
        'search_name': search_name,
        'search_year': search_year,
        'search_university': search_university,
        'sort': sort,
    }
    return render(request, 'snippets/lectures/index.html', context)

def lecture_show(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    reviews = lecture.review_set.all()
    context = {
        'lecture': lecture,
        'reviews': reviews,
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
            average = Review.objects.filter(lecture=lecture).aggregate(Avg('score'))['score__avg']
            lecture.average_score = round(average, 2)
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
