from textual.widgets import Header, _header, Button


class Header(Header):
    BINDINGS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_mount(self):
        self.remove_children(_header.HeaderIcon)
        self.mount(Button("X", flat=True, compact=True),
                   before=self.query_one(_header.HeaderTitle))

    def on_button_pressed(self):
        if len(self.app.screen_stack) > 2:
            self.app.pop_screen()
        else:
            self.app.exit()
