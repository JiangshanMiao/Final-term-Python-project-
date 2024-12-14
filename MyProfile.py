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
from kivy.uix.screenmanager import ScreenManager, Screen

from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class BorderedBox(BoxLayout):
    """Custom BoxLayout with a border and background."""
    def __init__(self, border_thickness=1, border_color=(0, 0, 0, 1), background_color=(1, 1, 1, 1), **kwargs):
        super(BorderedBox, self).__init__(**kwargs)
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.background_color = background_color

        with self.canvas.before:
            Color(*self.border_color)
            self.border = Rectangle(size=self.size, pos=self.pos)
            Color(*self.background_color)
            self.background = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_canvas, pos=self._update_canvas)

    def _update_canvas(self, *args):
        """Update the canvas size and position when the widget's size or position changes."""
        self.border.size = (
            self.size[0] + self.border_thickness * 2,
            self.size[1] + self.border_thickness * 2,
        )
        self.border.pos = (
            self.pos[0] - self.border_thickness,
            self.pos[1] - self.border_thickness,
        )
        self.background.size = self.size
        self.background.pos = self.pos


class MainScreen(Screen):
    """Main screen layout."""
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20, 20, 20])

        upper_layout = BoxLayout(orientation='horizontal', size_hint_y=0.9, spacing=10)

        left_panel = ScrollView(size_hint=(0.4, 1))
        left_content = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        left_content.bind(minimum_height=left_content.setter('height'))
        left_content.add_widget(self.create_profile_section())
        left_content.add_widget(self.create_contact_and_name_section())
        left_panel.add_widget(left_content)

        right_panel = ScrollView(size_hint=(0.6, 1))
        right_content = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=[10, 20, 10, 10])
        right_content.bind(minimum_height=right_content.setter('height'))

        right_content.add_widget(self.create_email_password_section())
        right_content.add_widget(self.create_labeled_bordered_section("Resume", on_press=self.upload_resume))
        right_content.add_widget(self.create_labeled_bordered_section("Work Experience", on_press=self.add_work_experience))
        right_content.add_widget(self.create_labeled_bordered_section("Education"))
        right_content.add_widget(self.create_labeled_bordered_section("Projects & Outside Experience"))
        right_content.add_widget(self.create_labeled_bordered_section("Socials"))
        right_content.add_widget(self.create_labeled_bordered_section("Skills"))
        right_content.add_widget(self.create_labeled_bordered_section("Languages"))


        right_panel.add_widget(right_content)

        upper_layout.add_widget(left_panel)
        upper_layout.add_widget(right_panel)

        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=20, padding=[10, 0, 10, 0])
        back_button = Button(text='Back to Registration', size_hint=(0.5, 1), on_press=self.go_to_registration)
#        save_next_button = Button(text='Save and Continue', size_hint=(0.5, 1), on_press=self.save_and_continue)
        bottom_layout.add_widget(back_button)
#        bottom_layout.add_widget(save_next_button)

        main_layout.add_widget(upper_layout)
        main_layout.add_widget(bottom_layout)

        self.add_widget(main_layout)

    def create_profile_section(self):
        profile_section = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        self.profile_image = Image(
            source='default_avatar.png' if os.path.exists('default_avatar.png') else '',
            size_hint=(1, 0.8)
        )
        upload_button = Button(
            text='Upload Photo', size_hint=(1, 0.2),
            on_press=self.upload_photo
        )
        profile_section.add_widget(self.profile_image)
        profile_section.add_widget(upload_button)
        return profile_section

    def create_contact_and_name_section(self):
        contact_name_section = BoxLayout(orientation='vertical', size_hint_y=None, height=400, spacing=10)
        contact_name_section.add_widget(self.create_labeled_input_field('Name'))
#        contact_name_section.add_widget(self.create_labeled_input_field('Email'))
        contact_name_section.add_widget(self.create_labeled_input_field('Phone'))
        contact_name_section.add_widget(self.create_labeled_input_field('Location'))
        contact_name_section.add_widget(self.create_labeled_input_field('Job Preferences'))
        return contact_name_section

    def create_labeled_input_field(self, label_text):
        field_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=70, spacing=5)
        label = Label(text=label_text, size_hint_y=None, height=20, halign='left', valign='middle', color=(0, 0, 0, 1))
        label.bind(size=self._update_label_alignment)
        input_field = TextInput(hint_text=f"Enter {label_text.lower()}", multiline=False, size_hint_y=None, height=40)
        field_layout.add_widget(label)
        field_layout.add_widget(input_field)
        return field_layout

    def _update_label_alignment(self, instance, value):
        instance.text_size = (instance.width, None)
        instance.halign = 'left'
        instance.valign = 'middle'

    def create_labeled_bordered_section(self, title, on_press=None):
        """Create a bordered section with a label and custom functionality."""
        # Allocate more height for Projects & Outside Experience
        height = 200 if title == "Projects & Outside Experience" else 150
        section_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=height, spacing=5)

        # Add a label above the section
        label = Label(text=f"{title}:", size_hint_y=None, height=30, halign='left', valign='middle', color=(0, 0, 0, 1))
        label.bind(size=self._update_label_alignment)
        section_layout.add_widget(label)

        # Set white border for all modules
        bordered_section = BorderedBox(
            orientation='vertical', size_hint_y=None, height=120, spacing=5, padding=5,
            border_thickness=2, border_color=(1, 1, 1, 1), background_color=(1, 1, 1, 1)
        )

        if title in ["Education", "Socials", "Skills", "Languages", "Projects & Outside Experience"]:
            # Input field for these modules
            input_field = TextInput(
                hint_text=f"Enter {title.lower()} here",
                multiline=True,
                size_hint=(1, None),
                height=90
            )
            bordered_section.add_widget(input_field)

            # For Projects & Outside Experience, add a button as well
            if title == "Projects & Outside Experience":
                file_button = Button(
                    text="Upload/Save File (PDF, DOC, DOCX)", size_hint=(1, None), height=30,
                    on_press=self.open_and_save_file
                )
                bordered_section.add_widget(file_button)

        else:
            # Add a button for other sections
            add_button = Button(
                text=f"Add {title}", size_hint=(1, 1),
                on_press=on_press
            )
            bordered_section.add_widget(add_button)

        section_layout.add_widget(bordered_section)
        return section_layout

    def upload_photo(self, instance):
        file_path = self.open_file_dialog(["png", "jpg", "jpeg", "bmp", "gif"])
        if file_path:
            self.profile_image.source = file_path
            self.profile_image.reload()

    def open_and_save_file(self, instance):
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        file_path = askopenfilename(
            title="Select a File",
            filetypes=[("PDF files", "*.pdf"), ("Word files", "*.doc *.docx"), ("All Files", "*.*")]
        )

        if file_path:
            save_path = asksaveasfilename(
                title="Save File As",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("Word files", "*.doc *.docx"), ("All Files", "*.*")]
            )
            if save_path:
                print(f"File saved as: {save_path}")

        root.destroy()

    def upload_resume(self, instance):
        file_path = self.open_file_dialog(["pdf", "doc", "docx"])
        if file_path:
            print(f"Resume uploaded: {file_path}")

    def add_work_experience(self, instance):
        self.manager.current = 'work_experience_screen'

    def open_file_dialog(self, file_types):
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        file_path = askopenfilename(
            title="Select a File",
            filetypes=[(f"{ft.upper()} files", f"*.{ft}") for ft in file_types] if file_types else [("All Files", "*.*")]
        )
        root.destroy()
        return file_path

    def go_to_registration(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'


    #def save_and_continue(self, instance):
        # Save profile data if necessary (e.g., self.save_profile_data())
    #    self.manager.transition.direction = 'left'

    #    self.manager.current = 'interested_field_screen'  # Transition to InterestedFieldScreen



    def create_email_password_section(self):
        """Creates a section for email and password input."""
        section_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)

        email_field = self.create_labeled_input_field("Email")
        password_field = self.create_labeled_input_field("Password")

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

    def save_email_password(self, instance):
        """Saves the email and password to the user database."""
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        print(f"Email: {email}, Password: {password}")

        if not email or not password:
            print("Email or password cannot be empty.")
            return

        # whetehr LoginScreen
        login_screen = self.manager.get_screen('login_screen')

        if hasattr(login_screen, 'user_database'):
            login_screen.user_database[email] = password
            print(f"Email and password saved: {email}")
        else:
            print("Login screen or database not found.")

        for email, password in login_screen.user_database.items():
            print(f"Email: {email}, Password: {password}")







