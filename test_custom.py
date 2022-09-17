import time
from extractor import NumberExtractor


# text = 'двести тысяч два тракториста и тридцать два чеченца через сорок четыре совы двадцать тридцать'
# text = 'пятьдесят шесть два двадцать три четыре пятьсот два дав десять'
text = "Выплаты за второго-третьего ребенка выросли на пятьсот двадцать пять тысячных процента и составили 90 тысяч рублей"
# text = 'четыре тысячи триста тридцать два девяноста ноль восемь пятьсот'
# text = 'три нуля'
extractor = NumberExtractor()

# print(extractor.calc_number_radix())
a = time.time()
for match in extractor(text):
    print(match.fact)
print((time.time() - a)*1000)
print(extractor.replace(text))
print(extractor.replace_groups(text))
# print(extractor.replace_groups_sa(text))


