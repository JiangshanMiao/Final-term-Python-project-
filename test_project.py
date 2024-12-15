import pytest
from JobRecommendation import JobRecommendationScreen  # Replace with actual import
from InterestedField import InterestedFieldScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.togglebutton import ToggleButton

@pytest.fixture


def app():
    # Setup code: Initialize and return your app/screen instance
    return JobRecommendationScreen()

def test_populate_job_list(app):
    screen = app
    screen.populate_job_list()
    assert len(screen.job_grid.children) > 0, "Job list is empty"


def test_toggle_tag_selection(app):
    screen = app
    screen.toggle_tag_selection("Python", True)
    assert "Python" in screen.checked_tags

def test_toggle_job_selection(app):
    screen = app
    screen.toggle_job_selection("Software Engineer", True)
    assert "Software Engineer" in screen.checked_jobs

def test_button_color_update():
    screen = InterestedFieldScreen()
    button = ToggleButton(text="Software Engineer")

    # Simulate button click (state changes from 'normal' to 'down')
    screen.update_button_color(button, "down")
    assert tuple(button.background_color) == (0.4, 0.8, 1, 1)  # Corrected this line

    # Simulate button deselection (state changes from 'down' to 'normal')
    screen.update_button_color(button, "normal")
    assert tuple(button.background_color) == (1, 1, 1, 1)

def test_screen_category_and_tags_display():
    screen = InterestedFieldScreen()

    # Simulate loading data
    categories = {
        "Tech": ["Software Engineer", "Data Scientist"],
        "Business": ["Product Manager"]
    }
    for category, tags in categories.items():
        for tag in tags:
            button = ToggleButton(text=tag)
            if category not in screen.buttons_dict:
                screen.buttons_dict[category] = []
            screen.buttons_dict[category].append(button)

    # Verify that categories and buttons_dict are populated correctly
    assert "Tech" in screen.buttons_dict
    assert len(screen.buttons_dict["Tech"]) == 2
    assert screen.buttons_dict["Tech"][0].text == "Software Engineer"
    assert screen.buttons_dict["Business"][0].text == "Product Manager"

def test_save_and_continue():
    screen_manager = ScreenManager()

    # Add a mock JobRecommendationScreen
    mock_job_screen = JobRecommendationScreen(name="job_recommendation_screen")
    screen_manager.add_widget(mock_job_screen)

    screen = InterestedFieldScreen(name="interested_field_screen")
    screen.manager = screen_manager

    # Simulate buttons and categories
    screen.buttons_dict = {
        "Tech": [ToggleButton(text="Software Engineer", state="down"),
                 ToggleButton(text="Data Scientist", state="normal")],
        "Business": [ToggleButton(text="Product Manager", state="down")]
    }

    # Simulate saving and continuing
    screen.save_and_continue(None)

    # Check if the selected tags are correct
    selected_tags = [btn.text for category, buttons in screen.buttons_dict.items()
                     for btn in buttons if btn.state == "down"]
    assert selected_tags == ["Software Engineer", "Product Manager"]

    # Ensure the next screen is set correctly
    assert screen_manager.current == "job_recommendation_screen"

