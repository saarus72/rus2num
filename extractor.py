from number import NUMBER
from natasha.extractors import Extractor


class NumberExtractor(Extractor):
    def __init__(self):
        super(NumberExtractor, self).__init__(NUMBER)

    @staticmethod
    def number_of_digits(number):
        num = (number.int * number.multiplier) if number.multiplier else number.int

        number_of_digits = 0
        while num >= 1:
            num /= 10
            number_of_digits += 1
        return number_of_digits

    def replace(self, text):
        """
        Замена чисел в тексте без их группировки

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
        """
        if text:
            new_text = ""
            start = 0

            for match in self.parser.findall(text):
                if match.fact.multiplier:
                    num = match.fact.int * match.fact.multiplier
                else:
                    num = match.fact.int
                new_text += text[start: match.span.start] + str(num)
                start = match.span.stop
            new_text += text[start:]

            if start == 0:
                return text
            else:
                return new_text
        else:
            return None

    # TODO переписать. Сейчас алгоритм очень трудно воспринимается
    def replace_groups(self, text):
        """
        Замена сгруппированных составных чисел в тексте

        Аргументы:
            text: исходный текст

        Результат:
            new_text: текст с замененными числами
        """
        if text:
            start = 0
            matches = list(self.parser.findall(text))
            groups = []
            group_matches = []

            for i, match in enumerate(matches):
                if i == 0:
                    start = match.span.start
                if i == len(matches) - 1:
                    next_match = match
                else:
                    next_match = matches[i + 1]
                group_matches.append(match.fact)

                # Если условие срабатывает, то значит, что группа завершена
                # Условие:
                # - если между текущим и следующим числом есть что-то в тексте
                # - если число является последним
                # - если у следующего числа разряд меньше, чем у текущего
                # - если следующее число = 0
                if text[match.span.stop: next_match.span.start].strip() \
                        or next_match == match \
                        or self.number_of_digits(match.fact) - self.number_of_digits(next_match.fact) <= 0\
                        or next_match.fact.int == 0:
                    groups.append((group_matches, start, match.span.stop))
                    group_matches = []
                    start = next_match.span.start
            
            new_text = ""
            start = 0

            for group in groups:
                num = 0
                nums = []
                new_text += text[start: group[1]]
                for match in group[0]:
                    curr_num = match.int * match.multiplier if match.multiplier else match.int
                    if match.multiplier:
                        num = (num + match.int) * match.multiplier
                        nums.append(num)
                        num = 0
                    elif num > curr_num or num == 0:
                        num += curr_num
                    else:
                        nums.append(num)
                        num = 0
                if num > 0:
                    nums.append(num)
                new_text += str(sum(nums))
                start = group[2]
            new_text += text[start:]

            if start == 0:
                return text
            else:
                return new_text
        else:
            return None
