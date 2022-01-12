DISPLAY_BUFFER = "display_buffer"
LISTVIEW_BUFFER = "listview_buffer"
COMMAND_LINE_BUFFER = "command_line_buffer"
POPUP_BUFFER = "popup_buffer"

# https://stackoverflow.com/questions/21503865/how-to-denote-that-a-command-line-argument-is-optional-when-printing-usage
HELP_TEXT = """

xradios
-------


- Press `:` to show the commandline.
- Press `Ctrl + Up` or `Ctrl + Down` to move the focus.
- Press `UP` or `Down` to navigate between radio stations
- To close xradios press `Ctrl + q` or `:quit` or `:exit`.
- To close this window, press F1, ESC, or change the focus.


Player commands
---------------

play <line-number>
stop


Search command
---------------

search option=value, option=value, ....

Example:

search order=votes, limit=1000, hidebroken=true


## Search paramters

- name: str
- name_exact: bool (default=false)
- country: str
- country_exact: bool (default=false)
- countrycode: str
- state: str
- state_exact: bool (default=false)
- language: str
- language_exact: bool (default=false)
- tag: str
- tag_exact: bool (default=false)
- codec: str
- bitrate_min: int (default=0)
- bitrate_max: int (default=1000000)
- has_geo_info: bool (default=not set)
- has_extended_info: bool (default=not set)
- is_https: bool (default=not set)
- order: str (default=name)
- reverse: bool (default=false)
- offset: int (default=0)
- limit: int (default=1000000)
- hidebroken: bool (default=false)


List tags
---------

tags


Favorites commands
------------------

favorite-add <line-number>
favorite-rm <line-number>
favorites


Help commands
--------------

help
help <command> # TODO
"""
