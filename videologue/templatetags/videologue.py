from django import template
from copy import copy
from django.conf import settings

register = template.Library()

def _booleanize(x):
    return x.lower().strip('"\'') == 'true'

class VideoDisplay(template.Node):
    def __init__(self, video_obj, *args):
        self.video = template.Variable(video_obj)
        self.options = dict(
            size = None,
            autoplay = False,
            dl_links = True,
        )

        prep_options = dict(
            size = lambda x: (x or '').strip('"\''),
            autoplay = _booleanize,
            dl_links = _booleanize,
        )

        for arg in args:
            if '=' not in arg: continue
            name, _, val = arg.partition('=')
            if name in self.options:
                if name in prep_options:
                    self.options[name] = prep_options[name](val)
                else:
                    self.options[name] = val

    def render(self, context):
        size = self.options['size'] or getattr(settings, 'VIDEOLOGUE_VIDEO_SIZE', '320x240')
        width, height = [int(_) for _ in size.split('x')]
        video = self.video.resolve(context)

        tpl = template.loader.get_template('videologue/ttags/html5_video.html')
        dl_tpl = template.loader.get_template('videologue/ttags/html5_video_download_links.html')

        ctx = template.Context(dict(
            video = video,
            height = height,
            width = width,
            FLOWPLAYER = getattr(settings, 'FLOWPLAYER', ''),
            autoplay = self.options['autoplay'],
        ))
        ret = tpl.render(ctx)
        if self.options['dl_links']:
            ret += dl_tpl.render(ctx)
        return ret

@register.tag
def display_video(parser, token):
    '''
    Displays a VideoLogue Video object as an HTML5 Video construct with flash
    fallback using Flowplayer.  Markup based on Croc Camen's
    `Video for Everybody <http://camendesign.com/code/video_for_everybody>`_.

    Usage::

        {% load videologue %}
        {% display_video video  size=size
                                autoplay=(true|false)
                                dl_links=(true|false) %}

        video
            The Video object to display.
            Required

        size
            A string of format 'widthxheight'.
            Default: settings.VIDEOLOGUE_VIDEO_SIZE or 320x240

        autoplay
            Whether or not to enable autoplay
            Default: False

        dl_links
            Whether or not to display the download links.
            Override the template videos/html5_video_download_links.html to
                provide custom download links.
            Default: True

    The keyword arguments (all but the 'video' argument) are optional and can
    appear in any order.

    '''
    tag, _, bits = token.contents.partition(' ')
    return VideoDisplay(*bits.split())
