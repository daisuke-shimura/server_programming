from django.urls import path
from helloworld import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from helloworld.views import signup_view, top
#CustomLoginView
#from helloworld.views import

urlpatterns = [
#一般ユーザ
    path('', top, name='top'),
    path('new/', views.snippet_new, name='snippet_new'),
    path('<int:snippet_id>/', views.snippet_detail, name='snippet_detail'),
    path('<int:snippet_id>/edit/', views.snippet_edit, name='snippet_edit'),
    #path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='snippets/login.html'), name='login'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='snippets/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('signup/', CreateView.as_view(template_name='snippets/signup.html',form_class=CustomUserCreationForm, success_url='/'), name='signup'),
    path('signup/', signup_view, name='signup'),

    #講義に関するページ（一覧, 詳細）
    path('lectures/', views.lecture_index, name='lectures_index'),
    path('lectures/<int:lecture_id>', views.lecture_show, name='lectures_show'),

    #レビューに関するページ（作成、編集、削除）
    path('lectures/<int:lecture_id>/reviews/new', views.review_new, name='reviews_new'),
    path('lectures/<int:lecture_id>/reviews/<int:review_id>/edit', views.review_edit, name='reviews_edit'),
    path('lectures/<int:lecture_id>/reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),

#管理者ページ
    path('manager/signup', views.manager_signup, name='manager_signup'),

    #講義に関するページ（新規作成, 編集）
    path('manager/lectures/new', views.lecture_new, name='lectures_new'),
    path('manager/lectures/<int:lecture_id>/edit', views.lecture_edit, name='lectures_edit'),

]