from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class Author(models.Model):  # Модель, содержащая объекты всех авторов.
    author_rating = models.IntegerField(default = 0)  # рейтинг пользователя
    user = models.OneToOneField(User, on_delete=models.CASCADE)# cвязь «один к одному» с встроенной моделью пользователей User;

    def update_rating(self) -> int:  # обновляет рейтинг текущего автора
        aut_post_rat = Post.objects.filter(author_id = self.id).aggregate(Sum('post_rating'))['post_rating__sum'] * 3   # суммарный рейтинг каждой статьи автора умножается на 3
        aut_com_rat = Comment.objects.filter(user_id = self.user_id).aggregate(Sum('comment_rating'))['comment_rating__sum']  # суммарный рейтинг всех комментариев автора
        post_com_rat = Comment.objects.filter(post__author_id=self.id).aggregate(Sum('comment_rating'))['comment_rating__sum']  # суммарный рейтинг всех комментариев к статьям автора.
        self.author_rating = aut_com_rat + aut_post_rat + post_com_rat
        self.save()


class Category(models.Model):  # Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
    category_name = models.CharField(max_length=64, unique=True)  #  Название категории
    subscribers = models.ManyToManyField(User, blank=True, through='CategorySubscribe')

    def __str__(self) -> str:
        return self.category_name
    

news = 'n'
article = 'a'
cat = [(news, 'Новость'), (article, 'Статья')]


class Post(models.Model):  # модель содержит в себе статьи и новости, которые создают пользователи
    post_header = models.CharField(max_length=64)  # заголовок статьи/новости
    post_text = models.TextField()  # текст статьи/новости
    post_rating = models.IntegerField(default=0)  # рейтинг статьи/новости
    post_type = models.CharField(max_length=1, choices=cat, default=news)  # поле с выбором — «статья» или «новость»;
    post_datetime = models.DateTimeField(auto_now_add=True)  # автоматически добавляемая дата и время создания;
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Author;
    category = models.ManyToManyField(Category, through='PostCategory')  # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);

    def __str__(self) -> str:
        return f'{self.post_datetime}' \
        f'{self.post_header}' \
        f'{self.post_text}'

    def like(self) -> int:  # увеличивает рейтинг на единицу.
        self.post_rating += 1
        self.save()
    
    def dislike(self) -> int:  # уменьша tт рейтинг на единицу.
        self.post_rating -= 1
        self.save()
    
    def preview(self) -> str:  # возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце
        if len(self.post_text) <= 127:
            return self.post_text
        return f'{self.post_text[:124]}...'
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):  # Промежуточная модель для связи «многие ко многим»
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post;
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Category.


class CategorySubscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribe = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):  # Иодель комментариев
    comment_text = models.CharField(max_length=255)  # текст комментария
    comment_datetime = models.DateTimeField(auto_now_add=True) # дата и время создания комментария;
    comment_rating = models.IntegerField(default=0)  # рейтинг комментария
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # связь «один ко многим» с моделью Post;
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);

    def like(self) -> int:  # увеличивает рейтинг на единицу.
        self.comment_rating += 1
        self.save()
    
    def dislike(self) -> int:  # уменьша tт рейтинг на единицу.
        self.comment_rating -= 1
        self.save()
