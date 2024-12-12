from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

import json


class InterestedFieldScreen(Screen):
    def __init__(self, **kwargs):
        super(InterestedFieldScreen, self).__init__(**kwargs)

        # Set window background color to white
        Window.clearcolor = (1, 1, 1, 1)

        # Main layout
        main_layout = GridLayout(cols=1, padding=[10, 40, 10, 10], spacing=10, size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Create title
        title_label = Label(
            text="What kinds of roles are you interested in?",
            font_size=30,
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle',
        )
        title_label.bind(size=title_label.setter('text_size'))
        main_layout.add_widget(title_label)

        # Add space between title and first category
        spacer_label = Label(size_hint_y=None, height=50)  # Adjust height to control spacing
        main_layout.add_widget(spacer_label)

        # Dictionary to store all buttons
        self.buttons_dict = {}

        # Helper function: add a button to the grid layout
        def add_button_to_grid(grid_layout, tag, category):
            button = ToggleButton(
                text=tag,
                size_hint_y=None,
                height=25,  # Button height
                halign='left',
                valign='middle',
                background_color=(1, 1, 1, 1),
                color=(0, 0, 0, 1),
                font_size=13,  # Set font size
                background_normal='',
                background_down='',
            )
            button.bind(state=self.update_button_color)

            # Add a gray rectangular border
            with button.canvas.before:
                Color(0.5, 0.5, 0.5, 1)  # Gray color
                button.border_line = Line(rectangle=(0, 0, button.width, button.height), width=1)

            button.bind(pos=self.update_border, size=self.update_border)
            grid_layout.add_widget(button)

            # Store the button in the dictionary
            if category not in self.buttons_dict:
                self.buttons_dict[category] = []
            self.buttons_dict[category].append(button)

        # Helper function: handle buttons for a category
        def add_category_buttons(category_label, tags, category):
            category_layout = GridLayout(cols=1, spacing=0, padding=0, size_hint_y=None)
            category_layout.bind(minimum_height=category_layout.setter('height'))
            category_layout.add_widget(category_label)

            # Dynamically calculate the number of columns per row
            max_cols_per_row = 4  # Maximum columns
            num_tags = len(tags)
            rows = (num_tags // max_cols_per_row) + (1 if num_tags % max_cols_per_row != 0 else 0)

            buttons_grid = GridLayout(cols=max_cols_per_row, rows=rows, spacing=10, padding=10, size_hint_y=None)
            buttons_grid.bind(minimum_height=buttons_grid.setter('height'))  # Adjust height dynamically

            for tag in tags:
                add_button_to_grid(buttons_grid, tag, category)
            category_layout.add_widget(buttons_grid)
            return category_layout

        # Create and add buttons for each category
        categories = {
            "Technical & Engineering": [
                "Aerospace Engineering",
                "AI & Machine Learning",
                "Architecture & Civil Engineering",
                "Data & Analytics",
                "Developer Relations",
                "DevOps & Infrastructure",
                "Electrical Engineering",
                "Engineering Management",
                "Hardware Engineering",
                "IT & Security",
                "Mechanical Engineering",
                "QA & Testing",
                "Quantitative Finance",
                "Sales & Solution Engineering",
                "Software Engineering",
            ],
            "Finance & Operations & Strategy": [
                "Accounting",
                "Business & Strategy",
                "Consulting",
                "Finance & Banking",
                "Growth & Marketing",
                "Operations & Logistics",
                "Product",
                "Real Estate",
                "Sales & Account Management",
            ],
            "Creative & Design": [
                "Art, Graphics & Animation",
                "Content & Writing",
                "Journalism",
                "Social Media",
                "UI/UX & Design",
            ],
            "Legal & Support & Administration": [
                "Administrative & Executive Assistance",
                "Clerical & Data Entry",
                "Customer Success & Support",
                "Legal & Compliance",
                "People & HR"
            ],
            "Life Sciences": [
                "Biology & Biotech",
                "Lab & Research",
                "Medical, Clinical & Veterinary"
            ]
        }

        for category, tags in categories.items():
            category_label = Label(
                text=category,
                font_size=20,
                bold=True,
                halign='left',
                valign='middle',
                size_hint_y=None,
                height=30,
                color=(0, 0, 0, 1),
            )
            category_label.bind(size=category_label.setter('text_size'))
            category_layout = add_category_buttons(category_label, tags, category)
            main_layout.add_widget(category_layout)

        # Create bottom layout with Back and Generate JSON buttons
        bottom_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10, padding=[10, 10, 10, 10])

        # Back button
        back_button = Button(
            text="Back",
            size_hint=(0.3, 1),
            on_press=self.go_back,
        )

        save_button = Button(
            text="Save and Continue",
            size_hint=(None, None),
            width=150,
            height=25,
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1),
            font_size=13,  # Set font size
            halign='left',
            valign='middle'
        )
        save_button.bind(on_press=self.save_and_continue)

        bottom_layout.add_widget(back_button)
        bottom_layout.add_widget(save_button)
        main_layout.add_widget(bottom_layout)

        # Create a scrollable view
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(main_layout)

        self.add_widget(scroll_view)

    def go_back(self, instance):
        """Handle the back button press."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    def update_button_color(self, instance, value):
        if value == 'down':
            instance.background_color = (0.4, 0.8, 1, 1)  # Color when selected (#66ccff)
        else:
            instance.background_color = (1, 1, 1, 1)  # Color when not selected

    def update_border(self, instance, value):
        instance.border_line.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def generate_json(self, instance):
        data = {}
        for category, buttons in self.buttons_dict.items():
            selected_tags = [button.text for button in buttons if button.state == 'down']
            data[category] = selected_tags

        with open("user_interest_tags.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def save_and_continue(self, instance):
        """Save selected interests and navigate to job recommendations."""
        self.generate_json(instance)
        self.manager.transition.direction = 'left'
        self.manager.current = 'job_recommendation_screen'

