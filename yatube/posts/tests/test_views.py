from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post, User, Comment, Follow

COUNT_POST_PAGE_1 = 10
COUNT_POST_PAGE_2 = 3
COUNT_POST = 13
TEXT = 'TEXT_FOR_THE_TEST'


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='User')
        cls.author = User.objects.create(username='Author')
        cls.group = Group.objects.create(
            title='Название',
            slug='slug',
            description='Описание'
        )
        cls.group2 = Group.objects.create(
            title='Название_2',
            slug='slug_2',
            description='Описание_2'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text=TEXT,
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_urls_pages_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/create_post.html'
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_create_page_show_correct_context(self):
        """Проверка: Форма создания поста - post_create."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
        self.assertFalse(response.context['is_edit'])

    def test_post_edit_page_show_correct_context(self):
        """Проверка: Форма создания поста - post_create."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
        self.assertTrue(response.context['is_edit'])

    def test_post_on_index_group_profile_create(self):
        """Проверка: Созданный пост появился в Группе, Профайле, Главной"""
        reverse_page_names_post = [
            reverse('posts:index'),
            reverse('posts:profile', kwargs={
                'username': self.author.username}),
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}),
        ]
        for url in reverse_page_names_post:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(len(response.context['page_obj']), 1)

    def test_index_page_show_correct_context(self):
        """Проверка: Шаблон index с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:index'))
        post = response.context['page_obj'][0]
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group, self.post.group)
        self.assertIn('page_obj', response.context)

    def test_group_list_page_show_correct_context(self):
        """Проверка: Шаблон group_list с правильным контекстом"""
        response = (self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'slug'})))
        self.assertIn('page_obj', response.context)
        self.assertIn('group', response.context)
        post = response.context['page_obj'][0]
        group = response.context['group']
        self.assertEqual(post.group, self.post.group)
        self.assertEqual(group, self.post.group)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)

    def test_profile_page_shows_correct_context(self):
        """Проверка: Шаблон profile с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.author.username})
        )
        self.assertIn('page_obj', response.context)
        self.assertIn('author', response.context)
        post = response.context['page_obj'][0]
        author = response.context['author']
        self.assertEqual(post.group, self.post.group)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(author, self.post.author)

    def test_post_detail_list_page_show_correct_context(self):
        """Проверка: Шаблон post_detail с правильным контекстом"""
        response = (self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id})))
        post_detail = response.context['post']
        self.assertEqual(post_detail.text, self.post.text)
        self.assertEqual(post_detail.group, self.post.group)
        self.assertEqual(post_detail.author, self.post.author)

    def test_post_not_in_other_group(self):
        """Проверка: Созданный пост не появился в иной группе"""
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group2.slug}
            )
        )
        self.assertNotIn(self.post, response.context.get('page_obj'))
        group2 = response.context.get('group')
        self.assertNotEqual(group2, self.group)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='User')
        cls.group = Group.objects.create(
            title='Название',
            slug='slug',
            description='Описание',
        )
        cls.posts = [
            Post(
                text=f' TEXT {number_post}',
                author=cls.user,
                group=cls.group,
            )
            for number_post in range(COUNT_POST)
        ]
        Post.objects.bulk_create(cls.posts)

    def setUp(self):
        self.authorized_author = Client()

    def test_page_contains_ten_records(self):
        """Проверка: пагинация на 1, 2 странице index, group_list, profile"""
        pagin_urls = (
            ('posts:index', None),
            ('posts:group_list', (self.group.slug,)),
            ('posts:profile', (self.user.username,))
        )
        pages_units = (
            ('?page=1', COUNT_POST_PAGE_1),
            ('?page=2', COUNT_POST_PAGE_2)
        )
        for address, args in pagin_urls:
            for page, count_posts in pages_units:
                with self.subTest(page=page):
                    response = self.authorized_author.get(
                        reverse(address, args=args) + page
                    )
            self.assertEqual(len(response.context['page_obj']), count_posts)
