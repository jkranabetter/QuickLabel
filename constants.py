# directory naming
UNLABELLED_FOLDER = 'unlabelled'
LABELLED_FOLDER = 'labelled'

# class names
FOLDERS = ['-1', '0', '1']

# set constants for window size
MAX_WINDOW_HEIGHT = 600
MAX_WINDOW_WIDTH = 600

# set the size of the undo buffer (how many you can go back)
BUFFER_SIZE = 10

KEY_BINDINGS = {
    '97': 'class -1',
    '65': 'class -1',
    '119': 'class 0',
    '87': 'class 0',
    '100': 'class 1',
    '68': 'class 1',
    '117': 'undo',
    '27': 'exit'
}

WINDOW_STRING = 'a = -1(mislabelled)    w = 0(fail)    d = 1(pass)    u = undo'
