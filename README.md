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


### その他の追記
1. `.py`ファイル
   - `helloworld/urls.py`
   - `helloworld/forms.py`
   - `helloworld/views.py`
   - (`helloworld/admins.py`)
2. HTMLファイル