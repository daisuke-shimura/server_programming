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
               university = models.CharField(max_length=128)
               school_year = models.PositiveIntegerField()
           
           
           class Manager(models.Model):
               user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
           
           
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


### ユーザー登録
1. `helloworld/urls.py`を編集
   - 上部のformに     
   `from helloworld.views import signup_view`    
   を追加
   - signupのpathを      
   `path('signup/', signup_view, name='signup'),`       
   に変更
2. `helloworld/forms.py`を編集
   - 上部のformに     
   `from django.contrib.auth.forms import UserCreationForm`       
   `from django.contrib.auth import get_user_model`
   の二つを追加
   - 下部に以下を追記
   ```python
   User = get_user_model()
      class CustomUserCreationForm(UserCreationForm):
          class Meta:
              model = User
              fields = ('username', 'email', 'school_year')
   ```
3. `helloworld/views.py`を編集
   - 以下の記述を下部に追加
   ```python
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
   ```
