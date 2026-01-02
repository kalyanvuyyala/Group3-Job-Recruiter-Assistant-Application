from typing import Dict, Any, List, Tuple
from src.app.exceptions import NotFoundError
from src.app.utils import normalise_text
from src.storage.repository import Repository

class ScreeningService:
    def __init__(self, repo: Repository):
        self.repo = repo

    def filter_eligibility(self, job_id: str, candidate_ids: List[str]) -> List[Dict[str, Any]]:
        db = self.repo.load()
        jid = normalise_text(job_id)
        job = db["jobs"].get(jid)
        if not job:
            raise NotFoundError("Job not found.")

        req_skills = set([normalise_text(s) for s in job.get("required_skills", [])])
        min_exp = int(job.get("min_experience_years", 0))
        visa_required = bool(job.get("visa_required", False))

        out = []
        for cid_raw in candidate_ids:
            cid = normalise_text(cid_raw)
            cand = db["candidates"].get(cid)
            if not cand:
                continue

            cand_skills = set([normalise_text(s) for s in cand.get("skills", [])])
            exp_ok = int(cand.get("years_experience", 0)) >= min_exp
            skills_ok = req_skills.issubset(cand_skills) if req_skills else True

            visa_ok = True
            visa_status = normalise_text(cand.get("visa_status", "unknown"))
            if visa_required:
                visa_ok = (visa_status in {"no_sponsorship", "citizen", "pr", "settled"})

            if exp_ok and skills_ok and visa_ok:
                out.append({"candidate_id": cid, "eligible": True, "reason": "meets_all"})
            else:
                reasons = []
                if not exp_ok:
                    reasons.append("insufficient_experience")
                if not skills_ok:
                    reasons.append("missing_skills")
                if not visa_ok:
                    reasons.append("visa_mismatch")
                out.append({"candidate_id": cid, "eligible": False, "reason": ",".join(reasons)})
        return out

    def rank_candidates(self, job_id: str, candidate_ids: List[str],
                        weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        db = self.repo.load()
        jid = normalise_text(job_id)
        job = db["jobs"].get(jid)
        if not job:
            raise NotFoundError("Job not found.")

        weights = weights or {"skills": 0.5, "experience": 0.3, "education": 0.2}
        req_skills = set([normalise_text(s) for s in job.get("required_skills", [])])
        edu_map = {"phd": 1.0, "masters": 0.8, "bachelors": 0.6, "diploma": 0.4, "unknown": 0.2}

        scored: List[Tuple[float, Dict[str, Any]]] = []
        for cid_raw in candidate_ids:
            cid = normalise_text(cid_raw)
            cand = db["candidates"].get(cid)
            if not cand:
                continue

            cand_skills = set([normalise_text(s) for s in cand.get("skills", [])])
            skills_score = 1.0 if not req_skills else (len(req_skills.intersection(cand_skills)) / max(1, len(req_skills)))

            exp = int(cand.get("years_experience", 0))
            exp_score = 1.0 if exp >= 10 else exp / 10.0
            exp_score = min(max(exp_score, 0.0), 1.0)

            edu = normalise_text(cand.get("education_level", "unknown"))
            edu_score = edu_map.get(edu, 0.2)

            total = (weights["skills"] * skills_score) + (weights["experience"] * exp_score) + (weights["education"] * edu_score)

            scored.append((total, {
                "candidate_id": cid,
                "score": round(total, 4),
                "breakdown": {"skills": round(skills_score, 4), "experience": round(exp_score, 4), "education": round(edu_score, 4)}
            }))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored]
