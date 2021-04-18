import requests, datetime

token = '7e04d8f1ad225832d1b42835499a5c65b8c46a3cab83cd25a9cb2f2d87542b8927d3e61133d23c13c02bc'

v = 5.92

class Test():
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

    def run(self, domain):
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
            # try:
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
            response = requests.post(f"http://127.0.0.1:8000/vk/auth/group/add", data={
                # 'title': 'text',
                # 'count': 1,
                # 'number': 7658,
                # 'comment_number': 1,
                # 'views': 1,
                # 'likes': 1,
                # 'reposts': 1,
                # 'date': "2021-04-14 21:48:08+06",
                # 'owner': 567,
                # 'domain': domain,
                # 'from_id': 215
                'title': parsed_data['text'],
                'count': i,
                'number': 185128,
                'comment_number': int(parsed_data['comments']['count']),
                'views': int(parsed_data['views']['count']),
                'likes': int(parsed_data['likes']['count']),
                'reposts': int(parsed_data['reposts']['count']),
                'date': self.set_time(time=parsed_data['date']),
                'owner': int(parsed_data['owner_id']),
                'domain': domain,
                'from_id': int(parsed_data['from_id'])
            }
                                     )
            print(response)
            print(response.json())
            for j in range(1, parsed_data['comments']['count']):
                comment = self.get_comment(parsed_data['id'], j, parsed_data['owner_id'])
                parsed_comment = comment['response']['items'][0]
                comments_add = requests.post(f"http://127.0.0.1:8000/vk/auth/comment/add", data={
                    'number': 12894,
                    'from_id': parsed_comment['from_id'],
                    'post_id_id': response.json()['number'],
                    'date': self.set_time(time=parsed_comment['date']),
                    'text': parsed_comment['text'],
                    'likes': parsed_comment['likes']['count'],
                    'domain': domain
                }

                                             )

a = Test()
a.run('hellyeahplay')