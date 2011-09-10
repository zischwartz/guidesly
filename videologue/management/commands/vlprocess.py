import sys, os, subprocess, re
from base64 import b64decode
from tempfile import mktemp
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from videologue.models import ConvertVideo

FFMPEG = getattr(settings, 'VIDEOLOGUE_FFMPEG', 'ffmpeg')
FLVTOOL = getattr(settings, 'VIDEOLOGUE_FLVTOOL', 'flvtool2')

ENCODE_FLV = getattr(settings, 'VIDEOLOGUE_ENCODE_FLV', True)
ENCODE_MP4 = getattr(settings, 'VIDEOLOGUE_ENCODE_MP4', False)
ENCODE_OGV = getattr(settings, 'VIDEOLOGUE_ENCODE_OGV', False)

MP4_TWOPASS = getattr(settings, 'VIDEOLOGUE_MP4_TWOPASS', True)

AUDIO_CODEC = getattr(settings, 'VIDEOLOGUE_AUDIO_CODEC', 'libmp3lame')
AUDIO_BITRATE = getattr(settings, 'VIDEOLOGUE_AUDIO_BITRATE', 32000)
AUDIO_SAMPLING_RATE = getattr(settings, 'VIDEOLOGUE_AUDIO_SAMPLING_RATE', 22050)

VIDEO_SIZE = getattr(settings, 'VIDEOLOGUE_VIDEO_SIZE', '320x240')
IMAGE_SIZE = getattr(settings, 'VIDEOLOGUE_IMAGE_SIZE', '320x240')

LETTERBOX = getattr(settings, 'VIDEOLOGUE_AUTO_LETTERBOX', True)

hq_pre = b64decode('''
Y29kZXI9MQpmbGFncz0rbG9vcApjbXA9K2Nocm9tYQpwYXJ0aXRpb25zPStwYXJ0aTh4OCtwYXJ0aTR
4NCtwYXJ0cDh4OCtwYXJ0Yjh4OAptZV9tZXRob2Q9dW1oCnN1YnE9OAptZV9yYW5nZT0xNgpnPTI1MA
prZXlpbnRfbWluPTI1CnNjX3RocmVzaG9sZD00MAppX3FmYWN0b3I9MC43MQpiX3N0cmF0ZWd5PTIKc
WNvbXA9MC42CnFtaW49MTAKcW1heD01MQpxZGlmZj00CmJmPTQKcmVmcz00CmRpcmVjdHByZWQ9Mwp0
cmVsbGlzPTEKZmxhZ3MyPSticHlyYW1pZCt3cHJlZCttaXhlZF9yZWZzK2RjdDh4OCtmYXN0cHNraXA
K
''')

ipod640_pre = b64decode('''
Y29kZXI9MApiZj0wCnJlZnM9MQpmbGFnczI9LXdwcmVkLWRjdDh4OApsZXZlbD0zMAptYXhyYXRlPTE
wMDAwMDAwCmJ1ZnNpemU9MTAwMDAwMDAK
''')

class Command(BaseCommand):

    help = ('Converts unprocessed videologue avi/mpeg files to flv, mp4, and/or ogv.')

    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **options):
        return process_files()

def process_files():
    """
    Creates flv files for the given video objects.
    """

    convert_videos = ConvertVideo.objects.filter(started=False)

    if not convert_videos:
        print "No videos to convert"

    for convert in convert_videos:

        convert.started = True
        convert.error = ''
        convert.save()

        video_data = {}
        if LETTERBOX:
            try:
                indata = subprocess.Popen([FFMPEG, '-i', convert.video.original_video.path],
                                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                indata = '\n'.join(indata.communicate())
                in_w, in_h = [int(_) for _ in re.search("Video: .* (\d+x\d+)[, ].*", indata, re.I)
                                                .groups()[0].split('x')]
                in_aspect = 1.*in_w/in_h

                out_w, out_h = [int(_) for _ in VIDEO_SIZE.split('x')]
                out_aspect = 1.*out_w/out_h
                conv_height = int(out_w/in_aspect)

                # letterbox or pillarbox?
                letterbox = in_aspect > out_aspect
                # If pillarbox, negate the padding
                pad = (-1+(letterbox*2))*int((out_h-conv_height)/2)

                video_data.update(dict(
                    padbottom = pad if letterbox else 0,
                    padtop = pad if letterbox else 0,
                    padleft = pad if not letterbox else 0,
                    padright = pad if not letterbox else 0,
                    out_aspect = out_aspect,
                    size = '%sx%s' % (out_w, conv_height)
                ))
                video_data['letterboxing'] = ' '.join(
                    str(_)
                        for _ in
                    ['-padbottom', video_data.get('padbottom', 0),
                    '-padtop', video_data.get('padtop', 0),
                    '-padright', video_data.get('padright', 0),
                    '-padleft', video_data.get('padleft', 0),
                    ('-aspect %s' % video_data.get('out_aspect'))
                    if 'out_aspect' in video_data else '']
                )


            except Exception, e:
                # If there are any errors getting video info, don't do letterboxing.
                video_data = {}

        convertvideopng(convert, video_data)
        if ENCODE_FLV:
            convertvideoflv(convert, video_data)
        if ENCODE_MP4:
            convertvideomp4(convert, video_data)
        if ENCODE_OGV:
            convertvideoogv(convert, video_data)

def convertvideoflv(convert, video_data):
    ''' Convert the uploaded video to .flv
    '''

    output = ""

    video = convert.video

    sourcefile = video.original_video.path
    targetfile = NamedTemporaryFile(suffix='.flv')

    ffmpeg = (  '%(ffmpeg)s -y -i "%(infile)s" '
                '-acodec %(audioc)s -ar %(audiosr)s -ab %(audiobr)s '
                '-f flv %(letterboxing)s -s %(size)s %(outfile)s'
                ) % dict(
                    ffmpeg=FFMPEG,
                    infile=sourcefile,
                    audioc=AUDIO_CODEC,
                    audiosr=AUDIO_SAMPLING_RATE,
                    audiobr=AUDIO_BITRATE,
                    letterboxing=video_data.get('letterboxing', ''),
                    size=video_data.get('size', VIDEO_SIZE),
                    outfile=targetfile.name
                )

    if FLVTOOL:
        flvtool = "%s -U %s" % (FLVTOOL, targetfile.name)

    output += "Source : %s\n" % sourcefile
    output += "Target : %s\n" % targetfile.name

    print "------------------ FFMPEG : FLV ----------------\n"
    output += "------------------ FFMPEG : FLV ----------------\n"
    output += "Command: %s\n" % ffmpeg
    f = os.popen(ffmpeg)
    ffmpegresult = f.readline()
    output += ffmpegresult

    if FLVTOOL:
        print "-------------------- FFLVTOOL ------------------\n"
        f = os.popen(flvtool)
        flvtoolresult = f.readline()
        output += "-------------------- FFLVTOOL ------------------\n"
        output += "Command: %s\n" % flvtool
        output += flvtoolresult

    s = os.stat(targetfile.name)
    fsize = s.st_size
    if (fsize == 0):
        output += "Target file is 0 bytes conversion failed?\n"

    convert.error += output
    convert.save()

    video.flv_video.save('%s.flv' % video.pk, File( targetfile ) )
    video.save()

    print output

def convertvideopng(convert, video_data):
    ''' Grab a PNG snapshot of the video
    '''

    output = ""

    video = convert.video

    sourcefile = video.original_video.path
    thumbnailfile = NamedTemporaryFile(suffix='.png')

    grabimage = (   '%(ffmpeg)s -y -i "%(infile)s" '
                    '-vframes 1 -ss 00:00:10 -an '
                    '-vcodec png -f rawvideo '
                    '-s %(size)s %(outfile)s'
                    ) % dict(
                        ffmpeg=FFMPEG,
                        infile=sourcefile,
                        size=IMAGE_SIZE,
                        outfile=thumbnailfile.name
                    )

    print "-------------------- GRAB IMAGE ------------------\n"
    output += "-------------------- GRAB IMAGE ------------------\n"
    output += "Command: %s\n" % grabimage
    f = os.popen(grabimage)
    ffmpegresult = f.readline()
    output += ffmpegresult

    convert.error += output
    convert.save()

    video.image.save('%s_flvthumb.png' % video.pk, File( thumbnailfile) )
    video.save()

    print output

def convertvideomp4(convert, video_data):
    ''' Convert the uploaded video to .mp4
    '''

    output = ""

    video = convert.video

    sourcefile = video.original_video.path
    targetfile = NamedTemporaryFile(suffix='.mp4')

    hq_prefilename = mktemp()
    hq_prefile = open(hq_prefilename, 'w')
    hq_prefile.write(hq_pre)
    hq_prefile.close()
    ipod640_prefilename = mktemp()
    ipod640_prefile = open(ipod640_prefilename, 'w')
    ipod640_prefile.write(ipod640_pre)
    ipod640_prefile.close()

    if MP4_TWOPASS:
        original_files = os.listdir('.') # used later for cleanup
        ffmpeg = (  '%(ffmpeg)s -y -i "%(source)s" '
                    '-vcodec libx264 -fpre "%(hq_prefile)s" -fpre "%(ipod640_prefile)s" '
                    '-an -pass 1 -s %(size)s %(letterboxing)s -f rawvideo '
                    '%(outfile)s'
                    ) % dict(
                        ffmpeg=FFMPEG,
                        source=sourcefile,
                        size=video_data.get('size', VIDEO_SIZE),
                        letterboxing=video_data.get('letterboxing', ''),
                        # For first-pass, use a null output.  Windows needs the
                        #   NUL keyword, linuxy systems can use /dev/null
                        outfile='/dev/null' if os.path.exists('/dev/null') else 'NUL',
                        ipod640_prefile=ipod640_prefilename,
                        hq_prefile=hq_prefilename
                    )

        output += "Source : %s\n" % sourcefile
        output += "Target : %s\n" % targetfile.name

        print "------------- FFMPEG : MP4 : Pass1 -------------\n"
        output += "------------- FFMPEG : MP4 : Pass1 -------------\n"
        output += "Command: %s\n" % ffmpeg
        f = os.popen(ffmpeg)
        ffmpegresult = f.readline()
        output += ffmpegresult


    ffmpeg = (  '%(ffmpeg)s -y -i "%(source)s" '
                '-vcodec libx264 -fpre "%(hq_prefile)s" -fpre "%(ipod640_prefile)s" '
                '-acodec libfaac -ac 2 '
                '%(letterboxing)s '
                '-s %(size)s %(twopass)s %(outfile)s'
                ) % dict(
                    ffmpeg=FFMPEG, source=sourcefile,
                    letterboxing=video_data.get('letterboxing', ''),
                    size=video_data.get('size', VIDEO_SIZE),
                    twopass='-pass 2' if MP4_TWOPASS else '',
                    outfile=targetfile.name,
                    ipod640_prefile=ipod640_prefilename,
                    hq_prefile=hq_prefilename
                )

    output += "Source : %s\n" % sourcefile
    output += "Target : %s\n" % targetfile.name

    header = ("------------- FFMPEG : MP4 : Pass2 -------------\n" if MP4_TWOPASS else
              "----------------- FFMPEG : MP4 -----------------\n")
    print header
    output += header
    output += "Command: %s\n" % ffmpeg
    f = os.popen(ffmpeg)
    ffmpegresult = f.readline()
    output += ffmpegresult

    s = os.stat(targetfile.name)
    fsize = s.st_size
    if (fsize == 0):
        output += "Target file is 0 bytes conversion failed?\n"

    convert.error += output
    convert.save()

    video.mp4_video.save('%s.mp4' % video.pk, File( targetfile ) )
    video.save()

    if MP4_TWOPASS:
        # Cleanup our 2-pass logfiles
        logs = filter(lambda x: x.endswith('.log') and '2pass' in x, set(os.listdir('.'))-set(original_files))
        for log in logs:
            os.unlink(log)

    os.unlink(hq_prefilename)
    os.unlink(ipod640_prefilename)
    print output

def convertvideoogv(convert, video_data):
    ''' Convert the uploaded video to .ogv
    '''

    output = ""

    video = convert.video

    sourcefile = video.original_video.path
    targetfile = NamedTemporaryFile(suffix='.ogv')

    ffmpeg = (  '%(ffmpeg)s -y -i "%(infile)s" '
                '-vcodec libtheora -acodec libvorbis '
                '%(letterboxing)s -s %(size)s %(outfile)s'
                ) % dict(
                    ffmpeg=FFMPEG,
                    infile=sourcefile,
                    letterboxing=video_data.get('letterboxing', ''),
                    size=video_data.get('size', VIDEO_SIZE),
                    outfile=targetfile.name
                )

    output += "Source : %s\n" % sourcefile
    output += "Target : %s\n" % targetfile.name

    print "------------------ FFMPEG : OGV ----------------\n"
    output += "------------------ FFMPEG : OGV ----------------\n"
    output += "Command: %s\n" % ffmpeg
    f = os.popen(ffmpeg)
    ffmpegresult = f.readline()
    output += ffmpegresult

    s = os.stat(targetfile.name)
    fsize = s.st_size
    if (fsize == 0):
        output += "Target file is 0 bytes conversion failed?\n"

    convert.error += output
    convert.save()

    video.ogv_video.save('%s.ogv' % video.pk, File( targetfile ) )
    video.save()

    print output

