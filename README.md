Group3 Job Recruiter Assistant Application
This project is a command-line interface (CLI) application designed to assist job recruiters with managing the hiring process. It provides a suite of tools to handle job postings, candidate profiles, applications, screening, and interview scheduling.

Features
Job Management: Create, edit, and search for job postings.
Candidate Management: Create and update candidate profiles with details like skills, experience, and education.
Application Tracking: Submit applications for candidates to jobs and update their status through the hiring pipeline (e.g., applied, screened, shortlisted).
Automated Screening: Filter candidates for eligibility based on predefined job requirements such as skills, experience, and visa status.
Candidate Ranking: Score and rank candidates for a specific job based on a weighted system of skills, experience, and education.
Interview Scheduling: Schedule interviews for shortlisted candidates, including checks to prevent interviewer scheduling conflicts.
Bulk Data Import: Import jobs, candidates, and applications in bulk from a single JSON file.
Data Persistence: All data is stored in a local recruiter_data.json file.
Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Python 3.x
Installation
Clone the repository to your local machine:

git clone https://github.com/kalyanvuyyala/group3-job-recruiter-assistant-application.git
Navigate to the project directory:

cd group3-job-recruiter-assistant-application
Install the necessary packages for development and testing:

pip install -r requirements.txt
Usage
To start the application, run the main.py module from the root directory:

python3 -m src.app.main
You will be presented with an interactive menu to choose from various actions:

Job Recruiter Assistant Application
1) Create Job
2) Create Candidate
3) Submit Application
4) Search Jobs
5) Update Application Status
6) Filter Eligibility
7) Rank Candidates
8) Schedule Interview
9) Exit
10) Bulk Import (JSON)
Running Tests
This project uses pytest for testing.

Running All Tests
To execute the entire test suite, run the following command from the project's root directory:

pytest -q
Test Coverage
To generate a test coverage report, run the following commands:

coverage run -m pytest
coverage report -m
