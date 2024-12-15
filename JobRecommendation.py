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
import matplotlib.pyplot as plt
import seaborn as sns
from kivy.uix.image import Image
from io import BytesIO
from kivy.core.image import Image as CoreImage
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from apify_client import ApifyClient
from datetime import datetime
from pymongo import MongoClient
import webbrowser


class JobRecommendationScreen(Screen):
    """Screen to display job recommendations and a floating window for selectable tags."""

    def __init__(self, **kwargs):
        super(JobRecommendationScreen, self).__init__(**kwargs)
        self.selected_tags = []  # Tags passed from InterestedFieldScreen
        self.checked_tags = []   # To track selected CheckBox tags
        self.checked_jobs = []  # To track selected job CheckBoxes


        # Example job data: title and detailed description
        '''self.jobs_data = [
            {"title": "Software1111 Engineer", "details": "Develop and maintain software applications using Python and Kivy."},
            {"title": "Data Scientist", "details": "Analyze data and build machine learning models for insights."},
            {"title": "AI & Machine Learning", "details": "Create and maintain websites using HTML, CSS, and JavaScript."},
            {"title": "Project Manager", "details": "Manage project timelines, resources, and deliverables."},
            {"title": "UX Designer", "details": "Design user-friendly interfaces with a focus on user experience."}
        ]'''
        # === Connect to MongoDB and Fetch Job Data === #
        uri = "mongodb+srv://pvyas1:A23ViuMWmUWxZ4e3@joblistings.ewq53.mongodb.net/?retryWrites=true&w=majority&appName=JobListings"
        client = MongoClient(uri)
        db = client['job_database']  # Replace with your actual database name
        collection = db['Job_Listings']  # Replace with your actual collection name

        # Fetch all job data from MongoDB
        cursor = collection.find()
        documents = list(cursor)

        # Convert the MongoDB documents into a pandas DataFrame
        df = pd.DataFrame(documents)

        # Predefined list of banners (categories)
        banners = [
            "Aerospace Engineering", "AI & Machine Learning", "Architecture & Civil Engineering",
            "Data & Analytics", "Developer Relations", "DevOps & Infrastructure",
            "Electrical Engineering", "Engineering Management", "Hardware Engineering",
            "IT & Security", "Mechanical Engineering", "QA & Testing", "Quantitative Finance",
            "Sales & Solution Engineering", "Software Engineering", "Accounting", "Business & Strategy",
            "Consulting", "Finance & Banking", "Growth & Marketing", "Operations & Logistics", "Product",
            "Real Estate", "Sales & Account Management", "Art, Graphics & Animation", "Content & Writing",
            "Journalism", "Social Media", "UI/UX & Design", "Administrative & Executive Assistance",
            "Clerical & Data Entry", "Customer Success & Support", "Legal & Compliance", "People & HR",
            "Biology & Biotech", "Lab & Research", "Medical, Clinical & Veterinary"
        ]

        # === Process and Clean the Job Titles === #
        # Clean the job titles (lowercase and remove special characters)
        df['cleaned_titles'] = df['positionName'].str.lower().str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)

        # Load a pre-trained SentenceTransformer model to calculate embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Generate embeddings for banners and job titles
        banner_embeddings = model.encode(banners)
        title_embeddings = model.encode(df['cleaned_titles'].tolist())

        # Compute cosine similarity between titles and banners to assign banners
        assigned_banners = []
        for embedding in title_embeddings:
            similarities = cosine_similarity([embedding], banner_embeddings)
            best_match_idx = np.argmax(similarities)
            assigned_banners.append(banners[best_match_idx])

        # Add the assigned banners to the DataFrame
        df['assigned_banner'] = assigned_banners

        if 'external_apply_link' not in df.columns:
            print("Warning: 'external_apply_link' column not found. Assigning default values.")
            df['external_apply_link'] = None

        # === Convert DataFrame to UI-Friendly Format === #
        # Format jobs_data to be used by the UI
        self.jobs_data = [
           # {"title": row['positionName'], "details": row['description'], "assigned_banner": row['assigned_banner']}
            {"title": row['positionName'],
                    "Company": row['company'],
                    "Salary": row['salary'],
                    "Location": row['location'],
                    "Description":row['description'],
                    "Rating": row['rating'],
                    "Apply Here": row['external_apply_link'],
                    "Job_ID":row['id'],
                    "assigned_banner": row['assigned_banner']
                }
            for _, row in df.iterrows()
        ]



        # Root layout
        root_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # === Header Layout (Top Section) === #
        header_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)

        self.choose_title_button = Button(
            text="Choose Your Title",
            size_hint=(0.5, 1),
            font_size=18,
            on_press=self.open_title_selection

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

        # Black border for visual clarity
        with right_box.canvas.before:
            Color(0, 0, 0, 1)  # Black border
            self.right_border = Line(rectangle=(0, 0, right_box.width, right_box.height), width=2)
        right_box.bind(size=self.update_right_border, pos=self.update_right_border)

        # Add ScrollView to enable scrolling
        details_scroll = ScrollView(size_hint=(1, 1))  # ScrollView fills the entire right section

        # Create a Label for job details
        self.details_label = Label(
            text="Select a job to see details here.",
            font_size=16,
            color=(0, 0, 0, 1),
            halign='left',  # Align text to the left
            valign='top',  # Start text from the top
            size_hint_y=None,  # Height adjusts dynamically based on content
            text_size=(details_scroll.width, None)  # Initial width adjustment
        )

        # Dynamically bind text_size to ScrollView width
        details_scroll.bind(
            width=lambda instance, value: setattr(self.details_label, 'text_size', (value, None))
        )

        # Bind texture_size to adjust Label height dynamically
        self.details_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        # Add Label to ScrollView
        details_scroll.add_widget(self.details_label)
        right_box.add_widget(details_scroll)
        content_layout.add_widget(right_box)
        root_layout.add_widget(content_layout)

        # === Footer Layout (Bottom Section) === #
        footer_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)

        # Analysis Button: Opens the floating confirmation window
        # Analysis Button: Opens the larger analysis floating window
        analysis_button = Button(
            text="Analysis",
            size_hint=(0.5, 1),
            font_size=18,
            background_color=(0.5, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            on_press=self.create_analysis_window  # Bind to the new method
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
            # Bind the CheckBox to the toggle_job_selection method with the Job_ID
            checkbox.bind(active=lambda checkbox, state, j=job["Job_ID"]: self.toggle_job_selection(j, state))

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
        """Display the selected job's structured details on the right side."""
        print(job)
        details_text = (
            f"Title: {job.get('title', 'N/A')}[/b]\n\n"
            f"Company: {job.get('Company', 'N/A')}\n"
            f"Salary: {job.get('Salary', 'N/A')}\n"
            f"Location: {job.get('Location', 'N/A')}\n"
            f"Description:\n{job.get('Description', 'N/A')}\n\n"
            f"Rating: {job.get('Rating', 'N/A')}\n\n"
            f"[ref=link]Apply Here[/ref]"

        )
        self.details_label.text = details_text
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

    # Choose your title Bottom
    def open_title_selection(self, instance):
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
        # Connect to MongoDB (replace with your MongoDB connection string)
        mongo_client = MongoClient(
            'mongodb+srv://pvyas1:A23ViuMWmUWxZ4e3@joblistings.ewq53.mongodb.net/?retryWrites=true&w=majority&appName=JobListings')
        db = mongo_client["job_database"]
        collection = db["Job_Listings"]


        # Loop through self.checked_jobs and match with MongoDB data
        for job_id in self.checked_jobs:
            # Find the document with the matching id
            job_data = collection.find_one({"id": job_id}, {"_id": 0, "url": 1})
            if job_data:
                url = job_data.get('url')
                if url:
                    webbrowser.open_new_tab(url)
                    print(f"Opened URL for Job_ID: {job_id}")
                else:
                    print(f"No URL found for Job_ID: {job_id}")
            else:
                print(f"No job found in database for Job_ID: {job_id}")

    def update_left_border(self, instance, value):
        self.left_border.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def update_right_border(self, instance, value):
        self.right_border.rectangle = (instance.x, instance.y, instance.width, instance.height)

    def update_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def toggle_job_selection(self, job_id, state):
        """Track selected job titles based on CheckBox states."""
        if state and job_id not in self.checked_jobs:
            self.checked_jobs.append(job_id)
        elif not state and job_id in self.checked_jobs:
            self.checked_jobs.remove(job_id)

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'interested_field_screen'

    def open_filters(self, instance):
        """
        Filter button does nothing.
        """
        print("Filter button clicked")
        # Initialize the ApifyClient with your API token

        for job_tags in self.checked_tags:
            client = ApifyClient("apify_api_gqVfqJ8JBUJJeFUOEvth89b1DT2kSw4svR1a")
            print(f'getting data f0r : {job_tags}')
            # Prepare the Actor input
            run_input = {
                "position": job_tags,
                "country": "US",
                "location": "San Francisco",
                "maxItems": 20,
                "parseCompanyDetails": False,
                "saveOnlyUniqueItems": True,
                "followApplyRedirects": False,
            }

            # Run the Actor and wait for it to finish
            run = client.actor("hMvNSpz3JnHgl5jkh").call(run_input=run_input)

            # Fetch Actor results from the run's dataset
            items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
            df = pd.DataFrame(items)
            # List of columns to keep
            columns_to_keep = [
                "positionName",
                "salary",
                "jobType",
                "company",
                "location",
                "rating",
                "url",
                "id",
                "postedAt",
                "scrapedAt",
                "description",
                "externalApplyLink",
            ]

            # Keep only the specified columns (if they exist)
            df = df[[col for col in columns_to_keep if col in df.columns]]

            # Convert the DataFrame to a list of dictionaries
            data_dict = df.to_dict(orient="records")

            # Display the resulting DataFrame
            df.head()

            # Convert the DataFrame to a list of dictionaries
            data_dict = df.to_dict(orient="records")

            # Connect to MongoDB (local instance)
            client = MongoClient(
                'mongodb+srv://pvyas1:A23ViuMWmUWxZ4e3@joblistings.ewq53.mongodb.net/?retryWrites=true&w=majority&appName=JobListings')

            # Access the 'job_database' database and the 'Job_Listings' collection
            db = client["job_database"]
            collection = db["Job_Listings"]

            # Insert the data into the collection
            collection.insert_many(data_dict)

            # Query and display the inserted data
            for doc in collection.find():
                print(doc)

        uri = "mongodb+srv://pvyas1:A23ViuMWmUWxZ4e3@joblistings.ewq53.mongodb.net/?retryWrites=true&w=majority&appName=JobListings"
        client = MongoClient(uri)
        db = client['job_database']  # Replace with your actual database name
        collection = db['Job_Listings']  # Replace with your actual collection name

        # Fetch all job data from MongoDB
        cursor = collection.find()
        documents = list(cursor)

        # Convert the MongoDB documents into a pandas DataFrame
        df = pd.DataFrame(documents)

        # Predefined list of banners (categories)
        banners = [
            "Aerospace Engineering", "AI & Machine Learning", "Architecture & Civil Engineering",
            "Data & Analytics", "Developer Relations", "DevOps & Infrastructure",
            "Electrical Engineering", "Engineering Management", "Hardware Engineering",
            "IT & Security", "Mechanical Engineering", "QA & Testing", "Quantitative Finance",
            "Sales & Solution Engineering", "Software Engineering", "Accounting", "Business & Strategy",
            "Consulting", "Finance & Banking", "Growth & Marketing", "Operations & Logistics", "Product",
            "Real Estate", "Sales & Account Management", "Art, Graphics & Animation", "Content & Writing",
            "Journalism", "Social Media", "UI/UX & Design", "Administrative & Executive Assistance",
            "Clerical & Data Entry", "Customer Success & Support", "Legal & Compliance", "People & HR",
            "Biology & Biotech", "Lab & Research", "Medical, Clinical & Veterinary"
        ]

        # === Process and Clean the Job Titles === #
        # Clean the job titles (lowercase and remove special characters)
        df['cleaned_titles'] = df['positionName'].str.lower().str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)

        # Load a pre-trained SentenceTransformer model to calculate embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Generate embeddings for banners and job titles
        banner_embeddings = model.encode(banners)
        title_embeddings = model.encode(df['cleaned_titles'].tolist())

        # Compute cosine similarity between titles and banners to assign banners
        assigned_banners = []
        for embedding in title_embeddings:
            similarities = cosine_similarity([embedding], banner_embeddings)
            best_match_idx = np.argmax(similarities)
            assigned_banners.append(banners[best_match_idx])

        # Add the assigned banners to the DataFrame
        df['assigned_banner'] = assigned_banners
        if 'external_apply_link' not in df.columns:
            print("Warning: 'external_apply_link' column not found. Assigning default values.")
            df['external_apply_link'] = None

        # === Convert DataFrame to UI-Friendly Format === #
        # Format jobs_data to be used by the UI
        self.jobs_data = [
            {"title": row['positionName'],
             "Company": row['company'],
             "Salary": row['salary'],
             "Location": row['location'],
             "Description": row['description'],
             "Rating": row['rating'],
             "Apply Here": row['external_apply_link'],
             "Job_ID": row['id'],
             "assigned_banner": row['assigned_banner']
             }
            for _, row in df.iterrows()
        ]

        self.populate_job_list(filtered=False)

    def select_OK(self):
        """
        Apply the selected tags and reset the job list if no tags are selected.
        """
        # Step 1: Reset checked_tags to sync with CheckBoxes
        self.checked_tags = []
        for child in self.checkbox_layout.children:
            if isinstance(child, BoxLayout):  # CheckBox and Label are inside BoxLayout
                checkbox = child.children[1]  # CheckBox is the second widget in BoxLayout
                label = child.children[0]  # Label is the first widget in BoxLayout
                if isinstance(checkbox, CheckBox) and checkbox.active:
                    self.checked_tags.append(label.text)

        # Step 2: Restore full job list if no tags are selected
        if not self.checked_tags:
            print("No tags selected, restoring full job list.")
            self.filtered_jobs_data = self.jobs_data[:]  # Restore the original job list
            self.populate_job_list(filtered=False)
        else:
            # Normalize checked tags: convert to lowercase and replace special symbols
            normalized_tags = [re.sub(r'[^a-z0-9]', ' ', tag.lower()) for tag in self.checked_tags]
            filtered_jobs = []

            # Step 3: Filter jobs based on checked tags
            for job in self.jobs_data:
                job_title = re.sub(r'[^a-z0-9]', ' ', job['assigned_banner'].lower())
                if any(tag in job_title for tag in normalized_tags):
                    filtered_jobs.append(job)

            # Step 4: Update filtered job list or show "No Results"
            self.filtered_jobs_data = filtered_jobs if filtered_jobs else [{"assigned_banner": "No Results", "Description": ""}]
            self.populate_job_list(filtered=True)

        # Close the floating window
        self.remove_widget(self.floating_window)


    # Analysis Bottom
    def create_analysis_window(self, instance=None):
        """
        Show a larger floating window for the Analysis button.
        This window displays two charts: a bar chart and a pie chart.
        """
        # Create the Analysis floating window
        self.analysis_window = FloatLayout(size_hint=(1, 1))

        # Main window layout
        analysis_box = BoxLayout(
            orientation='vertical',
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=20,
            spacing=10
        )

        # Background styling
        with analysis_box.canvas.before:
            Color(0.8, 0.8, 0.9, 0.95)  # Light blue background
            self.analysis_bg_rect = Rectangle(size=analysis_box.size, pos=analysis_box.pos)
        analysis_box.bind(size=self.update_analysis_rect, pos=self.update_analysis_rect)

        # Step 1: Extract job titles for analysis
        import pandas as pd
        job_titles = [job['assigned_banner'] for job in self.jobs_data]

        # Create a DataFrame where each job title is counted
        df = pd.DataFrame({'Job Title': job_titles})
        title_counts = df['Job Title'].value_counts()

        # Step 2: Generate and display the charts
        bar_chart = self.generate_bar_chart(title_counts)
        analysis_box.add_widget(bar_chart)

        pie_chart = self.generate_pie_chart(title_counts)
        analysis_box.add_widget(pie_chart)

        # Step 3: Add a Close button
        close_button = Button(
            text="Close",
            size_hint_y=None,
            height=50,
            font_size=18,
            on_press=lambda x: self.remove_widget(self.analysis_window)
        )
        analysis_box.add_widget(close_button)

        # Add the Analysis window layout to the floating window
        self.analysis_window.add_widget(analysis_box)

        # Add the floating window to the screen
        self.add_widget(self.analysis_window)

    def generate_bar_chart(self, title_counts):
        """
        Generate a bar chart showing the count of each job title.
        Returns the chart as a Kivy Image widget.
        """
        uri = "mongodb+srv://pvyas1:A23ViuMWmUWxZ4e3@joblistings.ewq53.mongodb.net/?retryWrites=true&w=majority&appName=JobListings"
        client = MongoClient(uri)
        db = client['job_database']  # Replace with your actual database name
        collection = db['Job_Listings']  # Replace with your actual collection name

        # Fetch all job data from MongoDB
        cursor = collection.find()
        documents = list(cursor)

        # Convert the MongoDB documents into a pandas DataFrame
        df = pd.DataFrame(documents)

        # Predefined list of banners (categories)
        banners = [
            "Aerospace Engineering", "AI & Machine Learning", "Architecture & Civil Engineering",
            "Data & Analytics", "Developer Relations", "DevOps & Infrastructure",
            "Electrical Engineering", "Engineering Management", "Hardware Engineering",
            "IT & Security", "Mechanical Engineering", "QA & Testing", "Quantitative Finance",
            "Sales & Solution Engineering", "Software Engineering", "Accounting", "Business & Strategy",
            "Consulting", "Finance & Banking", "Growth & Marketing", "Operations & Logistics", "Product",
            "Real Estate", "Sales & Account Management", "Art, Graphics & Animation", "Content & Writing",
            "Journalism", "Social Media", "UI/UX & Design", "Administrative & Executive Assistance",
            "Clerical & Data Entry", "Customer Success & Support", "Legal & Compliance", "People & HR",
            "Biology & Biotech", "Lab & Research", "Medical, Clinical & Veterinary"
        ]

        # === Process and Clean the Job Titles === #
        # Clean the job titles (lowercase and remove special characters)
        df['cleaned_titles'] = df['positionName'].str.lower().str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)

        # Load a pre-trained SentenceTransformer model to calculate embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Generate embeddings for banners and job titles
        banner_embeddings = model.encode(banners)
        title_embeddings = model.encode(df['cleaned_titles'].tolist())

        # Compute cosine similarity between titles and banners to assign banners
        assigned_banners = []
        for embedding in title_embeddings:
            similarities = cosine_similarity([embedding], banner_embeddings)
            best_match_idx = np.argmax(similarities)
            assigned_banners.append(banners[best_match_idx])

        # Add the assigned banners to the DataFrame
        df['assigned_banner'] = assigned_banners
        if 'external_apply_link' not in df.columns:
            print("Warning: 'external_apply_link' column not found. Assigning default values.")
            df['external_apply_link'] = None

        # === Convert DataFrame to UI-Friendly Format === #
        # Format jobs_data to be used by the UI
        self.jobs_data = [
            {"title": row['positionName'],
             "Company": row['company'],
             "Salary": row['salary'],
             "Location": row['location'],
             "Description": row['description'],
             "Rating": row['rating'],
             "Apply Here": row['external_apply_link'],
             "Job_ID": row['id'],
             "assigned_banner": row['assigned_banner']
             }
            for _, row in df.iterrows()
        ]
        # Create the bar chart
        plt.figure(figsize=(6, 4))
        sns.barplot(x=title_counts.values, y=title_counts.index, palette="viridis")
        plt.title('Distribution of Job Titles', fontsize=12)
        plt.xlabel('Number of Job Titles', fontsize=10)
        plt.ylabel('Job Titles', fontsize=10)

        # Convert the chart to a Kivy-compatible image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return Image(texture=CoreImage(buffer, ext='png').texture)

    def generate_pie_chart(self, title_counts):
        """
        Generate a pie chart showing the proportion of job titles.
        Returns the chart as a Kivy Image widget.
        """
        uri = "mongodb+srv://pvyas1:A23ViuMWmUWxZ4e3@joblistings.ewq53.mongodb.net/?retryWrites=true&w=majority&appName=JobListings"
        client = MongoClient(uri)
        db = client['job_database']  # Replace with your actual database name
        collection = db['Job_Listings']  # Replace with your actual collection name

        # Fetch all job data from MongoDB
        cursor = collection.find()
        documents = list(cursor)

        # Convert the MongoDB documents into a pandas DataFrame
        df = pd.DataFrame(documents)

        # Predefined list of banners (categories)
        banners = [
            "Aerospace Engineering", "AI & Machine Learning", "Architecture & Civil Engineering",
            "Data & Analytics", "Developer Relations", "DevOps & Infrastructure",
            "Electrical Engineering", "Engineering Management", "Hardware Engineering",
            "IT & Security", "Mechanical Engineering", "QA & Testing", "Quantitative Finance",
            "Sales & Solution Engineering", "Software Engineering", "Accounting", "Business & Strategy",
            "Consulting", "Finance & Banking", "Growth & Marketing", "Operations & Logistics", "Product",
            "Real Estate", "Sales & Account Management", "Art, Graphics & Animation", "Content & Writing",
            "Journalism", "Social Media", "UI/UX & Design", "Administrative & Executive Assistance",
            "Clerical & Data Entry", "Customer Success & Support", "Legal & Compliance", "People & HR",
            "Biology & Biotech", "Lab & Research", "Medical, Clinical & Veterinary"
        ]

        # === Process and Clean the Job Titles === #
        # Clean the job titles (lowercase and remove special characters)
        df['cleaned_titles'] = df['positionName'].str.lower().str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)

        # Load a pre-trained SentenceTransformer model to calculate embeddings
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # Generate embeddings for banners and job titles
        banner_embeddings = model.encode(banners)
        title_embeddings = model.encode(df['cleaned_titles'].tolist())

        # Compute cosine similarity between titles and banners to assign banners
        assigned_banners = []
        for embedding in title_embeddings:
            similarities = cosine_similarity([embedding], banner_embeddings)
            best_match_idx = np.argmax(similarities)
            assigned_banners.append(banners[best_match_idx])

        # Add the assigned banners to the DataFrame
        df['assigned_banner'] = assigned_banners
        if 'external_apply_link' not in df.columns:
            print("Warning: 'external_apply_link' column not found. Assigning default values.")
            df['external_apply_link'] = None

        # === Convert DataFrame to UI-Friendly Format === #
        # Format jobs_data to be used by the UI
        self.jobs_data = [
            {"title": row['positionName'],
             "Company": row['company'],
             "Salary": row['salary'],
             "Location": row['location'],
             "Description": row['description'],
             "Rating": row['rating'],
             "Apply Here": row['external_apply_link'],
             "Job_ID": row['id'],
             "assigned_banner": row['assigned_banner']
             }
            for _, row in df.iterrows()
        ]

        # Create the pie chart
        plt.figure(figsize=(6, 4))
        title_counts.plot.pie(autopct='%1.1f%%', startangle=140, colormap='tab20', fontsize=10)
        plt.title('Proportion of Job Titles', fontsize=12)
        plt.ylabel('')  # Remove default y-label

        # Convert the chart to a Kivy-compatible image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return Image(texture=CoreImage(buffer, ext='png').texture)

    def update_analysis_rect(self, instance, value):
        """Update the rectangle size for the analysis window background."""
        self.analysis_bg_rect.size = instance.size
        self.analysis_bg_rect.pos = instance.pos

