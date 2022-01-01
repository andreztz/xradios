from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.key_binding.bindings.focus import focus_previous

from prompt_toolkit.application import get_app
from prompt_toolkit.filters import Condition
from prompt_toolkit.filters import has_focus

from xradios.tui.constants import HELP_TEXT
from xradios.tui.constants import POPUP_BUFFER
from xradios.tui.constants import COMMAND_LINE_BUFFER


def kbindings():

    def enter_command_mode(app):
        command_buffer = app.layout.get_buffer_by_name(COMMAND_LINE_BUFFER)
        app.layout.focus(command_buffer)

    def leave_command_mode(app):
        app.layout.focus_last()

    def launch_popup(app):
        if not app.layout.has_focus(POPUP_BUFFER):
            popup_buffer = app.layout.get_buffer_by_name(POPUP_BUFFER)
            popup_buffer.update(HELP_TEXT)
            app.layout.focus(POPUP_BUFFER)
        else:
            app.layout.focus(COMMAND_LINE_BUFFER)

    @Condition
    def check_enter_command_mode():
        app = get_app()
        buffer = app.layout.get_buffer_by_name(COMMAND_LINE_BUFFER)
        if app.layout.has_focus(buffer):
            return False
        return True

    @Condition
    def check_leave_command_mode():
        app = get_app()
        buffer = app.layout.get_buffer_by_name(COMMAND_LINE_BUFFER)
        if not app.layout.has_focus(buffer):
            return False
        return buffer.text == ''

    kb = KeyBindings()

    @kb.add(":")
    def _(event):
        """
        Show the commandline
        """
        enter_command_mode(get_app())

    @kb.add(Keys.Escape, eager=True)
    @kb.add(Keys.Backspace, filter=check_leave_command_mode)
    def _(event):
        leave_command_mode(get_app())

    @kb.add(Keys.ControlDown)
    def _(event):
        enter_command_mode(get_app())

    @kb.add(Keys.ControlUp)
    def _(event):
        focus_previous(event)

    @kb.add(Keys.F1)
    def _(event):
        """Launch help pop up."""
        launch_popup(get_app())

    @kb.add(Keys.ControlQ)
    def _(event):
        event.app.exit()

    return kb
