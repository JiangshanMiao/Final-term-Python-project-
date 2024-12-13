import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
import tkinter as tk
from tkinter import filedialog



class MainScreen(Screen):
    """Main screen layout for registration."""
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20, 20, 20])

        # Upper layout for profile and details
        upper_layout = BoxLayout(orientation='horizontal', size_hint_y=0.9, spacing=10)

        # Left panel for profile and contact info
        left_panel = ScrollView(size_hint=(0.4, 1))
        left_content = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        left_content.bind(minimum_height=left_content.setter('height'))
        left_content.add_widget(self.create_profile_section())
        left_content.add_widget(self.create_contact_and_name_section())
        left_panel.add_widget(left_content)

        # Right panel for email/password and additional sections
        right_panel = ScrollView(size_hint=(0.6, 1))
        right_content = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=[10, 20, 10, 10])
        right_content.bind(minimum_height=right_content.setter('height'))

        right_content.add_widget(self.create_email_password_section())  # Email and Password
        right_content.add_widget(self.create_placeholder_section("Resume"))
        right_content.add_widget(self.create_placeholder_section("Work Experience"))
        right_content.add_widget(self.create_placeholder_section("Education"))
        right_content.add_widget(self.create_placeholder_section("Projects & Outside Experience"))
        right_content.add_widget(self.create_placeholder_section("Socials"))
        right_content.add_widget(self.create_placeholder_section("Skills"))
        right_content.add_widget(self.create_placeholder_section("Languages"))

        right_panel.add_widget(right_content)

        # Add panels to upper layout
        upper_layout.add_widget(left_panel)
        upper_layout.add_widget(right_panel)

        # Bottom layout with navigation buttons
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=20, padding=[10, 0, 10, 0])
        back_button = Button(text='Back to Registration', size_hint=(0.5, 1), on_press=self.go_to_registration)
        bottom_layout.add_widget(back_button)

        # Add layouts to the main layout
        main_layout.add_widget(upper_layout)
        main_layout.add_widget(bottom_layout)

        self.add_widget(main_layout)

    def create_profile_section(self):
        """Create the profile picture section with upload button."""
        profile_section = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        self.profile_image = Image(
            source='default_avatar.png' if os.path.exists('default_avatar.png') else '',
            size_hint=(1, 0.8)
        )
        upload_button = Button(text='Upload Photo', size_hint=(1, 0.2), on_press=self.upload_photo)
        profile_section.add_widget(self.profile_image)
        profile_section.add_widget(upload_button)
        return profile_section

    def create_contact_and_name_section(self):
        """Create section for name, phone, location, and job preferences."""
        section = BoxLayout(orientation='vertical', size_hint_y=None, height=400, spacing=10)
        section.add_widget(self.create_labeled_input_field('Name'))
        section.add_widget(self.create_labeled_input_field('Phone'))
        section.add_widget(self.create_labeled_input_field('Location'))
        section.add_widget(self.create_labeled_input_field('Job Preferences'))
        return section

    def create_email_password_section(self):
        """Create the email and password input section with save button."""
        section_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)

        email_field = self.create_labeled_input_field("Email")
        password_field = self.create_labeled_input_field("Password")

        # Save references to input fields
        self.email_input = email_field.children[0]
        self.password_input = password_field.children[0]

        save_button = Button(
            text="Save Email & Password",
            size_hint=(1, None),
            height=50,
            on_press=self.save_email_password
        )

        section_layout.add_widget(email_field)
        section_layout.add_widget(password_field)
        section_layout.add_widget(save_button)
        return section_layout

    def create_labeled_input_field(self, label_text):
        """Helper function to create labeled input fields."""
        field_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=70, spacing=5)
        label = Label(text=label_text, size_hint_y=None, height=20, halign='left', valign='middle', color=(0, 0, 0, 1))
        label.bind(size=self._update_label_alignment)
        input_field = TextInput(hint_text=f"Enter {label_text.lower()}", multiline=False, size_hint_y=None, height=40)
        field_layout.add_widget(label)
        field_layout.add_widget(input_field)
        return field_layout

    def create_placeholder_section(self, title):
        """Create a placeholder section for other fields."""
        section = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=5)

        # Update the label with left alignment
        label = Label(
            text=title,
            size_hint_y=None,
            height=30,
            halign='left',  # Left align text
            valign='middle',  # Vertical alignment
            color=(0, 0, 0, 1)
        )
        label.bind(size=self._update_label_alignment)  # Bind alignment for dynamic size updates

        # Placeholder TextInput
        placeholder = TextInput(
            hint_text=f"Enter {title.lower()} here",
            size_hint_y=None,
            height=100,
            multiline=True
        )

        section.add_widget(label)
        section.add_widget(placeholder)
        return section

    def save_email_password(self, instance):
        """Save the email and password to the LoginScreen's user database."""
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if not email or not password:
            print("Email or password cannot be empty.")
            return

        # Fetch the login screen from the screen manager
        login_screen = self.manager.get_screen('login_screen')

        # Save the credentials
        if hasattr(login_screen, 'user_database'):
            login_screen.user_database[email] = password
            print(f"Email: {email} and password saved successfully.")
            #self.manager.current = 'login_screen'  # Navigate back to login screen
        else:
            print("Error: Login screen or user database not found.")

    def _update_label_alignment(self, instance, value):
        """Update text alignment for labels."""
        instance.text_size = (instance.width, None)  # Set text width for wrapping
        instance.halign = 'left'  # Align text to the left
        instance.valign = 'middle'  # Vertically align text to the middle

    def go_to_registration(self, instance):
        """Navigate back to the login screen."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    def upload_photo(self, instance):
        """Open file chooser to upload a photo."""
        # Create a file chooser that filters for image files
        filechooser = FileChooserListView(filters=['*.png', '*.jpg', '*.jpeg'])

        # Create a popup to contain the file chooser
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup = Popup(title="Select Photo", content=popup_content, size_hint=(0.9, 0.9))

        # Add the file chooser and close button to the popup
        close_button = Button(text="Close", size_hint_y=None, height=40)
        popup_content.add_widget(filechooser)
        popup_content.add_widget(close_button)

        # Bind the close button to dismiss the popup
        close_button.bind(on_press=popup.dismiss)

        # Bind the file selection callback
        filechooser.bind(on_selection=lambda _, selection: self.select_photo(selection, popup))

        # Open the popup
        popup.open()

    def upload_photo(self, instance):
        """Open the system file manager to upload a photo."""

        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")]
        )

        if file_path:
            self.profile_image.source = file_path
            print(f"Photo selected: {file_path}")
