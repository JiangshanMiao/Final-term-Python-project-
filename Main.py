from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Registration import LoginScreen  # Import LoginScreen from Registration.py
from MyProfile import MainScreen  # Import MainScreen from MyProfile.py
from WorkExperience import WorkExperienceScreen  # Import WorkExperienceScreen from WorkExperience.py
from JobRecommendation import JobRecommendationScreen
from InterestedField import InterestedFieldScreen
class MainApp(App):
    """Main application managing screen transitions."""

    def build(self):
        # Create the ScreenManager
        sm = ScreenManager()

        # Add LoginScreen to the ScreenManager
        login_screen = LoginScreen(name='login_screen')
        sm.add_widget(login_screen)

        # Add MainScreen to the ScreenManager
        main_screen = MainScreen(name='main_screen')
        sm.add_widget(main_screen)

        # Add WorkExperienceScreen to the ScreenManager
        work_experience_screen = WorkExperienceScreen(name='work_experience_screen')
        sm.add_widget(work_experience_screen)

        # Add InterestedFieldScreen to the ScreenManager
        interested_field_screen = InterestedFieldScreen(name='interested_field_screen')
        sm.add_widget(interested_field_screen)

        # Add job_recommendation_screen
        job_recommendation_screen = JobRecommendationScreen(name='job_recommendation_screen')
        sm.add_widget(job_recommendation_screen)

        # Set the default screen to LoginScreen
        sm.current = 'login_screen'

        return sm


if __name__ == '__main__':
    MainApp().run()
