from src.storage.repository import Repository
from src.services.job_service import JobService
from src.services.candidate_service import CandidateService
from src.services.application_service import ApplicationService
from src.services.screening_service import ScreeningService
from src.services.interview_service import InterviewService
from src.app.exceptions import ValidationError, NotFoundError, ConflictError, StateError

class CLI:
    def __init__(self):
        repo = Repository()
        self.jobs = JobService(repo)
        self.candidates = CandidateService(repo)
        self.apps = ApplicationService(repo)
        self.screening = ScreeningService(repo)
        self.interviews = InterviewService(repo)

    def run(self) -> None:
        while True:
            print("\nJob Recruiter Assistant Application")
            print("1) Create Job")
            print("2) Create Candidate")
            print("3) Submit Application")
            print("4) Search Jobs")
            print("5) Update Application Status")
            print("6) Filter Eligibility")
            print("7) Rank Candidates")
            print("8) Schedule Interview")
            print("9) Exit")
            print("10) Bulk Import (JSON)")

            choice = input("Choose: ").strip()
            try:
                if choice == "1":
                    self._create_job()
                elif choice == "2":
                    self._create_candidate()
                elif choice == "3":
                    self._submit_application()
                elif choice == "4":
                    self._search_jobs()
                elif choice == "5":
                    self._update_status()
                elif choice == "6":
                    self._filter_eligibility()
                elif choice == "7":
                    self._rank_candidates()
                elif choice == "8":
                    self._schedule_interview()
                elif choice == "10":
                    self._bulk_import()
                elif choice == "9":
                    print("Bye.")
                    return
                else:
                    print("Invalid option.")
            except (ValidationError, NotFoundError, ConflictError, StateError) as e:
                print(f"Error: {e}")

    def _create_job(self):
        job_id = input("job_id: ")
        title = input("title: ")
        location = input("location: ")
        job_type = input("job_type: ")
        min_salary = int(input("min_salary: "))
        max_salary = int(input("max_salary: "))
        skills = input("required_skills (comma): ").split(",")
        min_exp = int(input("min_experience_years: "))
        visa = input("visa_required (y/n): ").strip().lower() == "y"
        job = self.jobs.create_job_posting(job_id, title, location, job_type, min_salary, max_salary, skills, min_exp, visa)
        print("Created:", job["job_id"])

    def _create_candidate(self):
        cid = input("candidate_id: ")
        name = input("name: ")
        email = input("email: ")
        phone = input("phone: ")
        location = input("location: ")
        years = int(input("years_experience: "))
        skills = input("skills (comma): ").split(",")
        edu = input("education_level: ")
        visa = input("visa_status (no_sponsorship/needs_sponsorship/etc): ")
        c = self.candidates.create_candidate_profile(cid, name, email, phone, location, years, skills, edu, visa)
        print("Created:", c["candidate_id"])

    def _submit_application(self):
        aid = input("application_id: ")
        job_id = input("job_id: ")
        cid = input("candidate_id: ")
        a = self.apps.submit_application(aid, job_id, cid)
        print("Submitted:", a["application_id"], a["status"])

    def _search_jobs(self):
        k = input("keyword: ")
        loc = input("location: ")
        jt = input("job_type: ")
        res = self.jobs.search_jobs(k, loc, jt)
        print(f"Found {len(res)} job(s).")
        for j in res:
            print("-", j["job_id"], j["title"], "|", j["location"])

    def _update_status(self):
        aid = input("application_id: ")
        status = input("new_status (screened/shortlisted/rejected/interview_scheduled): ")
        reason = input("reason: ")
        a = self.apps.update_application_status(aid, status, reason)
        print("Updated:", a["application_id"], a["status"])

    def _filter_eligibility(self):
        job_id = input("job_id: ")
        cids = input("candidate_ids (comma): ").split(",")
        res = self.screening.filter_eligibility(job_id, cids)
        for r in res:
            print(r)

    def _rank_candidates(self):
        job_id = input("job_id: ")
        cids = input("candidate_ids (comma): ").split(",")
        res = self.screening.rank_candidates(job_id, cids)
        for r in res:
            print(r)

    def _schedule_interview(self):
        iid = input("interview_id: ")
        aid = input("application_id: ")
        ts = input("scheduled_time ISO (e.g. 2025-12-20T10:00:00): ")
        dur = int(input("duration_minutes: "))
        interviewer = input("interviewer: ")
        loc = input("location: ")
        itv = self.interviews.schedule_interview(iid, aid, ts, dur, interviewer, loc)
        print("Scheduled:", itv["interview_id"])

    def _bulk_import(self):
        from src.services.bulk_import_service import BulkImportService
        svc = BulkImportService(self.jobs.repo)  # uses same Repository instance type
        path = input("Path to bulk JSON file (e.g. data/bulk_import.json): ").strip()
        report = svc.import_from_json(path)
        print("Import report:")
        print(report)

