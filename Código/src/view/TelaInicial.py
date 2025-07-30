from textual.app import App
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Input, Pretty, TextArea
from textual.screen import Screen
from textual.events import InputEvent
from view.TelaEstoque import TelaEstoque

class TelaInicial(App):
    
    CSS_PATH = "css/TelaInicial.tcss"
    
    def on_mount(self):
        self.push_screen(TelaEstoque())
        
