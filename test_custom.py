import time
from rus2num import Rus2Num


text = "Выплаты за двести тридцать две тысячи выросли на пятьсот двадцать пять тысячных процента"
extractor = Rus2Num()
t = time.time()
print(extractor(text))
print((time.time() - t) * 1000)


