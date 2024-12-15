THIS CODE WILL TAKE 20 MINUTES TO EXECUTE. EVERYTHING IS WORKING, SO PLEASE BE PATIENT TO SEE THE OUTPUTS.
TO CHECK THE SCRAPED DATA, YOU CAN REFER TO THE CONSOLE.
# Job Recommendation System

## Project Description

This project is a **Job Recommendation System** built using **Python** and the **Kivy Framework** for the user interface. It allows users to:

1. **Register/Login** into the system.
2. Enter personal information, work experience, and job preferences.
3. View personalized job recommendations based on selected tags and job titles.
4. Analyze job distributions using graphical charts.

The application interacts with a **MongoDB database** to fetch and store job-related data. It uses advanced **Natural Language Processing (NLP)** techniques for job title categorization.

---

## Features

1. **Registration/Login System**
   - Users can create accounts and log in securely.
   - Login validation ensures email and password correctness.

2. **User Profile Management**
   - Input and save personal details and work experience.
   - Edit or update information at any time.

3. **Job Recommendations**
   - View job listings fetched from a MongoDB database.
   - Select tags to filter jobs based on preferences.
   - View detailed job descriptions with options to apply.

4. **Job Analysis**
   - Visual analysis (Bar Chart & Pie Chart) of job categories.
   - Helps users understand job availability trends.

5. **Responsive UI**
   - Scrollable views for job listings and detailed descriptions.
   - Intuitive navigation between screens.

---

## Technologies Used

- **Python**: Backend programming.
- **Kivy**: User interface development.
- **MongoDB**: Database for job listings.
- **Sentence Transformers**: NLP model for job title embedding.
- **APIFY**: Web scraping tool for fetching job data.
- **Matplotlib & Seaborn**: Visualizations (Bar Charts & Pie Charts).
- **Pandas & NumPy**: Data manipulation and processing.

---

## Project Structure

```bash
.
├── Main.py                   # Entry point of the application
├── InterestedField.py        # Screen for selecting interested job fields
├── JobRecommendation.py      # Core logic for job recommendations and UI
├── Registration.py           # Login and registration screen
├── WorkExperience.py         # Screen for adding work experience
├── MyProfile.py              # Screen to manage user profile details
└── Project 2.pdf             # Project guidelines document
```

---

## Setup Instructions

Follow the steps below to set up and run the project on your machine.

### 1. Prerequisites

Make sure the following dependencies are installed:

- Python (>= 3.8)
- Kivy (>= 2.0.0)
- MongoDB (Cloud or Local instance)
- Sentence Transformers
- APIFY Python Client
- Matplotlib
- Seaborn
- Pandas
- NumPy

You can install the dependencies using pip:

```bash
pip install kivy pymongo sentence-transformers apify-client matplotlib seaborn pandas numpy
```

### 2. MongoDB Setup

1. Create a MongoDB Atlas account or run a local MongoDB instance.
2. Import job data into a collection named **Job_Listings** in the database **job_database**.
3. Update the MongoDB connection URI in `JobRecommendation.py`:

```python
uri = "your_mongodb_connection_string_here"
client = MongoClient(uri)
```

### 3. Running the Project

1. Navigate to the project folder.
2. Run the `Main.py` file to start the application:

```bash
python Main.py
```

---

## Usage Instructions

1. **Launch the Application**
   - Start the app by running `Main.py`.

2. **Register/Login**
   - Create an account or log in using valid credentials.

3. **Select Job Preferences**
   - Choose job categories/tags on the "InterestedField" screen.
   - These preferences will be used for job recommendations.

4. **Add Work Experience**
   - Fill in your work experience details on the "WorkExperience" screen.

5. **View Job Recommendations**
   - View jobs categorized based on your preferences.
   - Click on jobs to see their descriptions and details.

6. **Analyze Jobs**
   - Use the **"Analysis"** button to view job distribution charts.

---

## Screenshots

1. **Login/Registration Screen**
2. **Job Preferences Selection**
3. **Job Recommendations**
4. **Job Analysis (Charts)**

---

## Troubleshooting

1. **Database Connection Errors**:
   - Ensure the MongoDB URI is correct and accessible.
   - Check network settings and credentials.

2. **Dependency Errors**:
   - Reinstall missing dependencies using pip.

3. **UI Not Responsive**:
   - Adjust window size or test on a different screen resolution.

---

## Future Improvements

- Integrate live job scraping dynamically from multiple sources.
- Add user authentication and session management for better security.
- Allow job applications directly within the app.
- Improve UI for a better user experience.

---

## Contributors

- **Pranali Vyas**
- **Jiangshan Miao**
- **Xinyang Tong**

Feel free to reach out for any queries or improvements.

---

## License

This project is licensed under the MIT License.
  
