from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import csv


def load_jobs_from_csv(file_path):
    jobs = []


    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)


        for row in csv_reader:
            job = {
                'title': row['title'],
                'location': row['location'],
                'salary': row['salary'],
                'type': row['type']
            }
            jobs.append(job)

    return jobs



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

        def load_jobs_and_categorize(file_path):
            categorized_jobs = {}

            # Load jobs from CSV
            jobs = load_jobs_from_csv(file_path)

            # Group jobs by type (or any other field you prefer)
            for job in jobs:
                job_type = job['type']  # Assuming 'type' is the category
                if job_type not in categorized_jobs:
                    categorized_jobs[job_type] = []
                categorized_jobs[job_type].append(job)

            return categorized_jobs

        # Define categories and tags
        categories = load_jobs_and_categorize('jobs.csv')

        for category, jobs in categories.items():
            tags = [job['title'] for job in jobs]  # Use job titles as tags
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

        # Passing selected tags to the JobRecommendationScreen
        job_screen = self.manager.get_screen('job_recommendation_screen')
        job_screen.apply_selected_tags(selected_tags)

        # Transition to the JobRecommendationScreen
        self.manager.transition.direction = 'left'
        self.manager.current = 'job_recommendation_screen'

