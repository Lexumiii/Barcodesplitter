from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.slider import Slider
from pytest import File


class MyApp(App):
    def start_file_listener(self):
        # starting file listener as windows service
        return

    def build(self):

        # create tab
        panel = TabbedPanel()
        panel.default_tab_text = "Config"
        panel_header = TabbedPanelHeader(text="QR-Generation")

        # add content to first tab
        panel.default_tab_content = GridLayout(cols=2, rows=2)

        # add content to second tab
        panel.content.add_widget(
            Button(text="Start", action=self.start_file_listener()))

        # add header to panel
        panel.add_widget(panel_header)

        return panel


if __name__ == "__main__":
    MyApp().run()
