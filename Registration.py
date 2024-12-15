from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    """Login screen that allows users to sign in or navigate to the registration page."""

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Initialize user database to store email and password
        self.user_database = {}

        # Set layout properties
        layout = BoxLayout(orientation='vertical', spacing=10, padding=[50, 100, 50, 100])

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
        email_label.bind(size=email_label.setter('text_size'))

        # Email input field
        self.email_input = TextInput(
            hint_text='Email Address',
            multiline=False,
            size_hint_y=0.2
        )

        # Password label
        password_label = Label(
            text='Password',
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1),  # Black text
            size_hint_y=0.05
        )
        password_label.bind(size=password_label.setter('text_size'))

        # Password input field
        self.password_input = TextInput(
            hint_text='Password',
            multiline=False,
            password=True,
            size_hint_y=0.2
        )

        # Error label for invalid login
        self.error_label = Label(
            text='',
            color=(1, 0, 0, 1),  # Red text for errors
            size_hint_y=0.1
        )

        # Forgot password button
        forgot_password_button = Button(
            text='Forgot your password?',
            background_color=(1, 1, 1, 0),
            color=(0, 0, 0, 1),
            size_hint_y=0.1
        )

        # Sign-in button
        sign_in_button = Button(
            text='Sign in',
            background_color=(0, 0.5, 0.5, 1),
            color=(1, 1, 1, 1),
            size_hint_y=0.2
        )
        sign_in_button.bind(on_press=self.check_credentials)

        # Create a horizontal layout for "Don't have an account?" and "Register" button
        register_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)

        # "Don't have an account?" label
        dont_have_account_label = Label(
            text="Don't have an account?",
            color=(0, 0, 0, 1),
            halign='left',
            valign='middle'
        )
        dont_have_account_label.bind(size=dont_have_account_label.setter('text_size'))

        # Register button
        register_button = Button(
            text="Register",
            background_color=(1, 1, 1, 0),
            color=(0, 0.5, 1, 1),
            halign='left',
            valign='middle',
            size_hint_x=1
        )
        register_button.bind(on_press=self.go_to_register)

        # Add components to the horizontal layout
        register_layout.add_widget(dont_have_account_label)
        register_layout.add_widget(register_button)

        # Add components to the main layout
        layout.add_widget(title_label)
        layout.add_widget(subtitle_label)
        layout.add_widget(email_label)
        layout.add_widget(self.email_input)
        layout.add_widget(password_label)
        layout.add_widget(self.password_input)
        layout.add_widget(self.error_label)
        layout.add_widget(forgot_password_button)
        layout.add_widget(sign_in_button)
        layout.add_widget(register_layout)

        # Add the layout to the screen
        self.add_widget(layout)

    def check_credentials(self, instance):
        """Check if the entered email and password match stored credentials."""
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if not email or not password:
            self.error_label.text = "Email or password cannot be empty."
            return

        if email in self.user_database and self.user_database[email] == password:
            print("Login successful!")
            self.error_label.text = ""  # Clear error message
            self.manager.transition.direction = 'left'
            self.manager.current = 'interested_field_screen'  # Navigate to the next screen
        else:
            self.error_label.text = "Incorrect email or password."

    def go_to_register(self, instance):
        """Navigate to the registration screen."""
        self.manager.transition.direction = 'left'
        self.manager.current = 'main_screen'
