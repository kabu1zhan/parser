import tkinter as tk
import json, requests, time, datetime, multiprocessing
from tkinter import *
from tkinter import messagebox
import threading
import inspect
import ctypes
import time

token = '7e04d8f1ad225832d1b42835499a5c65b8c46a3cab83cd25a9cb2f2d87542b8927d3e61133d23c13c02bc'
v = 5.92

app = tk.Tk()
app.title('Пульт управления')
app.geometry('585x320')
app.resizable(width=False, height=False)
app.withdraw()


login_app = tk.Tk()
login_app.title('Войдите')
login_app.geometry('300x80')
login_app.resizable(width=False, height=False)

login_frame = Frame(login_app, bg='white')
login_frame.place(relwidth=1, relheight=1)


first_frame = Frame(app)
first_frame.place(relwidth=1, relheight=1)
first_frame.lower()


data_sets = tk.Tk()
data_sets.title('Установка данных')
data_sets.geometry('350x120+600+100')
data_sets.resizable(width=False, height=False)
data_sets.withdraw()

data_frame = Frame(data_sets)
data_frame.place(relwidth=1, relheight=1)
data_frame.lower()


display = tk.Tk()
display.title('Дисплей')
display.geometry('1000x500+600+300')
display.resizable(width=False, height=False)
display.withdraw()

display_frame = Frame(display)
display_frame.place(relwidth=1, relheight=1)
display_frame.lower()


slovar = tk.Tk()
slovar.title('Словарь')
slovar.geometry('500x250+600+300')
slovar.resizable(width=False, height=False)
slovar.withdraw()

slovar_frame = Frame(slovar)
slovar_frame.place(relwidth=1, relheight=1)
slovar_frame.lower()

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


def send_login():
    response = requests.post(
        'http://localhost:8000/vk/user/',
        data={"login": login_form.get(), "password": password_form.get()}
    )
    login_data = response.json()
    if login_data['result'] == True:
        login_app.destroy()
        app.deiconify()
    else:
        mes = messagebox.showerror(title='Ошибка входа', message='Неправильный логин или пароль')



class Data(Thread):
    def __init__(self):
        self._running = True
        self.j = 24
        self.s = 0
        self.domain_name = ''
        self.user_name = ''
        self.stopped = False

    def terminate(self):
        # on['text'] = 'Полный анализ - выкл'
        self._running = False

    def run(self):
        try:
            response = requests.post(f"http://127.0.0.1:8000/vk/auth/{self.domain_name}")
            self.data = response.json()
            # info.delete(1.0, END)
            # info.insert(1.0, self.data)
        except:
            messagebox.showerror(title='Неправильный домен', message='Неправильный домен')

    def send_domain(self):
        try:
            domain_name = group_label['text']
            response = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name.split()[1]}")
            self.data = response.json()
            vsego_postov['text'] = f'Постов: {len(self.data)}'
            display_text.delete(1.0, END)
            display_text.insert(1.0, f'{self.data[data.s:data.j]}\n')
        except:
            messagebox.showerror(title='Неправильный домен', message='Неправильный домен')


    def get_data_next(self):
        try:
            self.j += 25
            self.s += 25
            display_text.delete(1.0, END)
            return display_text.insert(1.0, f'{self.data[self.s:self.j]}\n')
        except:
            messagebox.showerror(title='Ошибка', message='В посте находится неотображаемый символ')

    def get_data_past(self):
        try:
            self.j -= 25
            self.s -= 25
            display_text.delete(1.0, END)
            return display_text.insert(1.0, f'{self.data[self.s:self.j]}\n')
        except:
            messagebox.showerror(title='Ошибка', message='В посте находится неотображаемый символ')

    def get_post_id(self):
        try:
            self.j -= 1
            display_text.delete(1.0, END)
            return display_text.insert(1.0, f'{self.data[int(post_form.get())]}\n')
        except:
            messagebox.showerror(title='Ошибка', message='В посте находится неотображаемый символ')

    def stop_threads_potok(self):
        self.stopped = True


def set_time(time):
    timestamp = datetime.datetime.fromtimestamp(time)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def get_groups(user_id):
    print(user_id)
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
    display_text.delete(1.0, END)
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
            for z in range(1, count, 3):
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
                                'post_count': 3,
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
                            if len(comment_words) >= level.get():
                                display_text.insert(1.0, f'{comment}: {comment_words}\n')
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

data = Data()

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


def to_data_frame():
    data_sets.deiconify()

def data_sets_exit():
    data_sets.withdraw()

def data_save():
    group_label['text'] = f"Группа: {group_domain_form.get()}"
    user_label['text'] = f"Пользователь: {user_id_form.get()}"
    data.domain_name = group_domain_form.get()
    data.user_name = user_id_form.get()

def get_numbers():
    domain_name = group_label['text']
    response = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name.split()[1]}")
    json_data = response.json()
    vsego_postov['text'] = f'Постов: {len(json_data)}'
    display_text.delete(1.0, END)
    display_text.insert(1.0, f'{json_data[data.s:data.j]}\n')

def display_open():
    display.deiconify()

def display_exit():
    display.withdraw()

def slovar_open():
    slovar.deiconify()

def slovar_exit():
    slovar.withdraw()

def fast_start():
    users_add()


class Page(Thread):
    def __init__(self):
        self._running = True

    def fast_analyze(self):
        domain_name = data.domain_name
        response = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/posts")
        self.data = response.json()
        display_text.delete(1.0, END)
        for i in self.data:
            display_text.insert(1.0, f'{i}\n')

    def fast_analyze_comments(self):
        domain_name = data.domain_name
        response = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/comments")
        self.data = response.json()
        display_text.delete(1.0, END)
        for i in self.data:
            display_text.insert(1.0, f'{i}\n')

    def run(self):
        # try:
        # on['text'] = 'Полный анализ - вкл'
        display_text.delete(1.0, END)
        domain_name = data.domain_name
        ids = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/detail/ids")
        comments = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/detail/commentsIds")
        bad = requests.get(f"http://127.0.0.1:8000/vk/auth/{domain_name}/analyze/detail/bad")
        print(bad.json()['bad'])
        for i in ids.json():
            ids = requests.get(f"http://127.0.0.1:8000/vk/auth/post/{i['number']}")
            ids_dat = ids.json()[0]
            ids_data = ids.json()[0]['title']
            common_words = set(ids_data.lower().split()) & set(bad.json()['bad'])
            if len(common_words) >= level.get():
                if self._running is False:
                    break
                try:
                    display_text.insert(1.0, f'{ids_dat}: {common_words}\n')
                    requests.post(f"http://127.0.0.1:8000/vk/auth/bad_data/add", data={'number': ids_data['number'],
                                                                                           'bad_word': common_words,
                                                                                           'text': ids_data['title'],
                                                                                           'user': ids_data['from_id']})
                except:pass
        for h in comments.json():
            comment = requests.get(f"http://127.0.0.1:8000/vk/auth/comment/id/{h['number']}")
            comment_data = comment.json()[0]
            commen_data = comment.json()[0]['text']
            comment_words = set(commen_data.lower().split()) & set(bad.json()['bad'])
            if self._running is False:
                break
            print(comment_words)
            print(len(comment_words))
            if len(comment_words) >= level.get():
                try:
                    display_text.insert(1.0, f'{comment_data}: {comment_words}\n')
                    requests.post(f"http://127.0.0.1:8000/vk/auth/bad_data/add", data={'number': comment_data['number'],
                                                                                       'bad_word': comment_words,
                                                                                       'text': comment_data['text'],
                                                                                       'user': comment_data['from_id']})
                except:pass



def get_groups_to_user():
    user_id = data.user_name
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
                    if len(comment_words) >= 1:
                        display_text.delete(1.0, END)
                        display_text.insert(1.0, f'{comment}: {comment_words}\n')
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
            'user_ids': data.user_name,
            'fields': 'sex, nickname, domain, city, country, photo_id, status'
        }
    )
    res = response.json()
    datas = res['response'][0]
    zxc = {}
    zxc["user_id"] = datas['id']
    zxc["first_name"] = datas['first_name']
    zxc['last_name'] = datas['last_name']
    zxc["is_closed"] = datas['is_closed']
    if zxc['is_closed'] is False:
        zxc['sex'] = datas['sex']
        zxc["nickname"] = datas['nickname']
        zxc["domain"] = datas['domain']
        zxc["photo"] = None
        zxc["status"] = datas['status']
    else:
        zxc['sex'] = ''
        zxc["nickname"] = ''
        zxc["domain"] = ''
        zxc["photo"] = ''
        zxc["status"] = ''
    zxc["city"] = 'Taraz'
    zxc["county"] = 'Kz'
    zxc["checked"] = False
    new_response = requests.post(
        'http://localhost:8000/vk/user/add',
        data=zxc,
    )
    get_groups_to_user()
    new_response = requests.put(
        'http://localhost:8000/vk/user/add',
        data={"user_id": datas['id'], "checked": True},
    )

def add_ban():
        try:
            domain_name = data.domain_name
            response = requests.post(f"http://127.0.0.1:8000/vk/auth/bad_word/add", data={'bad_word': slovar_dislpay.get("1.0", END)})
            res = response.json()
            slovar_dislpay.delete(1.0, END)
            slovar_dislpay.insert(1.0, f'{res["Post"]}\n')
        except:pass

def get_ban():
        domain_name = data.domain_name
        response = requests.get(f"http://127.0.0.1:8000/vk/auth/bad_word/get")
        res = response.json()
        slovar_dislpay.delete(1.0, END)
        slovar_dislpay.insert(1.0, f'{res}\n')


ttt = multiprocessing.Process(target=data.run)
sss = multiprocessing.Process(target=fast_start)
zzz = multiprocessing.Process(target=users_add_only)
new_data = Page()


login = Label(login_frame, text="Введите логин", font=40, bg='white')
login.grid(row=0, column=0, stick='we')
login_form = Entry(login_frame, bg='white')
login_form.grid(row=0, column=1, stick='we')
password = Label(login_frame, text='Введите пароль', font=40, bg='white')
password.grid(row=1, column=0, stick='we')
password_form = Entry(login_frame, bg='white')
password_form.grid(row=1, column=1, stick='nswe')
login_button = Button(login_frame, command=send_login, text="Войти", bg='white')
login_button.grid(row=2, column=0, columnspan = 2, sticky = "ew")


domain_button = Button(first_frame, command=to_data_frame, text="Установка данных", bg='white')
domain_button.grid(row=0, column=0, sticky="ew")
group_label = Label(first_frame, text="Группа: ----------", font=40)
group_label.grid(row=0, column=1, columnspan = 1, stick='we')
user_label = Label(first_frame, text="Пользователь: ----------", font=40)
user_label.grid(row=0, column=2, columnspan = 6, stick='we')
button_send = Button(first_frame, command=ttt.start, text="Начать захват данных", bg='white')
button_send.grid(row=1, column=0, stick='nswe')
posts_get_number_button = Button(first_frame, command=data.send_domain, text="Получить данные", bg='white')
posts_get_number_button.grid(row=1, column=1, stick='nswe')
vsego_postov = Label(first_frame, text="Постов:", font=40)
vsego_postov.grid(row=1, column=2, stick='we')
past_button = Button(first_frame, command=data.get_data_past, text="Предыдущая страница", bg='white')
past_button.grid(row=2, column=0, stick='nswe')
next_button = Button(first_frame, command=data.get_data_next, text="Следующая страница", bg='white')
next_button.grid(row=2, column=1, stick='nswe')
auto_button = Button(first_frame, command=sss.start, text="Автоматический режим", bg='white')
auto_button.grid(row=2, column=2, stick='nswe')
post_button = Button(first_frame, command=data.get_post_id, text="Получить пост", bg='white')
post_button.grid(row=3, column=1, stick='nswe')
post_form = Entry(first_frame, bg='white')
post_form.grid(row=3, column=2, stick='we')
display_button = Button(first_frame, command=display_open, text="Открыть дисплей", bg='white')
display_button.grid(row=3, column=0, stick='nswe')
level = Scale(first_frame, from_=1, to=3, orient=HORIZONTAL)
level.grid(row=4, column=0, stick='nswe')
lsa_posts = Button(first_frame, command=new_data.fast_analyze, text="LSA - постов", bg='white')
lsa_posts.grid(row=4, column=1, stick='nswe')
lsa_comments = Button(first_frame, command=new_data.fast_analyze_comments, text="LSA - комментариев", bg='white')
lsa_comments.grid(row=4, column=2, stick='nswe')
full_analyze = Button(first_frame, command=new_data.run, text="Анализ словоформы", bg='white')
full_analyze.grid(row=5, column=0, stick='nswe')
user_analyze = Button(first_frame, command=zzz.start, text="Анализ пользователя", bg='white')
user_analyze.grid(row=5, column=1, stick='nswe')
slovar_open_button = Button(first_frame, command=slovar_open, text="Управление слов", bg='white')
slovar_open_button.grid(row=5, column=2, stick='nswe')


slovar_dislpay = Text(slovar_frame, width=50, height=8)
slovar_dislpay.grid(row=0, column=0, columnspan=2, stick='ew')
slovar_exit_button = Button(slovar_frame, command=slovar_exit, text="Закрыть", bg='white')
slovar_exit_button.grid(row=2, column=0, stick='nswe')
add_ban = Button(slovar_frame, command=add_ban, text="Добавить слова")
add_ban.grid(row=1, column=0, stick='nswe')
get_ban = Button(slovar_frame, command=get_ban, text="Получить слова")
get_ban.grid(row=1, column=1, stick='nswe')


group_domain_label = Label(data_frame, text="Доменное имя группы", font=40, bg='white')
group_domain_label.grid(row=0, column=0, stick='we')
group_domain_form = Entry(data_frame, bg='white')
group_domain_form.grid(row=0, column=1, stick='we')
user_id_label = Label(data_frame, text='Айди пользователя', font=40, bg='white')
user_id_label.grid(row=1, column=0, stick='we')
user_id_form = Entry(data_frame, bg='white')
user_id_form.grid(row=1, column=1, stick='nswe')
data_sets_save = Button(data_frame, command=data_save, text='Сохранить', bg='green')
data_sets_save.grid(row=2, column=0, columnspan = 2, sticky="ew")
data_sets_exit = Button(data_frame, command=data_sets_exit, text='Закрыть окно', bg='red')
data_sets_exit.grid(row=3, column=0, columnspan = 2, sticky="ew")


display_text = Text(display_frame, width=125, height=27)
display_text.grid(row=0, column=0, rowspan=6, stick='ew')
display_exit = Button(display_frame, command=display_exit, text='Закрыть дисплей', bg='red')
display_exit.grid(row=7, column=0, sticky="nsew")

if __name__ == '__main__':
    try:
        login_app.mainloop()
    except:pass