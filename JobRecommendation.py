from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Line
import re

class JobRecommendationScreen(Screen):
    """Screen to display job recommendations and a floating window for selectable tags."""

    def __init__(self, **kwargs):
        super(JobRecommendationScreen, self).__init__(**kwargs)
        self.selected_tags = []  # Tags passed from InterestedFieldScreen
        self.checked_tags = []   # To track selected CheckBox tags
        self.checked_jobs = []  # To track selected job CheckBoxes

        # Example job data: title and detailed description
        self.jobs_data = [
            {"title": "Software Engineer", "details": "Develop and maintain software applications using Python and Kivy."},
            {"title": "Data Scientist", "details": "Analyze data and build machine learning models for insights."},
            {"title": "AI & Machine Learning", "details": "Create and maintain websites using HTML, CSS, and JavaScript."},
            {"title": "Project Manager", "details": "Manage project timelines, resources, and deliverables."},
            {"title": "UX Designer", "details": "Design user-friendly interfaces with a focus on user experience."}
        ]


        # Root layout
        root_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # === Header Layout (Top Section) === #
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)

        self.choose_title_button = Button(
            text="Choose Your Title",
            size_hint=(0.5, 1),
            font_size=18,
            on_press=self.open_floating_window
        )
        header_layout.add_widget(self.choose_title_button)

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
        self.details_label.bind(size=lambda instance, value: setattr(instance, 'text_size', instance.size))
        right_box.add_widget(self.details_label)
        content_layout.add_widget(right_box)

        root_layout.add_widget(content_layout)

        # === Footer Layout (Bottom Section) === #
        footer_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)

        # Analysis Button: Opens the floating confirmation window
        analysis_button = Button(
            text="Analysis",
            size_hint=(0.5, 1),
            font_size=18,
            background_color=(0.5, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            on_press=self.create_apply_confirmation_window  # Correct binding
        )

        # Apply Button: Retains its original functionality
        apply_button = Button(
            text="Apply",
            size_hint=(0.5, 1),
            font_size=18,
            background_color=(0, 0.7, 0.2, 1),  # Green background
            color=(1, 1, 1, 1),
            on_press=self.apply_selected_tags  # Executes the filtering logic
        )

        # Add buttons to the footer layout
        footer_layout.add_widget(analysis_button)
        footer_layout.add_widget(apply_button)

        # Add the footer layout to the root layout
        root_layout.add_widget(footer_layout)

        self.add_widget(root_layout)
        self.create_floating_window()
        self.populate_job_list()

    def load_selected_tags(self, tags):
        """Load tags passed from InterestedFieldScreen."""
        self.selected_tags = tags
        print("Loaded Tags:", self.selected_tags)

    # === Job List Population === #
    def populate_job_list(self, filtered=False):
        """
        Populate the job list with either all jobs or filtered jobs.

        Args:
            filtered (bool): Whether to display the filtered job list. Defaults to False.
        """
        # Clear existing widgets in the job grid layout
        self.job_grid.clear_widgets()

        # Choose the data source: filtered jobs or all jobs
        job_source = self.filtered_jobs_data if filtered else self.jobs_data

        # Check if the filtered data is empty or contains 'No Results'
        if job_source and job_source[0]["title"] == "No Results":
            # Render a single "No Results" label
            no_result_label = Label(
                text="No Results Found",
                font_size=16,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=60
            )
            self.job_grid.add_widget(no_result_label)
            return  # Stop further rendering

        for job in job_source:
            # Create a horizontal box for each job
            job_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)

            # Add a CheckBox to allow job selection
            checkbox = CheckBox(size_hint=(0.2, 1))
            checkbox.bind(active=lambda checkbox, state, j=job["title"]: self.toggle_job_selection(j, state))

            # Add a button to display the job title
            job_button = Button(
                text=job["title"],
                size_hint=(0.8, 1),
                font_size=16,
                color=(0, 0, 0, 1),
                background_normal='',  # Remove default button styling
                background_color=(0.9, 0.9, 0.9, 1)  # Light gray background
            )
            # Bind a function to display job details when the button is pressed
            job_button.bind(on_press=lambda instance, j=job: self.show_job_details(j))

            # Add the CheckBox and Button to the job box
            job_box.add_widget(checkbox)
            job_box.add_widget(job_button)

            # Add the job box to the job grid
            self.job_grid.add_widget(job_box)

    def show_job_details(self, job):
        """Display the selected job's details on the right side."""
        self.details_label.text = f"[b]{job['title']}[/b]\n\n{job['details']}"
        self.details_label.markup = True

    # === Floating Window === #
    def create_floating_window(self):
        self.floating_window = FloatLayout(size_hint=(1, 1))
        self.floating_window_window = BoxLayout(
            orientation='vertical',
            size_hint=(0.6, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=20,
            spacing=10
        )
        with self.floating_window_window.canvas.before:
            Color(0.7, 0.7, 0.7, 0.95)
            self.bg_rect = Rectangle(size=self.floating_window_window.size, pos=self.floating_window_window.pos)
        self.floating_window_window.bind(size=self.update_rect, pos=self.update_rect)

        self.floating_window_window.add_widget(Label(
            text="Select Your Tags", font_size=20, bold=True, color=(0, 0, 0, 1),
            size_hint_y=None, height=40
        ))
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.checkbox_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.checkbox_layout.bind(minimum_height=self.checkbox_layout.setter('height'))
        scroll_view.add_widget(self.checkbox_layout)
        self.floating_window_window.add_widget(scroll_view)

        close_button = Button(
            text="Ok", size_hint_y=None, height=50, font_size=18,
            on_press=lambda x: self.select_OK()
        )

        self.floating_window_window.add_widget(close_button)

        self.floating_window.add_widget(self.floating_window_window)

    def open_floating_window(self, instance):
        """Open the floating window for tag selection."""
        # Remove floating window if it already exists
        if self.floating_window.parent:
            self.remove_widget(self.floating_window)

        # Clear previous checkbox layout
        self.checkbox_layout.clear_widgets()

        for tag in self.selected_tags:
            tag_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

            # Enhanced CheckBox with visual improvements
            checkbox = CheckBox(
                size_hint=(0.2, 1),
                background_checkbox_normal='',
                background_checkbox_down='atlas://data/images/defaulttheme/checkbox_on',
                color=(0.5, 0.5, 0.6, 1)  # Set a visually clear blue checkmark color
            )
            checkbox.bind(active=lambda checkbox, state, t=tag: self.toggle_tag_selection(t, state))

            # Add the label for the tag
            tag_label = Label(
                text=tag,
                size_hint=(0.8, 1),
                font_size=16,
                color=(0, 0, 0, 1)
            )
            tag_box.add_widget(checkbox)
            tag_box.add_widget(tag_label)
            self.checkbox_layout.add_widget(tag_box)

        # Ensure floating window is displayed
        self.add_widget(self.floating_window)

    def toggle_tag_selection(self, tag, state):
        if state and tag not in self.checked_tags:
            self.checked_tags.append(tag)
        elif not state and tag in self.checked_tags:
            self.checked_tags.remove(tag)

    def apply_selected_tags(self, instance):
        """Apply selected tags and selected jobs."""
        print("Selected Tags to Apply:", self.checked_tags)
        print("Selected Jobs to Apply:", self.checked_jobs)

    def update_left_border(self, instance, value):
        self.left_border.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def update_right_border(self, instance, value):
        self.right_border.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def update_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def toggle_job_selection(self, job_title, state):
        """Track selected job titles based on CheckBox states."""
        if state and job_title not in self.checked_jobs:
            self.checked_jobs.append(job_title)
        elif not state and job_title in self.checked_jobs:
            self.checked_jobs.remove(job_title)

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'interested_field_screen'

    def open_filters(self, instance):
        """
        Filter button does nothing.
        """
        print("Filter button clicked")

    def select_OK(self):
        """
        Apply the selected tags and filter the job list.
        If no tags are selected, reset the job list to the original state.
        """
        # Check if any tags are selected
        if not self.checked_tags:
            print("No tags selected, restoring full job list.")
            self.filtered_jobs_data = self.jobs_data  # Restore original job list
            self.populate_job_list(filtered=False)  # Refresh job list with full data
        else:
            # Normalize checked tags: convert to lowercase and replace special symbols
            normalized_tags = [re.sub(r'[^a-z0-9]', ' ', tag.lower()) for tag in self.checked_tags]
            filtered_jobs = []

            # Filter jobs based on checked tags
            for job in self.jobs_data:
                job_title = re.sub(r'[^a-z0-9]', ' ', job['title'].lower())
                if any(tag in job_title for tag in normalized_tags):
                    filtered_jobs.append(job)

            # Update the filtered jobs data
            if filtered_jobs:
                self.filtered_jobs_data = filtered_jobs
            else:
                self.filtered_jobs_data = [
                    {"title": "No Results", "details": "No jobs found for the selected filters."}]

            self.populate_job_list(filtered=True)  # Refresh job list with filtered data

        # Close the floating window
        self.remove_widget(self.floating_window)

    # Floating window of Apply to JobRecommendationScreen
    def create_apply_confirmation_window(self, instance=None):
        """Create a floating confirmation window after Apply button is clicked."""
        self.apply_window = FloatLayout(size_hint=(1, 1))

        window_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.6, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=20,
            spacing=10
        )

        with window_box.canvas.before:
            Color(0.9, 0.9, 0.9, 0.95)  # Light gray background
            self.bg_rect = Rectangle(size=window_box.size, pos=window_box.pos)
        window_box.bind(size=self.update_rect, pos=self.update_rect)

        message_label = Label(
            text="Your selected jobs and tags have been successfully applied!",
            font_size=18,
            color=(0, 0, 0, 1),
            halign='center',
            valign='middle',
            size_hint_y=0.7
        )
        close_button = Button(
            text="OK",
            size_hint_y=0.3,
            font_size=16,
            on_press=lambda x: self.remove_widget(self.apply_window)
        )

        window_box.add_widget(message_label)
        window_box.add_widget(close_button)
        self.apply_window.add_widget(window_box)

        # Add the floating window to the screen
        self.add_widget(self.apply_window)

    # Modify apply_selected_tags method
    def apply_selected_tags(self, instance):
        """
        Print the selected tags and jobs to the console.
        This method does not show any floating windows.
        """
        print("Selected Tags to Apply:", self.checked_tags)
        print("Selected Jobs to Apply:", self.checked_jobs)

