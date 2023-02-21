from django.test import TestCase

from posts.models import Group, Post, User, Comment


CHARACTERS_TEXT = 15


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User")
        cls.post = Post.objects.create(
            author=cls.user, text="TEXT_FOR_THE_TEST",
        )
        cls.comment = Comment.objects.create(
            author=cls.user, post=cls.post, text="COMMENT_FOR_THE_TEST"
        )

    def test_models_have_correct_object_names(self):
        """Проверка: что у моделей корректно работает __str__, title"""
        self.assertEqual(self.post.text[:CHARACTERS_TEXT], str(self.post))

    def test_models_correct_verbose_name(self):
        """Правильное verbose_name"""
        task_post = PostModelTest.post
        verbose_fields = {
            "text": "Текст",
            "author": "Автор",
            "group": "Группа",
        }
        for value, expected in verbose_fields.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_post._meta.get_field(value).verbose_name, expected
                )

    def test_models_correct_help_text(self):
        """Правильный help_text"""
        task_post = PostModelTest.post
        help_text_fields = {
            "text": "Текст нового поста",
            "group": "Группа, к которой будет относиться пост",
        }
        for value, expected in help_text_fields.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_post._meta.get_field(value).help_text, expected
                )

    def test_comment_model_correct_verbose_name(self):
        """Правильное verbose_name"""
        task_comment = PostModelTest.comment
        verbose_fields = {
            "post": "Комментарий",
            "author": "Автор",
            "text": "Текст комментария",
            "pub_date": "Дата публикации",
        }
        for value, expected in verbose_fields.items():
            with self.subTest(value=value):
                self.assertEqual(
                    task_comment._meta.get_field(value).verbose_name, expected
                )


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="User")
        cls.group = Group.objects.create(
            title="Название", slug="slug", description="Описание",
        )

    def test_models_have_correct_object_names(self):
        """Проверка: что у моделей корректно работает __str__, title"""
        self.assertEqual(self.group.title, str(self.group))
