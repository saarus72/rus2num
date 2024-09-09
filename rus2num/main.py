from natasha.extractors import Extractor

from .number import NUMBER


class Rus2Num(Extractor):
    def __init__(self):
        super(Rus2Num, self).__init__(NUMBER)

    @staticmethod
    def __n_digits(n: int):
        return len(str(int(n)))

    @staticmethod
    def __trailing_zeros(n: int):
        """
        Count trailing zeros of a number

        Args:
            n (int): Number

        Returns:
            int: Count of zeros
        """
        cnt = 0
        while n % 10 == 0 and n != 0:
            cnt += 1
            n = n / 10
        return cnt

    def _get_groups(self, text: str):
        """
        Extract a list of numeral matches from a `text`

        Args:
            text (str): Input text

        Returns:
            list: List of match objects according to the `NUMBER` definition
        """
        start = 0
        matches = list(self.parser.findall(text))
        groups, group_matches = [], []
        for i, match in enumerate(matches):
            if i == 0:
                start = match.span.start
            if i == len(matches) - 1:
                next_match = match
            else:
                next_match = matches[i + 1]
            group_matches.append(match.fact)
            if text[match.span.stop : next_match.span.start].strip() or next_match == match:
                groups.append((group_matches, start, match.span.stop))
                group_matches = []
                start = next_match.span.start
        return groups

    def __call__(self, text: str):
        """
        Change numerals on numbers (letters to digits) within a `text`

        Args:
            text (str): Input text

        Returns:
            str: Transformed text
        """
        groups = self._get_groups(text)
        new_text, start = "", 0
        for group in groups:
            new_text += text[start : group[1]]
            nums = []
            prev_tz, prev_mult = 0, None
            for match in group[0]:
                mult = match.multiplier if match.multiplier else 1
                curr_num = (match.int if match.int is not None else 1) + (match.with_half or 0)
                tz = self.__trailing_zeros(curr_num)
                if (
                    tz < prev_tz
                    and not (0 < mult < 1 and prev_mult > 1)
                    and not (mult > 1 and 0 < prev_mult < 1)
                    and (mult >= prev_mult if (mult > 1 or prev_mult > 1) else mult <= prev_mult)
                    and curr_num != 0
                    and self.__n_digits(curr_num) < self.__n_digits(nums[0][0])
                    and self.__n_digits(curr_num) <= prev_tz
                ):
                    nums[0] = (nums[0][0] + curr_num, mult)
                else:
                    nums.insert(0, (curr_num, mult))
                prev_mult, prev_tz = mult, tz
            prev_mult = None
            new_nums = []
            for num, mult in nums:
                if mult == 10**-1:
                    power = 1
                elif mult == 10**-2:
                    power = 2
                elif mult == 10**-3:
                    power = 3
                else:
                    power = None
                new_num = round(num * mult, power) if power else num * mult
                if not prev_mult or mult <= prev_mult:
                    new_nums.append(new_num)
                else:
                    new_nums[-1] += new_num
                prev_mult = mult
            new_nums = [int(_) if isinstance(_, float) and _ == int(_) else _ for _ in new_nums[::-1]]
            new_text += " ".join(map(str, new_nums))
            start = group[2]
        new_text += text[start:]
        return new_text
