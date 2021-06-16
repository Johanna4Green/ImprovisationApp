import sys

# https://www.programcreek.com/python/?CodeExample=get+font

def get_monospace_font():
    """ Get MonospaceFont for OS
    """
    platform = sys.platform

    if 'linux' in platform:
        return 'DejaVuSans-Bold'    #'DroidSans-Bold'   'Monospace'
    elif 'darwin' in platform:
        return 'Helvetica'      # 'Menlo'
    elif 'freebsd' in platform:
        return 'Bitstream Vera Sans Mono'

    else:
        # windows
        return 'Arial'

os_font = get_monospace_font()