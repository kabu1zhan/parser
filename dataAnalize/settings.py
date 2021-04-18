#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk
from nltk import *
from nltk.corpus import brown
stopwords= nltk.corpus.stopwords.words('russian')
docs =[
"20210413_986023183_HellYeahPlay_АНИМЕ !Аукцион [ Бакуман s1e6-15, Магическая битва s1e16-24 ] https://disk.yandex.ru/i/BvWrSP7Cp2HJHg",
"Сотка - ммм",
"Жалко что все тайтлы были парашей",
"Засранцы с единичками",
"Юбилейная запись аукциона",

"Магическая битва ахуенно смотрелась. Жаль, что самое мясо ещё будет нескоро",
"The intersection graph of paths in trees",
"Graph minors IV: Widths of trees and well-quasi-ordering",
"Graph minors: A survey"
 ]
stem='russian'
#'danish', 'dutch', 'english', 'finnish', 'french', 'german', 'hungarian', 'italian',
#'norwegian', 'porter', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish'