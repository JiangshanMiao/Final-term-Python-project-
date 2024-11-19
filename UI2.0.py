from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

Initial_Length = 600
Initial_Width = 600
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class JobAppPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.spacing = 10
        self.padding = [50, 20]

        # Title
        self.add_widget(Label(text="Slogan.", font_size=32, size_hint=(1, 0.2), bold=True))
        self.add_widget(Label(text="tips.",
                               font_size=16, size_hint=(1, 0.1)))

        # Input Fields
        self.add_widget(TextInput(hint_text="Email Address", size_hint=(1, 0.1), multiline=False))
        self.add_widget(TextInput(hint_text="Password", size_hint=(1, 0.1), multiline=False))
        self.add_widget(Button(text="Forgot your password?", size_hint=(1, 0.1), color=(0, 0, 1, 1)))

        # Sign In and Register Buttons
        self.add_widget(Button(text="Sign in", size_hint=(1, 0.15), background_color=(0, 0.5, 1, 1)))
        self.add_widget(Button(text="Don't have an account? Register.", size_hint=(1, 0.1), color=(0, 0, 1, 1)))

        # Social Media Buttons
        social_buttons = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, 0.2))
        social_buttons.add_widget(Button(text="G", size_hint=(0.5, 1)))
        social_buttons.add_widget(Button(text="in", size_hint=(0.5, 1)))
        self.add_widget(social_buttons)


class JobApp(App):
    def build(self):
        return JobAppPage()


if __name__ == '__main__':
    JobApp().run()
