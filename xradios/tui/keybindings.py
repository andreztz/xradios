from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next
from prompt_toolkit.key_binding.bindings.focus import focus_previous

from xradios.tui.constants import HELP_TEXT
from xradios.tui.constants import POPUP_BUFFER
from xradios.tui.constants import PROMPT_BUFFER

from xradios.messages import emitter


def kbindings():

    kb = KeyBindings()

    # without eager=True delay is too long
    kb.add(Keys.Escape, eager=True)(
        lambda event: event.app.layout.focus_last()
    )

    @kb.add(Keys.ControlDown)
    def _(event):
        focus_next(event)

    @kb.add(Keys.ControlUp)
    def _(event):
        focus_previous(event)

    @kb.add(Keys.F1)
    def _(event):
        """Launch Help Pop Up."""

        if not event.app.layout.has_focus(POPUP_BUFFER):
            popup_buffer = event.app.layout.get_buffer_by_name(POPUP_BUFFER)
            popup_buffer.update(HELP_TEXT)
            event.app.layout.focus(POPUP_BUFFER)
        else:
            event.app.layout.focus(PROMPT_BUFFER)

    @kb.add(Keys.ControlQ)
    def _(event):
        event.app.exit()
        emitter.emit("KILLALL")

    return kb
