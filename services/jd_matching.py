import re
import spacy
from spacy.matcher import PhraseMatcher
from fuzzywuzzy import fuzz

class JDMatcher:
    def __init__(self, resume_text: str, jd_text: str):
        self.resume_text = resume_text
        self.jd_text = jd_text
        self.nlp = spacy.load("en_core_web_sm")
        self.skill_keywords = [
            "python", "machine learning", "statistics", "data analysis",
            "html", "css", "javascript", "react",
            "java", "c++", "algorithms",
            "excel", "presentation", "communication",
            "deep learning", "tensorflow", "pytorch"
        ]

    def extract_skills(self, text):
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in self.skill_keywords]
        matcher.add("SKILLS", patterns)
        doc = self.nlp(text)
        matches = matcher(doc)
        found_skills = set([doc[start:end].text for match_id, start, end in matches])
        return found_skills

    def fuzzy_match(self, skill, skill_set, threshold=80):
        for s in skill_set:
            if fuzz.token_set_ratio(skill, s) >= threshold:
                return s
        return None

    def match_skills(self):
        resume_skills = self.extract_skills(self.resume_text)
        jd_skills = self.extract_skills(self.jd_text)
        matched = set()
        missing = set()
        extra = set(resume_skills)

        for jd_skill in jd_skills:
            match = self.fuzzy_match(jd_skill, resume_skills)
            if match:
                matched.add(jd_skill)
                extra.discard(match)
            else:
                missing.add(jd_skill)

        return {
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "extra_skills": list(extra)
        }

# Example usage:
if __name__ == "__main__":
    resume = "Experienced in Python, Machine Learning, and Data Analysis."
    jd = "Looking for a candidate skilled in Python, Deep Learning, and Data Analysis."
    matcher = JDMatcher(resume, jd)
    print(matcher.match_skills())