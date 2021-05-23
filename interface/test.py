from math import ceil
import json,time

import vk_api
token = '7e04d8f1ad225832d1b42835499a5c65b8c46a3cab83cd25a9cb2f2d87542b8927d3e61133d23c13c02bc'
vk = vk_api.VkApi(token=token)  # Ваш токен
api = vk.get_api()

posts = api.wall.getById(posts='{owner_id}_{post_id}'.format(owner_id='-88245281', post_id='<post_id>'))  # Где <owner_id> - id пользователя/группы, post_id - id поста. *см. комментарии после кода

if not posts:
    print('No posts found!')

post = posts[0]
posts = []

for offset in range(ceil(post['comments']['count'] // 2500)):
    posts.extend(api.execute.getCommentsFromPost(owner_id='<owner_id>', post_id='<post_id>', offset=2500*offset, count=2500)['items'])  # тут всё по аналогии, как и в первый раз
    time.sleep(0.34)  # избегаем flood control

with open('output.json', 'w') as file:
    json.dump(posts, file)