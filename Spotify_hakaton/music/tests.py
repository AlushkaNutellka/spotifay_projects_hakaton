from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from collections import OrderedDict
from django.core.files import File

from .views import MusicViewSet
from .models import MusicInfo, Comment, User


class PostTest(APITestCase):

    def SetUp(self):
        self.factory = APIRequestFactory()
        self.category = MusicInfo.objects.create(
            title='cat1'
        )
        user = User.objects.create_user(
            email='akzolkanaev81@gmail.com',
            password='1234',
            is_active=True,
            name='Akjol',
            last_name='Kanaev'
        )
        img = File(open('/home/akjol/Downloads/Telegram Desktop/photo_2021-12-30_14-47-32.jpg', 'rb'))
        posts = [
            MusicInfo(author=user, body='new post',
                 title='post1', image=img, category=self.category, slug='1'),

            MusicInfo(author=user, body='new post',
                 title='post1', image=img, category=self.category, slug='2'),

            MusicInfo(author=user, body='new post',
                 title='post1', image=img, category=self.category, slug='3'),

            MusicInfo(author=user, body='new post',
                 title='post1', image=img, category=self.category, slug='4')
        ]
        MusicInfo.obojects.bulk_create(posts)

    def test_list(self):
        request = self.factory.get('music/')
        view = MusicViewSet.as_view({'get': 'list'})
        response = view(request)
        # print(response.data)

        self.assertEqual(response.status_code, 200)
        assert type(response.data) == OrderedDict

    def test_retrieve(self):
        slug = MusicInfo.objects.all()[0].slug
        request = self.factory.get(f'music/{slug}/')
        view = MusicViewSet.as_view({'get': 'retrive'})
        response = view(request, pk=slug)
        # print(response.data)

        assert response.status_code == 200

    def test_create(self):
        user = User.objects.all()
        data = {
            'body': 'vava',
            'title': 'post4',
            'category': 'cat1'
        }
        request = self.factory.post('music/', data, format='json')
        force_authenticate(request, user=user)
        view = MusicViewSet.as_view({'post': 'create'})
        response = view(request)
        print(response.data)

        assert response.status_code == 201
        assert response.data['body'] == data['body']
        assert MusicInfo.objects.filter(author=user, body=data['body']).exists()