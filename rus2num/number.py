from yargy import or_, rule
from yargy.interpretation import const, fact
from yargy.pipelines import caseless_pipeline, morph_pipeline
from yargy.predicates import caseless, eq, normalized, type

Number = fact("Number", ["int", "with_half", "multiplier"])
NUMS_RAW = {
    "ноль": 0,
    "нуль": 0,
    "один": 1,
    "полтора": 1.5,
    "два": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
    "двадцать": 20,
    "тридцать": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "шестьдесят": 60,
    "семьдесят": 70,
    "восемьдесят": 80,
    "девяносто": 90,
    "сто": 100,
    "двести": 200,
    "триста": 300,
    "четыреста": 400,
    "пятьсот": 500,
    "шестьсот": 600,
    "семьсот": 700,
    "восемьсот": 800,
    "девятьсот": 900,
}
NUMS_RAW_BIG = {
    "тысяча": 10**3,
    "миллион": 10**6,
    "миллиард": 10**9,
    "триллион": 10**12,
}

DOT = eq(".")
INT = type("INT")
BILLIONTH = rule(caseless_pipeline(["миллиардных", "миллиардная"])).interpretation(const(10**-9))
MILLIONTH = rule(caseless_pipeline(["миллионных", "миллионная"])).interpretation(const(10**-6))
THOUSANDTH = rule(caseless_pipeline(["тысячных", "тысячная"])).interpretation(const(10**-3))
HUNDREDTH = rule(caseless_pipeline(["сотых", "сотая"])).interpretation(const(10**-2))
TENTH = rule(caseless_pipeline(["десятых", "десятая"])).interpretation(const(10**-1))
INTEGER_PART = rule(caseless_pipeline(["целых", "целая"])).interpretation(const(10**0))
THOUSAND = or_(
    rule(caseless("т"), DOT),
    rule(caseless("тыс"), DOT.optional()),
    rule(normalized("тысяча")),
    rule(normalized("тыща")),
).interpretation(const(10**3))
MILLION = or_(rule(caseless("млн"), DOT.optional()), rule(normalized("миллион"))).interpretation(const(10**6))
MILLIARD = or_(rule(caseless("млрд"), DOT.optional()), rule(normalized("миллиард"))).interpretation(const(10**9))
TRILLION = or_(rule(caseless("трлн"), DOT.optional()), rule(normalized("триллион"))).interpretation(const(10**12))
WITH_HALF = (
    or_(
        rule(caseless("с"), normalized("половина")),
    )
    .interpretation(const(0.5))
    .interpretation(Number.with_half)
)
MULTIPLIER = or_(
    BILLIONTH,
    MILLIONTH,
    THOUSANDTH,
    HUNDREDTH,
    TENTH,
    INTEGER_PART,
    THOUSAND,
    MILLION,
    MILLIARD,
    TRILLION,
).interpretation(Number.multiplier)
NUM_RAW_BIG = rule(morph_pipeline(NUMS_RAW_BIG).interpretation(Number.multiplier.normalized().custom(NUMS_RAW_BIG.get)))
NUM_RAW = rule(morph_pipeline(NUMS_RAW).interpretation(Number.int.normalized().custom(NUMS_RAW.get)))
NUM_INT = rule(INT).interpretation(Number.int.custom(int))
NUM = or_(NUM_RAW_BIG, NUM_RAW, NUM_INT)
NUMBER = or_(rule(NUM, WITH_HALF.optional(), MULTIPLIER.optional())).interpretation(Number)
