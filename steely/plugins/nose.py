#!/usr/bin/env python3
'''ur nosey'''


import random


__author__ = 'sentriz'
COMMAND = 'nose'
MODIFIERS = "🏻🏼🏽🏾🏿🏿🏾🏽🏼🏻"
NOSE = "👃"


def main(bot, author_id, message, thread_id, thread_type, **kwargs):
    noses = NOSE + "".join(NOSE + mod for mod in MODIFIERS) + "\n"
    rev_noses = "".join(NOSE + mod for mod in MODIFIERS[::-1]) + NOSE + "\n"
    bot.sendMessage((noses + rev_noses) * random.randint(2, 4),
                    thread_id=thread_id, thread_type=thread_type)
