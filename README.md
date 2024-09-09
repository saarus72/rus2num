# (Russian) numerals to numbers

A small text-to-number package to transform a line like this

    триста тридцать пять с половиной тысяч отборных солдат США и тринадцать целых двадцать одна сотая процента всей экономики мира против полутора русских землекопов-старообрядцев

to a line like this

    335500 отборных солдат США и 13.21 процента всей экономики мира против 1.5 русских землекопов-старообрядцев

Based on **yargy** and **natasha**.

> Locked on `natasha 0.10` because of the bloatness of the later versions.
> May be updated easily to the latest `natasha` with a small change of providing an `Extractor` constructor with a `pymorphy` instance.
>
>     super(Rus2Num, self).__init__(NUMBER, pymorphy2.MorphAnalyzer())

## Installation

`$ pip install rus2num`

## Usage

```python
from run2num import Rus2Num

r2n = Rus2Num()
text = "Выплаты за второго-третьего ребенка выросли на пятьсот двадцать пять тысячных процента и составили 90 тысяч рублей"
print(r2n(text))
# Выплаты за 2-3 ребенка выросли на 0.525 процента и составили 90000 рублей
```

## Comparison

There are but a few packages from namely 
* NVidia's [NeMo](https://github.com/NVIDIA/NeMo-text-processing),
* [Oknolaz](https://github.com/Oknolaz/Russian_w2n),
* [SergeyShk](https://github.com/SergeyShk/Word-to-Number-Russian) and its forks from
    * [averkij](https://github.com/averkij/Word-to-Number-Russian) and
    * [flockentanz](https://github.com/flockentanz/word_to_number_ru).

**NeMo** works well but tends to miss many cases I won't have missed (see the comparison table below).

**Oknolaz** needs to be fed with extracted numbers only and does many mistakes in that case even so bad choice for us.

**SergeyShk** does either
* `replace_groups` — `тысяча сто` to `1100` but `сто двести триста` to `400` or
* `replace` — `сто двести триста` to `100 200 300` but `тысяча сто` to `1000 100`.

It is obvious that addition should be done on decreasing values only so there are some forks to fix it (the overall code is a mess so that I didn't want to do it myself anyway).

**averkij** and **flockentanz** work fine both but have some bugs so I took the second one and fixed them. Also I cover cases like `с половиной` and `одна целая две десятых`.

| Original | 🟡 NeMo TP | 🔴 Oknolaz `replace` | 🔴 SergeyShk `replace_groups` | 🔴 SergeyShk `replace` | 🔴 averkij `replace` | 🔴 flockentanz `replace_groups_sa` | 🟢 **rus2num** |
|--|--|--|--|--|--|--|--|
| `сто двести триста да хоть тысячу раз` | 🟢`100 200 300 да хоть 1000 раз` | 🔴`600000` | 🔴`400 да хоть 1000 раз` | 🟢`100 200 300 да хоть 1000 раз` | 🔴`10200 300 да хоть 1000 раз` | 🟢`100 200 300 да хоть 1000 раз` | 🟢`100 200 300 да хоть 1000 раз` |
| `тысяча сто` | 🟢`1100` | 🟢`1100` | 🟢`1100` | 🔴`1000 100` | 🟢`1100` | 🟢`1100` | 🟢`1100` |
| `я видел сто-двести штук` | 🟡`я видел сто-двести штук` | 🔴`300` | 🟢`я видел 100-200 штук` | 🟢`я видел 100-200 штук` | 🟢`я видел 100-200 штук` | 🟢`я видел 100-200 штук` | 🟢`я видел 100-200 штук` |
| `восемь девятьсот двадцать два пять пять пять тридцать пять тридцать пять, лучше позвонить, чем занимать` | 🟡`восемь 922 пять пять пять 35 35 , лучше позвонить, чем занимать` | 🔴`8` | 🔴`115, лучше позвонить, чем занимать` | 🔴`8 900 20 2 5 5 5 30 5 30 5, лучше позвонить, чем занимать` | 🟢`8 922 5 5 5 35 35, лучше позвонить, чем занимать` | 🟢`8 922 5 5 5 35 35, лучше позвонить, чем занимать` | 🟢`8 922 5 5 5 35 35, лучше позвонить, чем занимать` |
| `три с половиной человека` | 🟡`три с половиной человека` | 🔴`3` | 🟡`3 с половиной человека` | 🟡`3 с половиной человека` | 🟢`3.5 человека` | 🟡`3 с половиной человека` | 🟢`3.5 человека` |
| `миллион сто тысяч сто зайцев` | 🟢`1100100 зайцев` | ❌`list index out of range` | 🔴`1000100100 зайцев` | 🔴`1000000 100000 100 зайцев` | `1100100 зайцев` | 🔴`1000100100 зайцев` | 🟢`1100100 зайцев` |
| `одни двойки и ни одной пятёрки` | 🟡`одни двойки и ни одной пятёрки` | 🟡`No valid number words found! ...` | 🟡`1 двойки и ни 1 пятёрки` | 🟡`1 двойки и ни 1 пятёрки` | 🟡`1 двойки и ни 1 пятёрки` | 🟡`1 двойки и ни 1 пятёрки` | 🟡`1 двойки и ни 1 пятёрки` |
| `без одной минуты два` |🟢 `01:59` | 🔴`2` | 🟢`без 1 минуты 2` | 🟢`без 1 минуты 2` | 🟢`без 1 минуты 2` | 🟢`без 1 минуты 2` | 🟢`без 1 минуты 2` |
| `вторая дача пять соток` | 🟡`вторая дача пять соток` | 🔴`5` | 🟢`2 дача 5 соток` | 🟢`2 дача 5 соток` | 🟢`2 дача 5 соток` | 🟢`2 дача 5 соток` | 🟢`2 дача 5 соток` |
| `двести пятьдесят с половиной тысяч отборных солдат Ирака` | 🟡`250 с половиной 1000 отборных солдат Ирака` | 🔴`250000` | 🟡`250 с половиной 1000 отборных солдат Ирака` | 🔴`200 50 с половиной 1000 отборных солдат Ирака` | 🔴`2050000.5 отборных солдат Ирака` | 🟡`250 с половиной 1000 отборных солдат Ирака` | 🟢`250500 отборных солдат Ирака` |
| `ноль целых ноль десятых минус две целых шесть сотых` | 🟢`0,0 -2,06` | 🟡`Redundant number word! ...` | 🔴`0 целых 0.0 минус 2 целых 0.06` | 🔴`0 целых 0.0 минус 2 целых 0.06` | 🔴`0 целых 0.0 минус 2 целых 0.06` | 🔴`0 целых 0.0 минус 2 целых 0.06` | 🟢`0 минус 2.06` |
