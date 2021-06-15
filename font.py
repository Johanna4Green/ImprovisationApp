
import sys

# https://www.programcreek.com/python/?CodeExample=get+font

def get_monospace_font():
    """ Get MonospaceFont for OS
    """
    platform = sys.platform

    if 'linux' in platform:
        return 'DejaVuSans-Bold'
    elif 'darwin' in platform:
        return 'Helvetica'
    elif 'freebsd' in platform:
        return 'Bitstream Vera Sans Mono'

    else:
        # windows
        return 'Arial'


os_font = get_monospace_font()





'''
def get_font():
    """Attempts to retrieve a reasonably-looking TTF font from the system.

    We don't make much of an effort, but it's what we can reasonably do without
    incorporating additional dependencies for this task.
    """
    print(sys.platform)
    if sys.platform == 'win32':
        font_names = ['Arial']
    elif sys.platform in ['linux', 'linux2']:
        font_names = ['DejaVuSans-Bold', 'DroidSans-Bold']
    elif sys.platform == 'darwin':
        font_names = ['Menlo', 'Helvetica']

    font = None
    for font_name in font_names:
        try:
            font = ImageFont.truetype(font_name)
            break
        except IOError:
            continue
    print(font)
    return font

system_font = get_font()


def get_os_monospace_font():
    """ Get MonospaceFont for OS
    """
    platform = sys.platform

    if 'linux' in platform:
        return QFont('Monospace', 10)
    elif 'darwin' in platform:
        return QFont('Monaco', 11)
    elif 'freebsd' in platform:
        return QFont('Bitstream Vera Sans Mono', 10)
    else:
        # windows
        return QFont('Courier', 10)  # Consolas ??

    # return QFontDatabase.systemFont(QFontDatabase.FixedFont) ?? 
    '''
