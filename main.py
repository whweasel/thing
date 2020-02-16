for _ in [0]: # IMPORT STATEMENTS
    """ IMPORT STATEMENTS """
    from blessed import Terminal; # "mother" library class, used for debug purposes
    from scrtools import stream; # base class for most common methods
    from scrtools import color; # color class, for support of colors
    from scrtools import colors; # colors class, containing some predefined colors
    from scrtools import symbols; # symbols class, containing some symbols
    import textrpglib as rpg
    import os
    import sys
    os.chdir(sys.path[0])
    pass; # IMPORT STATEMENTS
for _ in [1]: # SCRTOOLS SETTINGS
    """ SCRTOOLS SETTINGS """
    stream.menu_select_keys = ["KEY_Z", "KEY_ENTER"]; # confirmation keys for menus
    stream.menu_cursor_color = colors.red; # color that the cursor will be shown in, for menus
    stream.menu_highlight_color = colors.yellow; # color that selected text will be shown in, for menus
    stream.menu_cursor = symbols.triangle; # string representing what the cursor shall look like.
    stream.echo_escape_keys = ["KEY_X"]; # keys that will bypass the "typewriter" effect for the echo() method, and print the body all at once
    stream.sleep_escape_keys = ["KEY_Z", "KEY_ENTER"]; # sleep escape keys
    stream.default_end = ''; #default value for the end variable. DON'T CHANGE THIS UNLESS YOU KNOW WHAT YOU'RE DOING!

stream.sleep(3000)