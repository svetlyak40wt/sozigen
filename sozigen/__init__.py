# -*- coding: utf-8 -*-

import os
import os.path
import urllib2
import math
import shelve

import PIL.Image
from StringIO import StringIO

NETWORK_TIMEOUT = 15
SLIDE_DELAY = 15 * 1000
TRANSITION_DELAY = 2 * 1000
CACHE_DIR = '~/.sozi_cache'

_bool_to_string = {
    True: 'true',
    False: 'false'
}

def _quote(text):
    return text.replace('&', '&amp;')

class Row(object):
    def __init__(self, *items, **kwargs):
        self._content = []

        for item in items:
            if isinstance(item, basestring):
                item = Image(item)
            self._content.append(item)

        self.padding = 0
        self.spacing = 10
        self.__dict__.update(kwargs)

        self.width = sum(item.width for item in self._content) + \
            self.padding * 2 + \
            self.spacing * (len(self._content) - 1)
        self.height = max(item.height for item in self._content) + \
            self.padding * 2

    def render(self, x, y):
        x += self.padding

        for item in self._content:
            yield item.render(x, y)
            x += item.width + self.spacing


class Frame(object):
    frame_id = 0

    def __init__(self, *rows, **kwargs):
        if isinstance(rows[0], basestring):
            self.title = _quote(rows[0])
            rows = rows[1:]
        else:
            self.title = None

        self._content = rows

        self.slide_delay = SLIDE_DELAY
        self.transition_delay = TRANSITION_DELAY
        self.padding = 10
        self.spacing = 10
        self.radius = 10
        self.fill_color = 'green'
        self.fill_opacity = 0.2
        self.stroke_width = 1
        self.stroke_color = self.fill_color
        self.stroke_opacity = 0.5
        self.font_size = 72
        self.text_color = 'green'
        self.text_opacity = 0.8
        self.hide_rect = True
        self.clip_rect = False

        self.__dict__.update(kwargs)

        self.width = max(item.width for item in self._content) + \
            self.padding * 2
        self.height = sum(item.height for item in self._content) + \
            self.padding * 2 + \
            self.spacing * (len(self._content) - 1)


    def render(self, x, y):
        current_y = y + self.padding
        current_x = x + self.padding
        current_id = Frame.frame_id
        Frame.frame_id += 1

        yield (
            '<rect id="frame-{id}" '
            'style="fill:{fill_color};stroke:{stroke_color};stroke-width:{stroke_width};'
            'fill-opacity:{fill_opacity};stroke-opacity:{stroke_opacity}" '
            'rx="{radius}" ry="{radius}" x="{x}" y="{y}" '
            'width="{width}" height="{height}"/>'
        ).format(
            id=current_id, x=x, y=y, **self.__dict__
        )
        yield (
            '<ns1:frame ns1:transition-profile="accelerate-decelerate" ns1:transition-duration-ms="{transition_delay}" '
            'ns1:timeout-ms="{slide_delay}" ns1:timeout-enable="true" '
            'ns1:hide="{hide}" ns1:clip="{clip}" ns1:sequence="{id}" ns1:title="" ns1:refid="frame-{id}" />'
        ).format(
            id=current_id,
            hide=_bool_to_string[self.hide_rect],
            clip=_bool_to_string[self.clip_rect],
            **self.__dict__
        )

        for row in self._content:
            yield row.render(current_x, current_y)
            current_y += row.height + self.spacing

        if self.title:
            yield '<text x="{x}" y="{y}" font-size="{font_size}px" fill="{text_color}" opacity="{text_opacity}">{title}</text>'.format(
                x=x + self.padding * 2,
                y=y + self.padding * 2  + self.font_size,
                **self.__dict__
            )


class Image(object):
    _cache = None

    def __init__(self, src):
        self._src = src
        self._width = None
        self._height = None

    @property
    def cache(self):
        if Image._cache is None:
            Image._cache = shelve.open(os.path.expanduser(CACHE_DIR))
        return Image._cache

    @property
    def width(self):
        if self._width is None:
            self._get_dimensions()
        return self._width

    @property
    def height(self):
        if self._height is None:
            self._get_dimensions()
        return self._height

    def _get_dimensions(self):
        if self._src not in self.cache:
            data = urllib2.urlopen(self._src, timeout=NETWORK_TIMEOUT).read()
            img = PIL.Image.open(StringIO(data))
            self.cache[self._src] = img.size

        self._width, self._height = self.cache[self._src]

    def render(self, x, y):
        yield '<image x="{x}" y="{y}" width="{width}" height="{height}" xlink:href="{src}"/>'.format(
            x=x, y=y, width=self.width, height=self.height, src=_quote(self._src)
        )


def _stream(iterable):
    if isinstance(iterable, basestring):
        yield iterable
    else:
        for item in iterable:
            for s in _stream(item):
                yield s


def render(scene):
    def load(resource):
        with open(os.path.join(os.path.dirname(__file__), resource)) as f:
            return f.read()

    module_dir = os.path.dirname(__file__)
    template = load(os.path.join(module_dir, 'template.xml'))
    sozi_js = load(os.path.join(module_dir, 'sozi.js'))
    custom_js = load(os.path.join(module_dir, 'custom.js'))

    return template.format(
        content='\n'.join(_stream(scene.render(0, 0))),
        sozi_js=sozi_js,
        custom_js=custom_js,
    )
