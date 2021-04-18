import tkinter as tk
import json, requests, time, datetime
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
        self.stop_threads=True

    def set_domain(self):
        self.domain_name = domain.get()
        domain_label['text'] = self.domain_name

app = tk.Tk()
app.title('Мониторинг социальной сети Вконтакте')
app.geometry('1080x500')
app.resizable(width=False, height=False)
data = Data()
ttt = Thread(target=data.run)
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
button_stop = Button(frame, command=data.terminate, text="Остановить захват данных")
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

new_data = Page()
t = Thread(target=new_data.run)
def terminate():
    time.sleep(0.6)
    t.terminate()
    t.join()

start_fast_analyze = Button(page2, command=new_data.fast_analyze, text="Латентно-семантический анализ\n постов")
start_fast_analyze.grid(row=0, column=0, stick='nswe')

start_fast_analyze_comments = Button(page2, command=new_data.fast_analyze_comments, text="Латентно-семантический анализ\n комментариев")
start_fast_analyze_comments.grid(row=1, column=0, stick='nswe')

start_slov_analyze = Button(page2, command=t.start, text="Полный анализ")
start_slov_analyze.grid(row=2, column=0, stick='nswe')

start_slov_analyze = Button(page2, command=terminate, text="Остановить полный анализ")
start_slov_analyze.grid(row=3, column=0, stick='nswe')

complex = Button(page2, text="Комплексный анализ")
complex.grid(row=4, column=0, stick='nswe')

back = Button(page2, command=to1_page, text="Вернуться назад")
back.grid()

info_2 = Text(page2)
info_2.grid(row=0, column=1, rowspan=6, stick='we')

on = Label(page2, text='Полный анализ - выкл')
on.grid(row=0, column=2, stick='we')

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
