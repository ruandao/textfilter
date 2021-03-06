#!/usr/bin/env python
# -*- coding:utf-8 -*-

__all__ = ['DFAFilter']
__author__ = 'observer'
__date__ = '2012.01.05'


class DFAFilter():

    '''Filter Messages from keywords

    Use DFA to keep algorithm perform constantly

    >>> f = DFAFilter()
    >>> f.add("sexy")
    >>> f.filter("hello sexy baby")
    hello **** baby
    '''

    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, path):
        with open(path) as f:
            for keyword in f:
                self.add(keyword.strip())

    def filter(self, message, repl="*"):
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)


def test_first_character():
    gfw = DFAFilter()
    gfw.add("1989年")
    assert gfw.filter("1989", "*") == "1989"


if __name__ == "__main__":
    import time
    D = DFAFilter()

    def test(D, name):
        print(name)
        D.parse("keywords")
        t = time.time()
        print(D.filter("法轮功 我操操操", "*"))
        print(D.filter("针孔摄像机 我操操操", "*"))
        print(D.filter("售假人民币 我操操操", "*"))
        print(D.filter("传世私服 我操操操", "*"))
        print(time.time() - t)
        D.add('AAA')
        print(D.filter('aaa,AAA,aAa,aaAAAaa'))

    test(D, 'DFAFilter')
    test_first_character()

