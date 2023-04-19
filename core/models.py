from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.manager import CustomUserManager

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    edited_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):
    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []

    username = None
    first_name = None
    last_name = None

    login = models.CharField(max_length=16, verbose_name="Логин", unique=True)
    password = models.CharField(max_length=128, verbose_name="Пароль")
    phone = models.CharField(max_length=16, verbose_name="№ телефона")
    email = models.EmailField()
    birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    objects = CustomUserManager()


    def __str__(self):
        return self.login

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Post(BaseModel):
    def get_file_name(self, file_name):
        return f'post_photos/{self.pk}_{file_name}'

    title = models.CharField(max_length=32, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    image = models.ImageField(null=True, blank=True, upload_to=get_file_name, verbose_name="Фотография")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")

    def __str__(self):
        return f"{self.title} - {self.author.login}"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост")
    text = models.TextField(verbose_name="Текст")

    def __str__(self):
        return f"{self.post.title} - {self.author.login} - {self.text}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"