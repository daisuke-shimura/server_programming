# サーバプログラミング演習「ラクタンナビ」

## 変更手順

### モデルの変更
   1. ターミナルで次のコマンドを実行（モデルの初期化）      
   `python manage.py migrate helloworld zero`  
   ※投稿したデータなどが削除されます！
   
   
   2. 色々削除
      - `djangosnippets/helloworld/migrations/0001_initial.py`を削除    
      - （`migrations`フォルダにある`__init__.py`以外すべて削除）    
      - `rm db.sqlite3`を実行
   
   
   3. `helloworld/models.py`に次のコードを追加
       <details>
       <summary>上部のformに追加</summary>
       
         ```python
              from django.conf import settings
              from django.db import models
              from django.contrib.auth.models import AbstractUser
              from django.core.validators import MinValueValidator, MaxValueValidator
         ```
      </details>

      <details>
      <summary>下部に追加</summary>
      
      ```python
      
           class User(AbstractUser):
                university = models.CharField(max_length=128, null=True, blank=True)
                school_year = models.PositiveIntegerField(null=True, blank=True)
                is_manager = models.BooleanField(default=False)
            
            
           class Lecture(models.Model):
                name = models.CharField(max_length=128)
                body = models.TextField()
                university = models.CharField(max_length=128)
                school_year = models.IntegerField()
                average_score = models.FloatField()
                reviews_count = models.IntegerField()
            
            
           class Review(models.Model):
                title = models.CharField(max_length=128)
                comment = models.TextField()
                score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
                lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
                user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
      
       ```
       </details>
   
   
   4. `djangisnippets/settings.py`最後に以下のコードを追加
       `AUTH_USER_MODEL = 'helloworld.User'`
   
   
   5. ターミナルで次のコマンドを実行  
      - `python manage.py makemigrations helloworld`
      - `python manage.py migrate`


## 追記
1. `.py`ファイル
   - `helloworld/model.py`   
     <details>
     <summary>コード</summary>
     
     ```python
     
        class User(AbstractUser):
            university = models.CharField(max_length=128, null=True, blank=True)
            school_year = models.PositiveIntegerField(null=True, blank=True)
            is_manager = models.BooleanField(default=False)
            def __str__(self):
                return self.username
        
        
        class Lecture(models.Model):
            name = models.CharField(max_length=128)
            body = models.TextField(null=True, blank=True)
            university = models.CharField(max_length=128, null=True, blank=True)
            school_year = models.IntegerField(null=True, blank=True)
            average_score = models.FloatField(null=True, blank=True)
            reviews_count = models.IntegerField(default=0, blank=True)
            def __str__(self):
                return self.name
        
        class Review(models.Model):
            title = models.CharField(max_length=128, null=True, blank=True)
            comment = models.TextField(null=True, blank=True)
            score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
            lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
            user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
            def __str__(self):
                return self.score
     ```
     
     </details>
     
     - コード追記後ターミナルで次のコマンドを実行  
        - `python manage.py makemigrations`
        - `python manage.py migrate`

   - `helloworld/forms.py`
     <details>
     <summary>コード</summary>
     
     ```python
     
        from django import forms
        from django import forms
        from helloworld.models import Helloworld, Lecture, Review
        from django.contrib.auth.forms import UserCreationForm
        from django.contrib.auth import get_user_model
        
        class SnippetForm(forms.ModelForm):
            class Meta:
                model = Helloworld
                fields = ('title', 'code', 'description')
        
        
        User = get_user_model()
        #ユーザ登録
        class CustomUserCreationForm(UserCreationForm):
            class Meta:
                model = User
                fields = ('username', 'email', 'school_year', 'university')
        
        #ユーザ編集
        class CustomUserEditForm(forms.ModelForm):
            class Meta:
                model = User
                fields = ['username', 'email', 'school_year', 'university']
        
        
        class ManagerForm(UserCreationForm):
            class Meta:
                model = User
                fields = ('username','email')
            def save(self, commit=True):
                user = super().save(commit=False)
                if commit:
                    user.save()
                    User.objects.create(user=user)
                return user
        
        
        class LectureForm(forms.ModelForm):
            class Meta:
                model = Lecture
                fields = ('name', 'body', 'university', 'school_year')
        
        
        class ReviewForm(forms.ModelForm):
            class Meta:
                model = Review
                fields = ('title', 'comment', 'score')
     ```
     </details>

   - `helloworld/views.py`
     <details>
     <summary>コード</summary>
     
     ```python
        from django.http import HttpResponse, HttpResponseForbidden
        from django.shortcuts import render, redirect, get_object_or_404
        from django.contrib.auth.decorators import login_required
        from helloworld.models import Helloworld, User, Lecture, Review
        from helloworld.forms import SnippetForm
        
        # Create your views here.
        def top(request):
            lectures = Lecture.objects.all()
            manager_exists = User.objects.filter(is_manager=True).exists()
            context = {
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
        
        #他のユーザの詳細
        def other_user(request, user_id):
            user = get_object_or_404(User, pk=user_id)
            context = {
                'user': user,
            }
            return render(request, 'snippets/users/_other_user.html', context)
        
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
            q_score = request.GET.get('q_score')
            search_score = int(q_score) if q_score is not None else ""
        
            if search_score:
                reviews = lecture.review_set.filter(score=search_score)
            else:
                reviews = lecture.review_set.all()
        
            score1_count = lecture.review_set.filter(score=1).count()
            score2_count = lecture.review_set.filter(score=2).count()
            score3_count = lecture.review_set.filter(score=3).count()
            score4_count = lecture.review_set.filter(score=4).count()
            score5_count = lecture.review_set.filter(score=5).count()
        
            score_counts = {
                5: score5_count,
                4: score4_count,
                3: score3_count,
                2: score2_count,
                1: score1_count,
            }
        
            valid_reviews = [review for review in reviews if review.title or review.comment]
        
            context = {
                'lecture': lecture,
                'reviews': reviews,
                'search_score': search_score,
                'score_counts': score_counts,
                'valid_reviews': valid_reviews,
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
        
        def lecture_delete(request, lecture_id):
            lecture = get_object_or_404(Lecture, pk=lecture_id)
            if request.method == 'POST':
                lecture.delete()
                return redirect('lectures_index')
            else:
                return redirect('lectures_index')
        
        
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
                    average = Review.objects.filter(lecture=lecture).aggregate(Avg('score'))['score__avg']
                    lecture.average_score = round(average, 2)
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
                lecture.reviews_count -= 1
                average = Review.objects.filter(lecture=lecture).aggregate(Avg('score'))['score__avg']
                lecture.average_score = round(average, 2)
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
     ```
     </details>

   - (`helloworld/urls.py`)
     <details>
     <summary>コード</summary>
     
     ```python
     
       from django.urls import path
       from helloworld import views
       from django.contrib.auth.views import LoginView, LogoutView
       from helloworld.views import signup_view, top
        
        urlpatterns = [
        #一般ユーザ
            path('', top, name='top'),
            path('new/', views.snippet_new, name='snippet_new'),
            path('<int:snippet_id>/', views.snippet_detail, name='snippet_detail'),
            path('<int:snippet_id>/edit/', views.snippet_edit, name='snippet_edit'),
            path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='snippets/login.html'), name='login'),
            path('logout/', LogoutView.as_view(), name='logout'),
            path('signup/', signup_view, name='signup'),
        
            #講義に関するページ（一覧, 詳細）
            path('lectures/', views.lecture_index, name='lectures_index'),
            path('lectures/<int:lecture_id>/', views.lecture_show, name='lectures_show'),
        
            #レビューに関するページ（作成、編集、削除）
            path('lectures/<int:lecture_id>/reviews/new/', views.review_new, name='reviews_new'),
            path('lectures/<int:lecture_id>/reviews/<int:review_id>/edit/', views.review_edit, name='reviews_edit'),
            path('lectures/<int:lecture_id>/reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),
        
            #ユーザに関するページ（マイページ, 編集, 他のユーザページ）
            path('users/<int:user_id>/', views.user_show, name='users_show'),
            path('users/<int:user_id>/edit/', views.user_edit, name='users_edit'),
            path('users/<int:user_id>/ajax/', views.other_user, name='other_user_ajax'),
        
        #管理者ページ
            path('manager/signup/', views.manager_signup, name='manager_signup'),
        
            #講義に関するページ（新規作成, 編集, 削除）
            path('manager/lectures/new/', views.lecture_new, name='lectures_new'),
            path('manager/lectures/<int:lecture_id>/edit/', views.lecture_edit, name='lectures_edit'),
            path('manager/lectures/<int:lecture_id>/delete/', views.lecture_delete, name='lectures_delete'),
        
            #ユーザに関するページ（一覧, 垢BAN）
            path('manager/users/', views.user_index, name='users_index'),
            path('users/<int:user_id>/active_switch/', views.user_active_switch, name='users_active_switch')
        ]

     ```
     </details>
    
   - ※(`helloworld/admins.py`)の下部に以下の3行を追記（まだなかったら）
     <details>
     <summary>コード</summary>
     
     ```python

        admin.site.register(User)
        admin.site.register(Lecture)
        admin.site.register(Review)

     ```
     </details>

2. HTMLファイル