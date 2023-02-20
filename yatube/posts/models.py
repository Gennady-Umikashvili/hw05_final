from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


NUMBER_OF_CHARACTERS = 15


class Group(models.Model):
    title = models.CharField("Заглавие", max_length=200)
    slug = models.SlugField("Значение", unique=True)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField("Текст", help_text="Текст нового поста")
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Группа",
        help_text="Группа, к которой будет относиться пост",
    )
    image = models.ImageField("Картинка", upload_to="posts/", blank=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text[:NUMBER_OF_CHARACTERS]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        null=True,
        on_delete=models.SET_NULL,
        related_name="comments",
        verbose_name="Комментарий",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(
        "Текст комментария", help_text="Введите текст комментария"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        models.UniqueConstraint(fields=["user", "author"], name="following")
