from django.core.management.base import BaseCommand
from helloworld.models import User, Lecture, Review
from django.utils.crypto import get_random_string
import random

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        users = User.objects.all()
        lectures = Lecture.objects.get(id=1)

        # Userを作成
        '''
        User.objects.create_user(
            username='円堂 守',
            email='endo@example.com',
            password='pass1234',
            university='雷門中',
            school_year=2,
            is_manager=False
        )
        User.objects.create_user(
            username='豪炎寺 修也',
            email='gouenzi@example.com',
            password='pass1234',
            university='雷門中',
            school_year=2,
            is_manager=False
        )
        User.objects.create_user(
            username='吹雪 士郎',
            email='hubuki@example.com',
            password='pass1234',
            university='白恋中',
            school_year=2,
            is_manager=False
        )
        User.objects.create_user(
            username='鬼道 有人',
            email='kidou@example.com',
            password='pass1234',
            university='帝国学園',
            school_year=2,
            is_manager=False
        )
        User.objects.create_user(
            username='風丸 一朗太',
            email='kazemaru@example.com',
            password='pass1234',
            university='雷門中',
            school_year=2,
            is_manager=False
        )
        User.objects.create_user(
            username='壁山 塀五郎',
            email='kabeyama@example.com',
            password='pass1234',
            university='雷門中',
            school_year=1,
            is_manager=False
        )
        User.objects.create_user(
            username='栗松 鉄平',
            email='kurimatu@example.com',
            password='pass1234',
            university='雷門中',
            school_year=1,
            is_manager=False
        )
        User.objects.create_user(
            username='染岡 竜吾',
            email='someoka@example.com',
            password='pass1234',
            university='雷門中',
            school_year=2,
            is_manager=False
        )
        User.objects.create_user(
            username='三国 太一',
            email='sangoku@example.com',
            password='pass1234',
            university='雷門中',
            school_year=3,
            is_manager=False
        )
        User.objects.create_user(
            username='アフロディ',
            email='ahuro@example.com',
            password='pass1234',
            university='世宇子中',
            school_year=2,
            is_manager=False
        )
        '''

        # Lectureを作成
        '''
        Lecture.objects.create(
            name='算数',
            body='足し算や引き算、掛け算などの基礎的な計算を学びます。',
            university='雷門中',
            school_year=1
        )
        Lecture.objects.create(
            name='国語',
            body='物語文や説明文を読んで、登場人物の気持ちや内容を読み取る練習をします。',
            university='雷門中',
            school_year=1
        )
        Lecture.objects.create(
            name='理科',
            body='植物の成長や昆虫の観察など、自然の不思議について学びます。',
            university='雷門中',
            school_year=2
        )
        Lecture.objects.create(
            name='社会',
            body='地域の産業や交通について学び、日本の地理の基本を理解します。',
            university='雷門中',
            school_year=3
        )
        Lecture.objects.create(
            name='英語',
            body='英語のあいさつや基本的な単語を使って簡単な表現を練習します。',
            university='雷門中',
            school_year=2
        )
        Lecture.objects.create(
            name='音楽',
            body='リコーダーや鍵盤ハーモニカの演奏を通して、音楽の楽しさを体験します。',
            university='雷門中',
            school_year=1
        )
        Lecture.objects.create(
            name='図工',
            body='紙や粘土を使って自由な発想で作品を作ります。創造力を養います。',
            university='雷門中',
            school_year=2
        )
        Lecture.objects.create(
            name='数学',
            body='方程式や関数、図形の証明などを通して論理的思考力を育てます。',
            university='帝国学園',
            school_year=3
        )
        Lecture.objects.create(
            name='物理',
            body='運動の法則やエネルギー保存則を学び、実験を通して理解を深めます。',
            university='帝国学園',
            school_year=3
        )
        Lecture.objects.create(
            name='歴史',
            body='縄文時代から現代までの日本の歴史を学び、出来事の背景や人々の暮らしを理解します。',
            university='世宇子中',
            school_year=3
        )
        '''

        Review.objects.create(
            title='楽しい',
            comment='おかし食べても怒られない',
            score=5,
            lecture=lectures,
            user=random.choice(users),
        )
        for _ in range(30):  # 30件作成
            Review.objects.create(
                title=get_random_string(10),
                comment="これはサンプルレビューです。" + get_random_string(20),
                score=random.randint(1, 5),
                lecture=lectures,
                user=random.choice(users),
            )
