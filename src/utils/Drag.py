from textual.app import App, ComposeResult
from textual.widgets import Label
from textual import events
from textual.geometry import Offset


class SsSs(Label):
    def __init__(self, content="", *, variant=None, expand=False, shrink=False, markup=True, name=None, id=None, classes=None, disabled=False):
        super().__init__(content, variant=variant, expand=expand, shrink=shrink,
                         markup=markup, name=name, id=id, classes=classes, disabled=disabled)
        self.mouse_at_drag_start = None
        self.offset_at_drag_start = None
        self.can_focus = True

    def on_mouse_down(self, event: events.MouseDown) -> None:
        self.focus()

        if not self.parent:
            return
        widget, _ = self.screen.get_widget_at(*event.screen_offset)

        self.mouse_at_drag_start = event.screen_offset
        self.offset_at_drag_start = Offset(
            int(self.styles.offset.x.value),
            int(self.styles.offset.y.value),
        )
        self.capture_mouse()

        self.can_focus = False

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if (
            self.mouse_at_drag_start is not None
            and self.offset_at_drag_start is not None
        ):
            self.styles.offset = (
                self.offset_at_drag_start.x + event.screen_x - self.mouse_at_drag_start.x,
                self.offset_at_drag_start.y + event.screen_y - self.mouse_at_drag_start.y,
            )

    def on_mouse_up(self, event: events.MouseUp) -> None:
        if self.mouse_at_drag_start is None and self.offset_at_drag_start is None:
            return

        self.mouse_at_drag_start = None
        self.offset_at_drag_start = None

        try:
            self.release_mouse()
        except Exception:
            pass

        self.can_focus = True


class ModalApp(App):

    CSS = '''
    Static {
        background:white;
        color:black;
    }
    '''

    def compose(self) -> ComposeResult:
        yield SsSs("Static")


if __name__ == "__main__":
    app = ModalApp()
    app.run()
