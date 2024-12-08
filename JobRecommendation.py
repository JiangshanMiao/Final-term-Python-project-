from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

class BorderedBox(BoxLayout):
    """Custom BoxLayout with a border and background."""
    def __init__(self, border_color=(0, 0, 0, 1), background_color=(1, 1, 1, 1), **kwargs):
        super(BorderedBox, self).__init__(**kwargs)
        self.border_color = border_color
        self.background_color = background_color

        with self.canvas.before:
            Color(*self.background_color)  # Background color
            self.background = Rectangle(size=self.size, pos=self.pos)
            Color(*self.border_color)  # Border color
            self.border = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_canvas, pos=self.update_canvas)

    def update_canvas(self, *args):
        """Ensure canvas updates correctly and does not overlap text."""
        self.background.size = self.size
        self.background.pos = self.pos
        self.border.size = self.size
        self.border.pos = self.pos



class JobRecommendationScreen(Screen):
    def __init__(self, **kwargs):
        super(JobRecommendationScreen, self).__init__(**kwargs)

        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=20, padding=10)

        # Header: Search bar and filters
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        # Search bar
        search_bar = TextInput(
            hint_text="Search for roles, companies, or locations",
            multiline=False,
            size_hint=(0.7, 1)
        )
        header_layout.add_widget(search_bar)

        # Filters button
        filter_button = Button(
            text="Filters",
            size_hint=(0.3, 1),
            on_press=self.open_filters  # Placeholder for filters functionality
        )
        header_layout.add_widget(filter_button)

        main_layout.add_widget(header_layout)

        # Content area
        content_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.9))

        # Left: Job list (30% width)
        job_list_layout = ScrollView(size_hint=(0.3, 1))
        job_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        job_grid.bind(minimum_height=job_grid.setter('height'))

        # Example jobs
        jobs = [
            {"title": "Sales Development Representative - SDR", "location": "New York, NY, USA", "salary": "$70k-$80k", "type": "Full-Time"},
            {"title": "Software Engineer - Backend", "location": "San Francisco, CA, USA", "salary": "$120k-$150k", "type": "Full-Time"},
            {"title": "Business Analyst", "location": "Boston, MA, USA", "salary": "$80k-$100k", "type": "Part-Time"}
        ]
        for job in jobs:
            job_button = Button(
                text=f"{job['title']}\n{job['location']}\n{job['salary']} - {job['type']}",
                size_hint_y=None,
                height=120,
                font_size=20,
                halign="left",
                valign="middle",
                background_color=(0.9, 0.9, 0.9, 1)  # Light gray background for buttons
            )
            job_button.text_size = (job_button.width - 20, None)
            job_button.bind(size=self.update_text_alignment)
            job_button.bind(on_press=lambda instance, j=job: self.show_job_details(j))
            job_grid.add_widget(job_button)

        job_list_layout.add_widget(job_grid)
        content_layout.add_widget(job_list_layout)

        # Right: Job details (70% width, white background, black border)
        self.details_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(0.7, 1))

        # Add a white background and black border
        with self.details_layout.canvas.before:
            # White background
            Color(1, 1, 1, 1)  # White color for the background
            self.details_background = Rectangle(size=self.details_layout.size, pos=self.details_layout.pos)
            # Black border (drawn larger to create a border effect)
            Color(0, 0, 0, 1)  # Black color for the border
            self.details_border = Line(rectangle=(self.details_layout.pos[0] - 1, self.details_layout.pos[1] - 1,
                                                  self.details_layout.size[0] + 2, self.details_layout.size[1] + 2),
                                       width=2)  # Set width for a consistent thin border

        # Bind the size and position to update dynamically
        self.details_layout.bind(size=self.update_details_canvas, pos=self.update_details_canvas)

        # Add placeholder text to see the content clearly
        self.details_layout.add_widget(Label(
            text="Job details will appear here.",
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)  # Black text
        ))
        content_layout.add_widget(self.details_layout)

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

    def update_text_alignment(self, instance, value):
        """Ensure proper text wrapping and alignment for job buttons."""
        instance.text_size = (instance.width - 20, None)
        instance.halign = "left"
        instance.valign = "middle"

    def open_filters(self, instance):
        """Placeholder for filters functionality."""
        print("Filters button clicked!")

    def show_job_details(self, job):
        """Display job details in the right panel."""
        self.details_layout.clear_widgets()
        self.details_layout.add_widget(Label(text=f"Title: {job['title']}", font_size=16, color=(0, 0, 0, 1)))
        self.details_layout.add_widget(Label(text=f"Location: {job['location']}", font_size=14, color=(0, 0, 0, 1)))
        self.details_layout.add_widget(Label(text=f"Salary: {job['salary']}", font_size=14, color=(0, 0, 0, 1)))
        self.details_layout.add_widget(Label(text=f"Type: {job['type']}", font_size=14, color=(0, 0, 0, 1)))
        self.details_layout.add_widget(Label(
            text="Detailed description goes here...",
            font_size=30,
            color=(0, 0, 0, 1)
        ))
    def update_details_background(self, instance, value):
        self.details_background.size = instance.size
        self.details_background.pos = instance.pos

    def update_details_canvas(self, instance, value):
        """Update the size and position of the white background and black border."""
        # Update background size and position
        self.details_background.size = instance.size
        self.details_background.pos = instance.pos

        # Update border size and position (to slightly enclose the background)
        self.details_border.rectangle = (instance.pos[0] - 1, instance.pos[1] - 1,
                                         instance.size[0] + 2, instance.size[1] + 2)

'''class TestApp(App):
    def build(self):
        # Create ScreenManager to manage our screen
        sm = ScreenManager()

        # Add the JobRecommendationScreen to the ScreenManager
        job_recommendation_screen = JobRecommendationScreen(name='job_recommendation_screen')
        sm.add_widget(job_recommendation_screen)

        # Set the current screen to the JobRecommendationScreen
        sm.current = 'job_recommendation_screen'

        return sm

# Run the test app
if __name__ == '__main__':
    TestApp().run()'''