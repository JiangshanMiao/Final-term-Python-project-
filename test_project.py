import pytest
import json
from JobRecommendation import JobRecommendationScreen
from InterestedField import InterestedFieldScreen
from unittest.mock import patch
from pymongo import MongoClient


@pytest.fixture
def mock_mongo():
    with patch("pymongo.MongoClient") as mock_client:
        mock_db = mock_client.return_value["job_database"]
        mock_collection = mock_db["Job_Listings"]
        mock_collection.find.return_value = [
            {"title": "Software Engineer", "location": "New York", "salary": "$100k", "type": "Full-Time"}
        ]
        yield mock_client


def test_generate_json(screen, tmp_path):
    screen.buttons_dict['Technical & Engineering'][0].state = 'down'
    screen.generate_json(None)
    with open("user_interest_tags.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data['Technical & Engineering'] == ['Aerospace Engineering']


def test_load_jobs_from_database(mock_mongo):
    screen = JobRecommendationScreen()
    screen.load_jobs_from_database()
    assert len(screen.jobs) > 0


def test_search_functionality():
    screen = JobRecommendationScreen()
    screen.jobs = [
        {"title": "Software Engineer", "location": "New York", "salary": "$100k", "type": "Full-Time"},
        {"title": "Data Scientist", "location": "San Francisco", "salary": "$120k", "type": "Part-Time"},
    ]
    screen.search_bar.text = "Software"
    screen.perform_search(None)
    assert len(screen.filtered_jobs) == 1
    assert screen.filtered_jobs[0]["title"] == "Software Engineer"

def test_update_job_list():
    screen = JobRecommendationScreen()
    screen.filtered_jobs = [
        {"title": "Developer", "location": "Remote", "salary": "$80k", "type": "Contract"}
    ]
    screen.update_job_list()
    assert len(screen.job_grid.children) == 1
    assert "Developer" in screen.job_grid.children[0].text

def test_empty_database_handling():
    screen = JobRecommendationScreen()
    screen.jobs = []
    screen.update_job_list()
    assert len(screen.job_grid.children) == 0







