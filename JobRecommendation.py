from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Line, Ellipse


class JobRecommendationScreen(Screen):
    """Screen to display job recommendations and a floating window for selectable tags."""

    def __init__(self, **kwargs):
        super(JobRecommendationScreen, self).__init__(**kwargs)
        self.selected_tags = []  # Tags passed from InterestedFieldScreen
        self.checked_tags = []   # To track selected CheckBox tags

        # Root layout
        root_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # === Header Layout (Top Section) === #
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)

        # Choose Your Title Button
        self.choose_title_button = Button(
            text="Choose Your Title",
            size_hint=(0.5, 1),
            font_size=18,
            on_press=self.open_floating_window
        )
        header_layout.add_widget(self.choose_title_button)

        # Filter Button
        self.filter_button = Button(
            text="Filter",
            size_hint=(0.2, 1),
            font_size=18,
            on_press=self.open_filters
        )
        header_layout.add_widget(self.filter_button)

        root_layout.add_widget(header_layout)

        # === Content Layout (Middle Section) === #
        content_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.8))

        # Left Section: Job List
        left_box = BoxLayout(size_hint=(0.4, 1), padding=5)
        with left_box.canvas.before:
            Color(0, 0, 0, 1)  # Black border
            self.left_border = Line(rectangle=(0, 0, left_box.width, left_box.height), width=2)
        left_box.bind(size=self.update_left_border, pos=self.update_left_border)

        self.job_list_layout = ScrollView()
        self.job_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.job_grid.bind(minimum_height=self.job_grid.setter('height'))
        self.job_list_layout.add_widget(self.job_grid)
        left_box.add_widget(self.job_list_layout)
        content_layout.add_widget(left_box)

        # Right Section: Job Details
        right_box = BoxLayout(orientation='vertical', padding=5, spacing=10, size_hint=(0.6, 1))
        with right_box.canvas.before:
            Color(0, 0, 0, 1)  # Black border
            self.right_border = Line(rectangle=(0, 0, right_box.width, right_box.height), width=2)
        right_box.bind(size=self.update_right_border, pos=self.update_right_border)

        self.details_label = Label(
            text="Select a job to see details here.",
            font_size=16,
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle'
        )
        right_box.add_widget(self.details_label)
        content_layout.add_widget(right_box)

        root_layout.add_widget(content_layout)

        # === Footer Layout (Bottom Section) === #
        footer_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)

        # Back Button
        back_button = Button(
            text="Back",
            size_hint=(0.5, 1),
            font_size=18,
            on_press=self.go_back
        )

        # Apply Button
        apply_button = Button(
            text="Apply",
            size_hint=(0.5, 1),
            font_size=18,
            background_color=(0, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            on_press=self.apply_selected_tags
        )

        footer_layout.add_widget(back_button)
        footer_layout.add_widget(apply_button)
        root_layout.add_widget(footer_layout)

        # Add everything to the screen
        self.add_widget(root_layout)

        # Create the floating window for tags
        self.create_floating_window()

    # === Border Update Methods === #
    def update_left_border(self, instance, value):
        self.left_border.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def update_right_border(self, instance, value):
        self.right_border.rectangle = (instance.x, instance.y, instance.width, instance.height)

    # === Floating Window === #
    def create_floating_window(self):
        """Create a floating window with CheckBoxes for tags."""
        self.floating_window = FloatLayout(size_hint=(1, 1))

        self.floating_window_window = BoxLayout(
            orientation='vertical',
            size_hint=(0.6, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=20,
            spacing=10
        )

        # Gray background
        with self.floating_window_window.canvas.before:
            Color(0.7, 0.7, 0.7, 0.95)
            self.bg_rect = Rectangle(size=self.floating_window_window.size, pos=self.floating_window_window.pos)
        self.floating_window_window.bind(size=self.update_rect, pos=self.update_rect)

        # Title
        self.floating_window_window.add_widget(Label(
            text="Select Your Tags",
            font_size=20,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=40
        ))

        # GridLayout for CheckBoxes
        self.checkbox_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.checkbox_layout.bind(minimum_height=self.checkbox_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(self.checkbox_layout)
        self.floating_window_window.add_widget(scroll_view)

        # Close Button
        close_button = Button(
            text="Ok",
            size_hint_y=None,
            height=50,
            font_size=18,
            on_press=lambda x: self.remove_widget(self.floating_window)
        )
        self.floating_window_window.add_widget(close_button)

        self.floating_window.add_widget(self.floating_window_window)

    def open_floating_window(self, instance):
        """Open floating window with CheckBoxes for selected tags."""
        self.checkbox_layout.clear_widgets()
        self.checked_tags = []

        for tag in self.selected_tags:
            tag_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

            # Custom CheckBox with border for visibility
            checkbox = CheckBox(size_hint=(0.2, 1))
            checkbox.bind(active=lambda checkbox, state, t=tag: self.toggle_tag_selection(t, state))

            # Add canvas instructions for visibility
            with checkbox.canvas.before:
                Color(0.3, 0.3, 0.3, 1)  # Gray border color
                checkbox.outline_rect = Rectangle(size=checkbox.size, pos=checkbox.pos)
            checkbox.bind(size=self.update_checkbox_rect, pos=self.update_checkbox_rect)

            tag_label = Label(text=tag, size_hint=(0.8, 1), font_size=16, color=(0, 0, 0, 1))
            tag_box.add_widget(checkbox)
            tag_box.add_widget(tag_label)
            self.checkbox_layout.add_widget(tag_box)

        self.add_widget(self.floating_window)

    def update_checkbox_rect(self, instance, value):
        """Update the border rectangle for the CheckBox."""
        instance.outline_rect.size = instance.size
        instance.outline_rect.pos = instance.pos

    def toggle_tag_selection(self, tag, state):
        """Track selected tags based on CheckBox states."""
        if state:
            self.checked_tags.append(tag)
        else:
            if tag in self.checked_tags:
                self.checked_tags.remove(tag)

    def apply_selected_tags(self, instance):
        """Apply selected tags."""
        print("Selected Tags to Apply:", self.checked_tags)

    def update_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def load_selected_tags(self, tags):
        """Load tags passed from InterestedFieldScreen."""
        self.selected_tags = tags
        print("Loaded Tags:", self.selected_tags)

    def open_filters(self, instance):
        """Placeholder for filter functionality."""
        print("Filter button pressed!")

    def go_back(self, instance):
        """Navigate back to InterestedFieldScreen."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'interested_field_screen'
