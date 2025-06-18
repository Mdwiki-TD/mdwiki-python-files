#!/usr/bin/python3
"""

python3 core8/pwb.py update_med_views/tests/views

"""
import sys

from update_med_views.views import load_one_lang_views
from update_med_views.bot import get_one_lang_views

titles = [
    "Akágí yitsʼǫǫsii",
    "Atsʼiis naałdzid",
    "Biłhaazhchin (łitsooígíí)",
    "Chʼosh doo yitʼínii",
    "Dichin",
    "Dlóóʼ binaalniih",
    "Dáʼákʼehtah naʼastsʼǫǫsí binághah dah jíjinígíí",
    "Jéíʼádįįh",
    "Káálsiiyin",
    "Naałniih yichʼą́ą́h naabaahígíí bąąh dahooʼaahgo",
    "Níłchʼi ászólí",
    "Tahoniigááh",
    "Tsʼah",
    "Tsʼíʼii noodǫ́zí",
    "Tłʼoh azihii",
    "Yaaʼ nahachagiígíí",
    "Łóódtsoh",
    "Łį́į́ʼ bitsísʼná",
]
# ---
# zz = load_one_lang_views("nv", titles, 2023)
zz = get_one_lang_views("nv", titles, 2023)
# ---
print(zz)
# print(f"{len(zz)=:,}")
