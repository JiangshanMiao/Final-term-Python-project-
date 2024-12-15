from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class WorkExperienceScreen(Screen):
    """Work Experience Form Layout."""
    def __init__(self, **kwargs):
        super(WorkExperienceScreen, self).__init__(**kwargs)
        work_layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20, 20, 20])

        # Adding input fields to the layout
        work_layout.add_widget(self.create_input_field("Company Name:"))
        work_layout.add_widget(self.create_input_field("Location:"))
        work_layout.add_widget(self.create_input_field("Position Title:"))
        work_layout.add_widget(self.create_input_field("Experience:"))
        work_layout.add_widget(self.create_input_field("Start Month:"))
        work_layout.add_widget(self.create_input_field("Start Year:"))
        work_layout.add_widget(self.create_input_field("End Month:"))

        # Checkbox for currently working
        checkbox_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        checkbox_label = Label(text="I currently work here:", size_hint_x=0.8)
        checkbox = CheckBox(size_hint_x=0.2)
        checkbox_layout.add_widget(checkbox_label)
        checkbox_layout.add_widget(checkbox)
        work_layout.add_widget(checkbox_layout)

        # Description field
        work_layout.add_widget(self.create_text_area("Description:"))

        # Buttons for saving or cancelling
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        cancel_button = Button(text="Cancel", on_press=self.return_to_main, background_color=(1, 0, 0, 1))
        ok_button = Button(text="OK", on_press=self.save_work_experience, background_color=(0, 1, 0, 1))
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(ok_button)
        work_layout.add_widget(button_layout)

        self.add_widget(work_layout)

    def create_input_field(self, label_text):
        """Helper function to create labeled text input fields."""
        field_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        label = Label(text=label_text, size_hint_x=0.3)
        input_field = TextInput(hint_text=f"Enter {label_text[:-1].lower()}", multiline=False, size_hint_x=0.7)
        field_layout.add_widget(label)
        field_layout.add_widget(input_field)
        return field_layout

    def create_text_area(self, label_text):
        """Helper function to create labeled text area fields."""
        field_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=150, spacing=10)
        label = Label(text=label_text, size_hint_y=None, height=30)
        text_area = TextInput(hint_text=f"Enter {label_text[:-1].lower()}", multiline=True, size_hint_y=None, height=100)
        field_layout.add_widget(label)
        field_layout.add_widget(text_area)
        return field_layout

    def return_to_main(self, instance):
        """Switch back to the MainScreen."""
        self.manager.transition.direction = 'left'
        self.manager.current = 'main_screen'

    def save_work_experience(self, instance):
        """Handle saving the work experience and return to the MainScreen."""
        print("Work experience saved!")
        self.return_to_main(instance)
