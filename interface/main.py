import tkinter as tk
import json, requests, time, datetime, multiprocessing
from tkinter import *
from tkinter import messagebox

token = '7e04d8f1ad225832d1b42835499a5c65b8c46a3cab83cd25a9cb2f2d87542b8927d3e61133d23c13c02bc'
v = 5.92

import threading
import inspect
import ctypes
import time


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class Thread(threading.Thread):
    def _get_my_tid(self):
        """determines this (self's) thread id"""
        if not self.is_alive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("could not determine the thread's id")

    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""
        _async_raise(self._get_my_tid(), exctype)

    def terminate(self):
        """raises SystemExit in the context of the given thread, which should
        cause the thread to exit silently (unless caught)"""
        self.raise_exc(SystemExit)


class Data(Thread):
    def __init__(self):
        self._running = True
        self.j = 24
        self.s = 0
        self.domain_name = ''
        self.stopped = False

    def terminate(self):
        on['text'] = 'Полный анализ - выкл'
        self._running = False

    def run(self):
        try:
            response = requests.post(f"http://127.0.0.1:8000/vk/auth/{self.domain_name}")
            self.data = response.json()
            info.delete(1.0, END)
            info.insert(1.0, self.data)
        except:
            messagebox.showerror(title='Неправильный домен', message='Неправильный домен')

    def send_domain(self):
        try:
            response = requests.get(f"http://127.0.0.1:8000/vk/auth/{self.domain_name}")
            self.data = response.json()
            self.dlina = len(self.data)
            info.delete(1.0, END)
            info.insert(1.0, f'{self.data[self.s:self.j]}\n')
            vsego_postov['text'] = f'Постов: {self.dlina}'
        except:
            messagebox.showerror(title='Неправильный домен', message='Неправильный домен')

    def get_data_next(self):
        try:
            self.j += 25
            self.s += 25
            info.delete(1.0, END)
            return info.insert(1.0, f'{self.data[self.s:self.j]}\n')
        except:
            messagebox.showerror(title='Ошибка', message='В посте находится неотображаемый символ')

    def get_data_past(self):
        try:
            self.j -= 25
            self.s -= 25
            info.delete(1.0, END)
            return info.insert(1.0, f'{self.data[self.s:self.j]}\n')
        except:
            messagebox.showerror(title='Ошибка', message='В посте находится неотображаемый символ')

    def get_post_id(self):
        try:
            self.j -= 1
            info.delete(1.0, END)
            return info.insert(1.0, f'{self.data[int(post_id.get())]}\n')
        except:
            messagebox.showerror(title='Ошибка', message='В посте находится неотображаемый символ')

    def stop_threads_potok(self):
        self.stopped = True

    def set_domain(self):
        self.domain_name = domain.get()
        domain_label['text'] = self.domain_name



class Test():
    def get_count(self):
        get_count = requests.get(
            'https://api.vk.com/method/users.search',
            params={
                'access_token': token,
                'v': v,
                'city': 730,
                'country': 4,
                'count': 5
            }
        )
        time.sleep(1)
        data = get_count.json()
        return data

    def get_comment(self, i):
        return data


def users_add():
    a = Test()
    count = a.get_count()
    time.sleep(1)
    len = int(count['response']['count'])
    print(len)
    for i in range(1, len):
        print(i)
        try:
            response = requests.get(
                'https://api.vk.com/method/users.search',
                params={
                    'access_token': token,
                    'v': v,
                    'city': 730,
                    'country': 4,
                    'count': 1,
                    'offset': i,
                    'fields': 'sex, nickname, domain, city, country, photo_id, status'
                }
            )
            time.sleep(1)
            data = response.json()
            datas = data['response']['items'][0]
            data = {}
            data["user_id"] = datas['id']
            data["first_name"] = datas['first_name']
            data['last_name'] = datas['last_name']
            data["is_closed"] = datas['is_closed']
            if data['is_closed'] is False:
                data['sex'] = datas['sex']
                data["nickname"] = datas['nickname']
                data["domain"] = datas['domain']
                data["photo"] = datas['photo_id'] or ''
                data["status"] = datas['status']
            else:
                data['sex'] = ''
                data["nickname"] = ''
                data["domain"] = ''
                data["photo"] = ''
                data["status"] = ''
            data["city"] = 'Taraz'
            data["county"] = 'Kz'
            data["checked"] = False
        except: pass
        try:
            new_response = requests.post(
                'http://localhost:8000/vk/user/add',
                data=data,
            )
            get_groups(datas['id'])
            new_response = requests.put(
                'http://localhost:8000/vk/user/add',
                data={"user_id": datas['id'], "checked": True},
            )
        except: pass


def getUsers():
    response = requests.get(
        'http://localhost:8000/vk/user/add'
    )
    data = response.json()
    return data


def get_groups(user_id):
    response = requests.get(
        'https://api.vk.com/method/groups.get',
        params={
            'access_token': token,
            'v': 5.131,
            'user_id': user_id,
            'extended': 1
        }
    )
    time.sleep(1)
    groups = response.json()
    id_groups = groups['response']['items']
    group_list = []
    for i in id_groups:
        print(i['screen_name'])
        passed = 0
        try:
            response = requests.get(
                'https://api.vk.com/method/wall.get',
                params={
                    'access_token': token,
                    'v': v,
                    'domain': i['screen_name'],
                    'count': 1
                }
            )
            bad = requests.get(f"http://127.0.0.1:8000/vk/auth/{i['screen_name']}/analyze/detail/bad")
            pre_data = response.json()
            time.sleep(1)
            count = pre_data['response']['count']
            for z in range(1, count, 5):
                if passed < 10:
                    try:
                        print(int(pre_data['response']['items'][0]['owner_id']))
                        print(user_id)
                        print(z)
                        response = requests.get(
                            'https://api.vk.com/method/execute.getCommentGroup',
                            params={
                                'access_token': token,
                                'v': 5.131,
                                'owner_id': int(pre_data['response']['items'][0]['owner_id']),
                                'user_id': user_id,
                                'post_count': 5,
                                'offset': z
                            }
                        )
                        time.sleep(5)
                        comments = response.json()
                        print(comments)
                        for comment in comments['response']:
                            print(comment)
                            requests.post(
                                'http://localhost:8000/vk/auth/comment/add',
                                data={"number": comment['id'], "from_id": comment['from_id'], 'post_id': comment['post_id'],
                                      'date': set_time(time=comment['date']), 'text': comment['text'], 'likes': 0, 'domain': i['screen_name']}
                            )
                            commen_data = comment['text']
                            comment_words = set(commen_data.lower().split()) & set(bad.json()['bad'])
                            if len(comment_words) > 1:
                                info.insert(1.0, f'{comment}: {comment_words}\n')
                                requests.post(f"http://127.0.0.1:8000/vk/auth/bad_data/add",
                                              data={'number': comment['number'],
                                                    'bad_word': comment_words,
                                                    'text': comment['text'],
                                                    'user': comment['from_id']}
                                              )
                    except Exception as e: passed += 1
            group_list.append(i['screen_name'])
        except: pass
    try:
        requests.post(
            'http://localhost:8000/vk/group/add',
            data={"user_id": user_id, "group": group_list}
        )
    except: pass

def set_time(time):
    timestamp = datetime.datetime.fromtimestamp(time)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def fast_start():
    users_add()


app = tk.Tk()
app.title('Мониторинг социальной сети Вконтакте')
app.geometry('1080x500')
app.resizable(width=False, height=False)
data = Data()
ttt = multiprocessing.Process(target=data.run)
sss = multiprocessing.Process(target=fast_start)
frame = Frame(app)
frame.place(relwidth=1, relheight=1)

title = Label(frame, text="Введите домен", font=40)
title.grid(row=0, column=0, stick='we')
vsego_postov = Label(frame, text="Постов:", font=40)
vsego_postov.grid(row=0, column=3, stick='we')
domain_label = Label(frame, text="Домен:", font=40)
domain_label.grid(row=5, column=3, stick='we')
post_id = Entry(frame, bg='white')
post_id.grid(row=1, column=3, stick='we')
button_id = Button(frame, command=data.get_post_id, text="Получить пост")
button_id.grid(row=2, column=3, stick='nswe')
button_id = Button(frame, command=data.set_domain, text="Установить домен")
button_id.grid(row=6, column=3, stick='nswe')
button_send = Button(frame, command=ttt.start, text="Начать захват данных")
button_send.grid(row=2, column=0, stick='nswe')
button_stop = Button(frame, command=sss.start, text="Автоматический режим работы")
button_stop.grid(row=3, column=3, stick='ns')
domain = Entry(frame, bg='white')
domain.grid(row=1, column=0, stick='we')
button = Button(frame, command=data.send_domain, text="Получить данные")
button.grid(row=3, column=0, stick='nswe')
info = Text(frame)
info.grid(row=0, column=1, rowspan=6, stick='we')
scroll = Scrollbar(command=info.yview)
scroll.pack(side=RIGHT, fill=Y)
info.config(yscrollcommand=scroll.set)
prev = Button(frame, command=data.get_data_past, text="Прошлый")
prev.grid(row=4, column=0, stick='nswe')
nex = Button(frame, command=data.get_data_next, text="Следующий")
nex.grid(row=5, column=0, stick='nswe')

page2 = Frame(app)
page2.place(relwidth=1, relheight=1)
page2.lower()


def to2_page():
    frame.lower()
    page2.lift()


def to1_page():
    page2.lower()
    frame.lift()


class Page(Thread):
    def __init__(self):
        self._running = True

    def terminate(self):
        on['text'] = 'Полный анализ - выкл'
        self._running = False
        t.join()

    def fast_analyze(self):
        domain_name = data.domain_name
        response = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/posts")
        self.data = response.json()
        info_2.delete(1.0, END)
        for i in self.data:
            info_2.insert(1.0, f'{i}\n')

    def fast_analyze_comments(self):
        domain_name = data.domain_name
        response = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/comments")
        self.data = response.json()
        info_2.delete(1.0, END)
        for i in self.data:
            info_2.insert(1.0, f'{i}\n')

    def run(self):
        # try:
        on['text'] = 'Полный анализ - вкл'
        domain_name = data.domain_name
        ids = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/detail/ids")
        comments = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/detail/commentsIds")
        bad = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/detail/bad")
        for i in ids.json():
            ids = requests.get(f"http://127.0.0.1:8000/vk/auth/post/{i['number']}")
            ids_dat = ids.json()[0]
            ids_data = ids.json()[0]['title']
            common_words = set(ids_data.lower().split()) & set(bad.json()['bad'])
            for h in comments.json():
                comment = requests.get(f"http://127.0.0.1:8000/vk/auth/comment/id/{h['number']}")
                comment_data = comment.json()[0]
                commen_data = comment.json()[0]['text']
                comment_words = set(commen_data.lower().split()) & set(bad.json()['bad'])
                if self._running is False:
                    break
                if len(comment_words) > 2:
                    try:
                        info_2.insert(1.0, f'{comment_data}: {comment_words}\n')
                        requests.post(f"http://127.0.0.1:8000/vk/auth/bad_data/add", data={'number': comment_data['number'],
                                                                                           'bad_word': comment_words,
                                                                                           'text': comment_data['text'],
                                                                                           'user': comment_data['from_id']})
                    except:pass
            if len(common_words) > 2:
                if self._running is False:
                    break
                try:
                    info_2.insert(1.0, f'{ids_dat}: {common_words}\n')
                    requests.post(f"http://127.0.0.1:8000/vk/auth/bad_data/add", data={'number': ids_data['number'],
                                                                                           'bad_word': common_words,
                                                                                           'text': ids_data['title'],
                                                                                           'user': ids_data['from_id']})
                except:pass


to_next = Button(frame, command=to2_page, text="Перейти к анализу данных")
to_next.grid(row=4, column=3, stick='nswe')

def get_groups_to_user():
    user_id = int(user_label['text'])
    response = requests.get(
        'https://api.vk.com/method/groups.get',
        params={
            'access_token': token,
            'v': 5.131,
            'user_id': user_id,
            'extended': 1
        }
    )
    time.sleep(1)
    groups = response.json()
    id_groups = groups['response']['items']
    group_list = []
    for i in id_groups:
        passed = 0
        response = requests.get(
            'https://api.vk.com/method/wall.get',
            params={
                'access_token': token,
                'v': 5.131,
                'owner_id': f"-{(i['id'])}",
                'count': 5
            }
        )
        bad = requests.get(f"http://127.0.0.1:8000/vk/auth/{i['screen_name']}/analyze/detail/bad")
        pre_data = response.json()
        time.sleep(1)
        count = pre_data['response']['count']
        for z in range(1, count, 5):
            if passed < 10:
                response = requests.get(
                    'https://api.vk.com/method/execute.getCommentGroup',
                    params={
                        'access_token': token,
                        'v': 5.131,
                        'owner_id': int(pre_data['response']['items'][0]['owner_id']),
                        'user_id': user_id,
                        'post_count': 5,
                        'offset': z
                    }
                )
                time.sleep(5)
                comments = response.json()
                for comment in comments['response']:
                    print(comment)
                    requests.post(
                        'http://localhost:8000/vk/auth/comment/add',
                        data={"number": comment['id'], "from_id": comment['from_id'], 'post_id': comment['post_id'],
                              'date': set_time(time=comment['date']), 'text': comment['text'], 'likes': 0, 'domain': i['screen_name']}
                    )
                    commen_data = comment['text']
                    comment_words = set(commen_data.lower().split()) & set(bad.json()['bad'])
                    print(len(comment_words))
                    if len(comment_words) >= 1:
                        print(True)
                        info_2.delete(1.0, END)
                        info_2.insert(1.0, f'{comment}: {comment_words}\n')
                        requests.post(f"http://127.0.0.1:8000/vk/auth/bad_data/add",
                                      data={'number': comment['id'],
                                            'bad_word': comment_words,
                                            'text': comment['text'],
                                            'user': comment['from_id']}
                                      )
        group_list.append(i['screen_name'])
    try:
        requests.post(
            'http://localhost:8000/vk/group/add',
            data={"user_id": user_id, "group": group_list}
        )
    except: pass


def users_add_only():
    response = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': token,
            'v': v,
            'user_ids': user_label['text'],
            'fields': 'sex, nickname, domain, city, country, photo_id, status'
        }
    )
    data = response.json()
    datas = data['response'][0]
    data = {}
    data["user_id"] = datas['id']
    data["first_name"] = datas['first_name']
    data['last_name'] = datas['last_name']
    data["is_closed"] = datas['is_closed']
    if data['is_closed'] is False:
        data['sex'] = datas['sex']
        data["nickname"] = datas['nickname']
        data["domain"] = datas['domain']
        data["photo"] = None
        data["status"] = datas['status']
    else:
        data['sex'] = ''
        data["nickname"] = ''
        data["domain"] = ''
        data["photo"] = ''
        data["status"] = ''
    data["city"] = 'Taraz'
    data["county"] = 'Kz'
    data["checked"] = False
    new_response = requests.post(
        'http://localhost:8000/vk/user/add',
        data=data,
    )
    get_groups_to_user()
    # new_response = requests.put(
    #     'http://localhost:8000/vk/user/add',
    #     data={"user_id": datas['id'], "checked": True},
    # )


new_data = Page()
t = Thread(target=new_data.run)
def terminate():
    time.sleep(0.6)
    t.terminate()
    t.join()
zzz = Thread(target=users_add_only)
start_fast_analyze = Button(page2, command=new_data.fast_analyze, text="Латентно-семантический анализ\n постов")
start_fast_analyze.grid(row=0, column=0, stick='nswe')

start_fast_analyze_comments = Button(page2, command=new_data.fast_analyze_comments, text="Латентно-семантический анализ\n комментариев")
start_fast_analyze_comments.grid(row=1, column=0, stick='nswe')

start_slov_analyze = Button(page2, command=t.start, text="Полный анализ")
start_slov_analyze.grid(row=2, column=0, stick='nswe')

start_slov_analyze = Button(page2, command=terminate, text="Остановить полный анализ")
start_slov_analyze.grid(row=3, column=0, stick='nswe')

back = Button(page2, command=to1_page, text="Вернуться назад")
back.grid()

info_2 = Text(page2)
info_2.grid(row=0, column=1, rowspan=6, stick='we')

on = Label(page2, text='Полный анализ - выкл')
on.grid(row=0, column=2, stick='we')


def set_domain():
    user_label['text'] = domain_user.get()


button_user = Button(page2, command=set_domain, text="Установить юзера")
button_user.grid(row=4, column=2, stick='nswe')
domain_user = Entry(page2, bg='white')
domain_user.grid(row=5, column=2, stick='we')
user_label = Label(page2, text="User:", font=40)
user_label.grid(row=6, column=2, stick='we')
complex = Button(page2, command=zzz.start, text="Комплексный анализ юзера")
complex.grid(row=4, column=0, stick='nswe')
page3 = Frame(app)
page3.place(relwidth=1, relheight=1)
page3.lower()


def to3_page():
    page2.lower()
    page3.lift()


class Page3():
    def add_ban(self):
        try:
            domain_name = data.domain_name
            response = requests.post(f"http://127.0.0.1:8000/vk/auth/bad_word/add", data={'bad_word': info_3.get("1.0", END)})
            self.data = response.json()
            info_3.delete(1.0, END)
            info_3.insert(1.0, f'{self.data["Post"]}\n')
        except:pass

    def get_ban(self):
        domain_name = data.domain_name
        response = requests.get(f"http://127.0.0.1:8000/vk/auth/bad_word/get")
        self.data = response.json()
        info_3.delete(1.0, END)
        info_3.insert(1.0, f'{self.data}\n')

    def get_user(self):
        user = user_id.get()
        response = requests.get(f"http://127.0.0.1:8000/vk/auth/user/{user}")
        data = response.json()
        info_2.delete(1.0, END)
        info_2.insert(1.0, f'{data}\n')



to_next_2 = Button(page2, command=to3_page, text="Слова")
to_next_2.grid(row=1, column=2, stick='nswe')

pages3 = Page3()
add_ban = Button(page3, command=pages3.add_ban, text="Добавить слова")
add_ban.grid(row=0, column=0, stick='nswe')
get_ban = Button(page3, command=pages3.get_ban, text="Получить слова")
get_ban.grid(row=1, column=0, stick='nswe')

back = Button(page3, command=to2_page, text="Назад")
back.grid(row=2, column=0, stick='nswe')

info_3 = Text(page3)
info_3.grid(row=0, column=1, rowspan=6, columnspan=2, stick='nswe')

user_id = Entry(page2, bg='white', text='Id пользователя')
user_id.grid(row=2, column=2, stick='we')

back = Button(page2, command=pages3.get_user, text="Получить")
back.grid(row=3, column=2, stick='nswe')

app.grid_rowconfigure(0, minsize=400)
# app.grid_rowconfigure(1, maxsize=400)

if __name__ == '__main__':
    try:
        app.mainloop()
    except:pass
