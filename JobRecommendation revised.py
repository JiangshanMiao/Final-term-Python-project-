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
from pymongo import MongoClient
import csv


#def load_csv(file_path):
#    try:
#        with open(file_path, mode='r', encoding='utf-8') as file:
#            reader = csv.DictReader(file)
 #           jobs = []
 #           for row in reader:
#                print(row)
 #               jobs.append(row)
 #           return jobs
  #  except Exception as e:
 #       print(f" {e}")
  #      return []

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
        self.search_bar = TextInput(
            hint_text="Search for roles, companies, or locations",
            multiline=False,
            size_hint=(0.7, 1)
        )
        self.search_bar.bind(on_text_validate=self.perform_search)
        header_layout.add_widget(self.search_bar)

        # Filters button
        filter_button = Button(
            text="Filters",
            size_hint=(0.3, 1),
            on_press=self.open_filters
        )
        header_layout.add_widget(filter_button)

        main_layout.add_widget(header_layout)

        # Content area
        content_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.9))

        # Job list area
        self.job_list_layout = ScrollView(size_hint=(0.3, 1))
        self.job_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.job_grid.bind(minimum_height=self.job_grid.setter('height'))
        self.job_list_layout.add_widget(self.job_grid)
        content_layout.add_widget(self.job_list_layout)

        # Job details area
        self.details_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint=(0.7, 1))
        self.details_layout.add_widget(Label(
            text="Job details will appear here.",
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)
        ))
        content_layout.add_widget(self.details_layout)

        main_layout.add_widget(content_layout)
        self.add_widget(main_layout)

        # Example job data
        self.jobs = [
           ]

        # Initially display all jobs
        self.filtered_jobs = self.jobs
        self.update_job_list()

        self.load_jobs_from_database()

#        # Load job data from a CSV file
#        file_path = "jobs.csv"
 #       self.jobs = load_csv(file_path)
 #       if not self.jobs:
 #           print("No jobs found in the CSV file or an error occurred.")
#
 #       print(self.jobs)
#
        # Initially display all jobs
#        self.filtered_jobs = self.jobs
#        self.update_job_list()

    def load_jobs_from_database(self):
        try:
            client = MongoClient(
                'mongodb+srv://pvyas1:A23ViuMWmUWxZ4e3@joblistings.ewq53.mongodb.net/?retryWrites=true&w=majority&appName=JobListings',
                tls=True
            )
            db = client["job_database"]
            collection = db["Job_Listings"]
            print("link MongoDB！")

            # Query data
            self.jobs = list(collection.find({}, {
                "_id": 0,
                "title": 1,
                "location": 1,
                "salary": 1,
                "type": 1
            }))
            print(f"Loaded {len(self.jobs)} jobs from the database.")
        except Exception as e:
            print(f" {e}")

    def perform_search(self, instance):
        """Filter job data based on the search query."""
        query = self.search_bar.text.lower().strip()
        self.filtered_jobs = [job for job in self.jobs if
                              query in job['title'].lower() or
                              query in job['location'].lower() or
                              query in job['type'].lower()]
        self.update_job_list()

    def update_job_list(self):
        """Update the job list to display filtered jobs."""
        self.job_grid.clear_widgets()

        for job in self.filtered_jobs:
            job_button = Button(
                text=f"{job['title']}\n{job['location']}\n{job['salary']} - {job['type']}",
                size_hint_y=None,
                height=120,
                font_size=20,
                halign="left",
                valign="middle",
                background_color=(0.9, 0.9, 0.9, 1)
            )
            job_button.text_size = (job_button.width - 20, None)
            job_button.bind(size=self.update_text_alignment)
            job_button.bind(on_press=lambda instance, j=job: self.show_job_details(j))
            self.job_grid.add_widget(job_button)

    def update_text_alignment(self, instance, value):
        instance.text_size = (instance.width - 20, None)

    def show_job_details(self, job):
        """Display job details in the right panel."""
        self.details_layout.clear_widgets()
        self.details_layout.add_widget(Label(text=f"Title: {job['title']}", font_size=16, color=(0, 0, 0, 1)))
        self.details_layout.add_widget(Label(text=f"Location: {job['location']}", font_size=14, color=(0, 0, 0, 1)))
        self.details_layout.add_widget(Label(text=f"Salary: {job['salary']}", font_size=14, color=(0, 0, 0, 1)))
        self.details_layout.add_widget(Label(text=f"Type: {job['type']}", font_size=14, color=(0, 0, 0, 1)))

    def open_filters(self, instance):
        """Placeholder for the filters functionality."""
        print("Filters button clicked!")



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