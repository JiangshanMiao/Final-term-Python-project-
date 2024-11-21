from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Set layout properties
        self.orientation = 'vertical'
        self.spacing = 15  # Adjust spacing between components
        self.padding = [50, 100, 50, 100]  # Add padding around the layout

        # Set window background color
        Window.clearcolor = (1, 1, 1, 1)  # White background

        # Set window size
        Window.size = (500, 600)  # Width: 500px, Height: 600px

        # Title label
        title_label = Label(
            text="Let's get you hired.",
            font_size=36,
            bold=True,
            color=(0, 0, 0, 1),  # Black text
            size_hint_y=0.1
        )

        # Subtitle label
        subtitle_label = Label(
            text='Apply to thousands of jobs in one-click and track your status.',
            color=(0, 0, 0, 1),  # Black text
            size_hint_y=0.1
        )

        # Email address label
        email_label = Label(
            text='Email Address',
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1),  # Black text
            size_hint_y=0.05
        )
        email_label.bind(size=email_label.setter('text_size'))  # Ensure text aligns to the left

        # Email input field
        email_input = TextInput(
            hint_text='Email Address',
            multiline=False,
            font_size=40,  # Adjust font size
            size_hint_y=0.1
        )


        # Password label
        password_label = Label(
            text='Password',
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1),  # Black text
            size_hint_y=0.05
        )
        password_label.bind(size=password_label.setter('text_size'))  # Ensure text aligns to the left

        # Password input field
        password_input = TextInput(
            hint_text='Password',
            multiline=False,
            password=True,
            font_size=40,  # Adjust font size
            size_hint_y=0.1
        )

        # Forgot password link
        forgot_password_button = Button(
            text='Forgot your password?',
            background_color=(1, 1, 1, 0),  # Transparent background
            color=(0, 0, 0, 1),  # Black text
            size_hint_y=0.1,
            halign='left',
            valign='middle'
        )
        forgot_password_button.bind(size=forgot_password_button.setter('text_size'))  # Ensure text aligns to the left

        # Sign-in button
        sign_in_button = Button(
            text='Sign in',
            background_color=(0, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),  # White text
            size_hint_y=0.25  # Increase height
        )

        # Horizontal layout for "Don't have an account?" and "Register"
        register_layout = BoxLayout(orientation='horizontal', size_hint_y=0.15)

        # "Don't have an account?" label
        dont_have_account_label = Label(
            text="Don't have an account?",
            color=(0, 0, 0, 1),  # Black text
            halign='left',
            valign='middle'
        )
        dont_have_account_label.bind(size=dont_have_account_label.setter('text_size'))  # Ensure text aligns to the left

        # Register button
        register_button = Button(
            text="Register",
            background_color=(1, 1, 1, 0),  # Transparent background
            color=(0, 0.5, 1, 1),  # Light blue text
            halign='left',
            valign='middle',
            size_hint_x=1
        )
        register_button.bind(size=register_button.setter('text_size'))  # Ensure text aligns to the left

        # Add "Don't have an account?" label and "Register" button to horizontal layout
        register_layout.add_widget(dont_have_account_label)
        register_layout.add_widget(register_button)

        # Add components to the main layout
        self.add_widget(title_label)
        self.add_widget(subtitle_label)
        self.add_widget(email_label)
        self.add_widget(email_input)
        self.add_widget(password_label)
        self.add_widget(password_input)
        self.add_widget(forgot_password_button)
        self.add_widget(sign_in_button)
        self.add_widget(register_layout)


class LoginApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    LoginApp().run()
