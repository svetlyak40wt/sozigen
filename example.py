#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sozigen import *

BASE = 'http://stats.svetlyak.ru/svetlyak.ru/'

DISK = Frame(
    'Disk',
    Row(
        Image(BASE + 'locum.svetlyak.ru-df-day.png'),
        Image(BASE + 'locum.svetlyak.ru-df-week.png'),
    ),
    Row(
        Image(BASE + 'locum.svetlyak.ru-df_inode-day.png'),
        Image(BASE + 'locum.svetlyak.ru-df_inode-week.png'),
    ),
    hide_rect=False,
)

NET = Frame(
    'Network',
    Row(
        Image(BASE + 'locum.svetlyak.ru-if_err_eth0-day.png'),
        Image(BASE + 'locum.svetlyak.ru-if_err_eth0-week.png'),
    ),
    Row(
        Image(BASE + 'locum.svetlyak.ru-if_eth0-day.png'),
        Image(BASE + 'locum.svetlyak.ru-if_eth0-week.png'),
    ),
    hide_rect = False,
)

MYSQL = Frame(
    Frame(
        'MySQL 1',
        Row(
            Image(BASE + 'locum.svetlyak.ru-mysql_bytes-day.png'),
            Image(BASE + 'locum.svetlyak.ru-mysql_bytes-week.png'),
        ),
        Row(
            Image(BASE + 'locum.svetlyak.ru-mysql_queries-day.png'),
            Image(BASE + 'locum.svetlyak.ru-mysql_queries-week.png'),
        ),
        hide_rect=False,
    ),
    Frame(
        'MySQL 2',
        Row(
            Image(BASE + 'locum.svetlyak.ru-mysql_slowqueries-day.png'),
            Image(BASE + 'locum.svetlyak.ru-mysql_slowqueries-week.png'),
        ),
        Row(
            Image(BASE + 'locum.svetlyak.ru-mysql_threads-day.png'),
            Image(BASE + 'locum.svetlyak.ru-mysql_threads-week.png'),
        ),
        hide_rect=False,
    )
)

SCENE = Frame(
    Row(
        Frame(
            DISK,
            NET,
        ),
        MYSQL,
    ),
)


def main():
    with open('example.svg', 'w') as f:
        f.write(render(SCENE))

if __name__ == '__main__':
    main()


