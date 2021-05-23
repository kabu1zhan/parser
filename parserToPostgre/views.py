import time, ast
import pymorphy2
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
import requests, datetime
from .serializers import *

token = '7e04d8f1ad225832d1b42835499a5c65b8c46a3cab83cd25a9cb2f2d87542b8927d3e61133d23c13c02bc'

v = 5.92

morph = pymorphy2.MorphAnalyzer()


class VkAuth(APIView):
    def get_comment(self, post_id, offset, onwer):
        response = requests.get(
            'https://api.vk.com/method/wall.getComments',
            params={
                'access_token': token,
                'v': v,
                'owner_id': onwer,
                'post_id': post_id,
                'need_likes': 1,
                'count': 1,
                'offset': offset
            }
        )
        data = response.json()
        return data

    def set_time(self, time):
        timestamp = datetime.datetime.fromtimestamp(time)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def get_posts(self, domain):
        response = requests.get(
            'https://api.vk.com/method/wall.get',
            params={
                'access_token': token,
                'v': v,
                'domain': domain,
                'count': 1
            }
        )
        pre_data = response.json()
        count = pre_data['response']['count']
        for i in range(0, count):
            try:
                response = requests.get(
                    'https://api.vk.com/method/wall.get',
                    params={
                        'access_token': token,
                        'v': v,
                        'domain': domain,
                        'count': 1,
                        'offset': i,
                    }
                )
                data = response.json()
                parsed_data = data['response']['items'][0]
                post = models.Group.objects.create(
                    title=parsed_data['text'],
                    count=i,
                    number=parsed_data['id'],
                    comment_number=parsed_data['comments']['count'],
                    views=parsed_data['views']['count'],
                    likes=parsed_data['likes']['count'],
                    reposts=parsed_data['reposts']['count'],
                    date=self.set_time(time=parsed_data['date']),
                    owner=parsed_data['owner_id'],
                    domain=domain,
                    from_id=parsed_data['from_id']
                )
                for j in range(1, parsed_data['comments']['count']):
                    comment = self.get_comment(parsed_data['id'], j, parsed_data['owner_id'])
                    parsed_comment = comment['response']['items'][0]
                    models.Comments.objects.create(
                        number=parsed_comment['id'],
                        from_id=parsed_comment['from_id'],
                        post_id_id=post.number,
                        date=self.set_time(time=parsed_comment['date']),
                        text=parsed_comment['text'],
                        likes=parsed_comment['likes']['count'],
                        domain=domain
                    )
                time.sleep(1)
            except:
                pass
        return {'result': True}

    def post(self, request, *args, **kwargs):
        domain = kwargs['domain']
        posts = self.get_posts(domain)
        return Response(posts)

    def get(self, request, *args, **kwargs):
        domain = kwargs['domain']
        queryset = models.Group.objects.filter(domain=domain)
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)


class GetAllComment(APIView):

    def get(self, request, *args, **kwargs):
        queryset = models.Comments.objects.filter(post_id=kwargs['post_id'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class GetComment(APIView):

    def get(self, request, *args, **kwargs):
        queryset = models.Comments.objects.filter(number=kwargs['comment_id'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)


class GetPost(APIView):

    def get(self, request, *args, **kwargs):
        queryset = models.Group.objects.filter(number=kwargs['post_id'])
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)


class GetUser(APIView):

    def get(self, request, *args, **kwargs):
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': token,
                'v': v,
                'user_ids': kwargs['user_id'],
                'fields': 'photo_id, sex, city, country, home_town, domain, status, nickname, '
            }
        )
        data = response.json()
        return Response(data)


class StartAnalyse(APIView):
    def get(self, request, *args, **kwargs):
        queryset = models.Group.objects.filter(domain=kwargs['domain']).values('title')
        serializer = TitleSerializer(queryset, many=True)
        filename = f"{kwargs['domain']}.txt"
        f = open(filename, "w+")
        f.seek(0)
        f.truncate()
        for i in serializer.data:
            try:
                f.write(i['title'])
            except:
                pass
        from dataAnalize import analize
        response = analize.start(f"{kwargs['domain']}")
        return Response(response)


class StartAnalyseComments(APIView):
    def get(self, request, *args, **kwargs):
        queryset= models.Comments.objects.filter(domain=kwargs['domain']).values('text')
        serializer = TextSerializer(queryset, many=True)
        filename = f"{kwargs['domain']}_comments.txt"
        f = open(filename, "w+")
        f.seek(0)
        f.truncate()
        for i in serializer.data:
            try:
                f.write(i['text'])
            except:
                pass
        # filename = f"{kwargs['domain']}_comments.txt"
        # f = open(filename, "w+")
        # for j in ids:
        #     post = models.Comments.objects.get(number=j)
        #     post_serializer = CommentSerializer(post)
        #     data = post_serializer.data['text']
        #     f.write(data)
        from dataAnalize import analize
        response = analize.start(f"{kwargs['domain']}_comments")
        return Response(response)


class GetIds(APIView):
    def get(self, request, *args, **kwargs):
        group = models.Group.objects.filter(domain=kwargs['domain']).values('number')
        serializer = NumberSerializer(group, many=True)
        return Response(serializer.data)


class GetCommentIds(APIView):
    def get(self, request, *args, **kwargs):
        comment = models.Comments.objects.filter(domain=kwargs['domain']).values('number')
        comment_serializer = NumberSerializer(comment, many=True)
        return Response(comment_serializer.data)


class GetBadWords(APIView):
    def get(self, request, *args, **kwargs):
        bad_list = set()
        bad_words = models.BadWord.objects.filter().values('varianty')
        bad_serializer = ValuesSerializer(bad_words, many=True)
        for d in bad_serializer.data:
            x = ast.literal_eval(d['varianty'])
            bad_list.update(x)
        return Response({'bad': bad_list})


class DetailAnalise(APIView):
    def get(self, request, *args, **kwargs):
        group = models.Group.objects.all().values('number')
        comment = models.Comments.objects.all().values('number')
        bad_list = set()
        bad_words = models.BadWord.objects.filter().values('varianty')
        bad_serializer = ValuesSerializer(bad_words, many=True)
        for d in bad_serializer.data:
            x = ast.literal_eval(d['varianty'])
            bad_list.update(x)
        serializer = NumberSerializer(group, many=True)
        comment_serializer = NumberSerializer(comment, many=True)
        comment_ids = []
        ids = []
        for i in serializer.data:
            ids.append(i['number'])
            for s in comment_serializer.data:
                comment_ids.append(s['number'])
        response = {}
        for j in ids:
            post = models.Group.objects.get(number=j)
            post_serializer = GroupSerializer(post)
            data = post_serializer.data['title']
            common_words = set(data.lower().split()) & bad_list
            for h in comment_ids:
                comments = models.Comments.objects.get(number=h)
                comments_serializer = CommentSerializer(comments)
                datas = comments_serializer.data['text']
                comment_words = set(datas.lower().split()) & bad_list
                print(comment_words)
                if len(comment_words) > 0:
                    try:
                        models.BadData.objects.create(number=comments.number, bad_word=comment_words, text=comments,
                                                      user=comments.from_id)
                    except:pass
                    response[comments.number] = common_words
            if len(common_words) > 0:
                try:
                    models.BadData.objects.create(number=post.number, bad_word=common_words, text=post, user=post.from_id)
                except:pass
                response[post.number] = common_words
        return Response(response)


class DetailAnaliseComments(APIView):
    def get(self, request, *args, **kwargs):
        queryset = models.Comments.objects.all().values('number')
        bad_list = set()
        bad_words = models.BadWord.objects.filter().values('varianty')
        bad_serializer = ValuesSerializer(bad_words, many=True)
        for d in bad_serializer.data:
            x = ast.literal_eval(d['varianty'])
            bad_list.update(x)
        serializer = NumberSerializer(queryset, many=True)
        ids = []
        for i in serializer.data:
            ids.append(i['number'])
        response = {}
        for j in ids:
            post = models.Comments.objects.get(number=j)
            post_serializer = CommentSerializer(post)
            data = post_serializer.data['text']
            common_words = set(data.lower().split()) & bad_list
            if len(common_words) > 0:
                models.BadData.objects.create(number=post.number, bad_word=common_words)
                response[post.number] = common_words
                response[post.number]
        return Response(response)


class AddBadWord(APIView):
    def post(self, request, *args, **kwargs):
        bad_words = request.data.get('bad_word')
        bad_words = bad_words.split()
        for i in bad_words:
            other = []
            slovo = morph.parse(i)[0]
            for j in slovo.lexeme:
                other.append(j[0])
            try:
                models.BadWord.objects.create(slovo=i, varianty=str(other))
            except:
                return Response({'Error': 'Это слово уже добавленно'})
        return Response({'Post': other})


class GetBadWord(APIView):
    def get(self, request, *args, **kwargs):
        queryset = models.BadWord.objects.all()
        serializer = BadWordSerializer(queryset, many=True)
        return Response(serializer.data)


class BadData(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BadDataSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({'result': True})


class AddComment(APIView):
    def post(self, request):
        a = Comments.objects.create(
            number=request.data['number'],
            from_id=request.data['from_id'],
            post_id_id=None,
            post_base=request.data['post_id'],
            date=request.data['date'],
            text=request.data['text'],
            likes=request.data['likes'],
            domain=request.data['domain'],
        )
        return Response({'result': True})


class AddGroup(APIView):
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class AddUserApi(APIView):
    def post(self, request):
        datas = request.data
        User.objects.create(
            user_id=datas['user_id'],
            first_name=datas['first_name'],
            last_name=datas['last_name'],
            is_closed=datas['is_closed'],
            sex=datas['sex'],
            nickname=datas['nickname'],
            domain=datas['domain'],
            city=datas['city'],
            county=datas['county'],
            photo=None,
            status=datas['status'],
            checked=False
        )
        return Response({'result': True})

    def get(self, request):
        queryset = User.objects.filter(is_closed=True).values('user_id')
        serializer = IdSerializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request):
        user = User.objects.get(user_id=request.data['user_id'])
        user.checked = True
        user.save()
        return Response({'result': True})


class GroupApi(APIView):
    def post(self, request):
        print(dict(request.data)['group'])
        models.GroupListUser.objects.create(
            user_id=request.data['user_id'],
            group=dict(request.data)['group']
        )
        return Response({'result': True})