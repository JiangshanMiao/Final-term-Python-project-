from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


class InterestedFieldScreen(Screen):
    """Screen for users to select interested fields (tags)."""

    def __init__(self, **kwargs):
        super(InterestedFieldScreen, self).__init__(**kwargs)

        # Set window background color to white
        Window.clearcolor = (1, 1, 1, 1)

        # Root layout: vertical BoxLayout
        root_layout = BoxLayout(orientation='vertical')

        # Title Label
        title_label = Label(
            text="What kinds of roles are you interested in?",
            font_size=36,
            bold=True,
            size_hint_y=None,
            height=60,
            color=(0, 0, 0, 1)
        )

        # Scrollable content area
        scroll_view = ScrollView(size_hint=(1, 1))
        main_layout = GridLayout(cols=1, spacing=20, padding=[20, 20, 20, 20], size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Dictionary to store all buttons
        self.buttons_dict = {}

        # Helper function: add buttons to a grid
        def add_category_buttons(category, tags):
            # Category Title
            category_label = Label(
                text=category,
                font_size=24,
                bold=True,
                halign='left',
                valign='middle',
                size_hint_y=None,
                height=40,
                color=(0, 0, 0, 1)
            )
            category_label.bind(size=category_label.setter('text_size'))
            main_layout.add_widget(category_label)

            # Grid layout for buttons
            button_grid = GridLayout(cols=3, spacing=15, size_hint_y=None)
            button_grid.bind(minimum_height=button_grid.setter('height'))

            for tag in tags:
                button = ToggleButton(
                    text=tag,
                    size_hint_y=None,
                    height=50,
                    font_size=18,
                    background_color=(1, 1, 1, 1),
                    color=(1, 1, 1, 1),
                    halign='center',
                    valign='middle'
                )
                button.bind(state=self.update_button_color)
                button_grid.add_widget(button)

                # Store buttons by category
                if category not in self.buttons_dict:
                    self.buttons_dict[category] = []
                self.buttons_dict[category].append(button)

            main_layout.add_widget(button_grid)

        # Define categories and tags
        categories = {
            "Technical & Engineering": [
                "Aerospace Engineering", "AI & Machine Learning", "Architecture & Civil Engineering",
                "Data & Analytics", "Developer Relations", "DevOps & Infrastructure",
                "Electrical Engineering", "Engineering Management", "Hardware Engineering",
                "IT & Security", "Mechanical Engineering", "QA & Testing", "Quantitative Finance",
                "Sales & Solution Engineering", "Software Engineering",
            ],
            "Finance & Operations & Strategy": [
                "Accounting", "Business & Strategy", "Consulting", "Finance & Banking",
                "Growth & Marketing", "Operations & Logistics", "Product", "Real Estate",
                "Sales & Account Management",
            ],
            "Creative & Design": [
                "Art, Graphics & Animation", "Content & Writing", "Journalism", "Social Media", "UI/UX & Design",
            ],
            "Legal & Support & Administration": [
                "Administrative & Executive Assistance", "Clerical & Data Entry", "Customer Success & Support",
                "Legal & Compliance", "People & HR"
            ],
            "Life Sciences": [
                "Biology & Biotech", "Lab & Research", "Medical, Clinical & Veterinary"
            ]
        }

        # Add categories and buttons
        for category, tags in categories.items():
            add_category_buttons(category, tags)

        # Add the main layout to the scroll view
        scroll_view.add_widget(main_layout)

        # Bottom button layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=20, padding=[20, 10])
        back_button = Button(
            text="Back",
            font_size=20,
            size_hint=(0.4, 1),
            on_press=self.go_back
        )
        save_button = Button(
            text="Save and Continue",
            font_size=20,
            size_hint=(0.4, 1),
            background_color=(1, 0, 0, 1),
            color=(1, 1, 1, 1),
            on_press=self.save_and_continue
        )
        button_layout.add_widget(back_button)
        button_layout.add_widget(save_button)

        # Combine all layouts
        root_layout.add_widget(title_label)
        root_layout.add_widget(scroll_view)
        root_layout.add_widget(button_layout)
        self.add_widget(root_layout)

    def update_button_color(self, instance, value):
        """Update button color when selected/deselected."""
        if value == 'down':
            instance.background_color = (0.4, 0.8, 1, 1)
        else:
            instance.background_color = (1, 1, 1, 1)

    def go_back(self, instance):
        """Navigate back to the main screen."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_screen'

    def save_and_continue(self, instance):
        """Save selected tags and navigate to JobRecommendationScreen."""
        selected_tags = [btn.text for category, buttons in self.buttons_dict.items()
                         for btn in buttons if btn.state == 'down']
        job_screen = self.manager.get_screen('job_recommendation_screen')
        job_screen.load_selected_tags(selected_tags)

        # Transition: Leftward flip
        self.manager.transition.direction = 'left'
        self.manager.current = 'job_recommendation_screen'
