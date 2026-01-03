# Job Recruiter Assistant Application

A comprehensive command-line interface (CLI) application designed to streamline the recruitment process. This tool helps recruiters manage job postings, candidate profiles, applications, screening workflows, and interview scheduling through an intuitive menu-driven interface.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Main Features](#main-features)
  - [Bulk Data Import](#bulk-data-import)
- [Testing](#testing)
- [Data Persistence](#data-persistence)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality

- **Job Management**
  - Create new job postings with detailed requirements
  - Edit existing job postings
  - Search and filter jobs by various criteria

- **Candidate Management**
  - Create comprehensive candidate profiles
  - Track skills, experience, education, and visa status
  - Update candidate information as needed

- **Application Tracking System**
  - Submit applications linking candidates to jobs
  - Track application status through the hiring pipeline
  - Status progression: `applied` → `screened` → `shortlisted` → `interviewed` → `offered`/`rejected`

- **Automated Candidate Screening**
  - Filter candidates based on predefined job requirements
  - Automated eligibility checks for:
    - Required skills matching
    - Minimum experience requirements
    - Education qualifications
    - Visa/work authorization status

- **Intelligent Candidate Ranking**
  - Score candidates using a weighted ranking system
  - Evaluation criteria include:
    - Skills match percentage
    - Years of experience
    - Education level
  - Automatic sorting from highest to lowest score

- **Interview Scheduling**
  - Schedule interviews for shortlisted candidates
  - Built-in conflict detection for interviewer availability
  - Track interview dates and assigned interviewers

- **Bulk Data Import**
  - Import multiple jobs, candidates, and applications at once
  - JSON-based format for easy integration
  - Streamlined onboarding for large datasets

## 📁 Project Structure

```
Group3-Job-Recruiter-Assistant-Application/
├── .idea/                      # IDE configuration files
├── data/                       # Sample data files
├── src/                        # Source code
│   ├── app/                    # Application modules
│   │   └── main.py            # Main application entry point
│   └── ...                     # Other source modules
├── tests/                      # Test suite
├── .coverage                   # Test coverage data
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.x** (Python 3.7 or higher recommended)
- **pip** (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kalyanvuyyala/Group3-Job-Recruiter-Assistant-Application.git
   ```

2. **Navigate to the project directory**
   ```bash
   cd Group3-Job-Recruiter-Assistant-Application
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Starting the Application

Run the application from the project root directory:

```bash
python3 -m src.app.main
```

### Main Features

Upon starting, you'll see an interactive menu:

```
Job Recruiter Assistant Application
=====================================
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

Choose an option:
```

#### Option Details

1. **Create Job** - Add a new job posting with requirements, description, and qualifications
2. **Create Candidate** - Add a new candidate with profile details, skills, and experience
3. **Submit Application** - Link a candidate to a job opening
4. **Search Jobs** - Find jobs by title, department, location, or other criteria
5. **Update Application Status** - Move applications through the hiring pipeline
6. **Filter Eligibility** - Automatically screen candidates against job requirements
7. **Rank Candidates** - Score and rank all candidates for a specific position
8. **Schedule Interview** - Set up interviews with conflict checking
9. **Exit** - Close the application
10. **Bulk Import (JSON)** - Import multiple records from a JSON file

### Bulk Data Import

The bulk import feature accepts a JSON file with the following structure:

```json
{
  "jobs": [
    {
      "title": "Software Engineer",
      "department": "Engineering",
      "required_skills": ["Python", "JavaScript"],
      "min_experience": 3,
      "education": "Bachelor's"
    }
  ],
  "candidates": [
    {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "skills": ["Python", "Java", "SQL"],
      "experience": 5,
      "education": "Bachelor's",
      "visa_status": "Citizen"
    }
  ],
  "applications": [
    {
      "candidate_id": "C001",
      "job_id": "J001",
      "status": "applied"
    }
  ]
}
```

## 🧪 Testing

This project uses `pytest` for comprehensive testing.

### Running All Tests

Execute the complete test suite:

```bash
pytest -q
```

### Running Specific Tests

Run tests for a specific module:

```bash
pytest tests/test_module_name.py -v
```

### Test Coverage

Generate a detailed coverage report:

```bash
# Run tests with coverage
coverage run -m pytest

# Display coverage report
coverage report -m

# Generate HTML coverage report
coverage html
```

The HTML report will be available in the `htmlcov/` directory.

### Expected Output

The test suite should show comprehensive coverage across all modules. Example output:

```
tests/test_*.py ...................... [ 95%]
===================== X passed in X.XXs =====================
```

## 💾 Data Persistence

All application data is stored locally in `recruiter_data.json`. This file contains:

- Job postings
- Candidate profiles
- Application records
- Interview schedules

The file is automatically created on first run and updated with each operation.

**Note:** Ensure you have write permissions in the application directory.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write tests for new features
- Ensure all tests pass before submitting PR
- Update documentation as needed

## 📝 License

This project is available for educational and personal use.

## 👥 Contributors

This project was developed by Group 3. Special thanks to all contributors who have helped shape this application.

## 📧 Contact

For questions, issues, or suggestions, please open an issue on the [GitHub repository](https://github.com/kalyanvuyyala/Group3-Job-Recruiter-Assistant-Application/issues).

---

**Happy Recruiting! 🎯**
