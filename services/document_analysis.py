import spacy
from collections import Counter
from spacy.matcher import PhraseMatcher
from transformers import pipeline

class DocumentAnalysis:
    def __init__(self, text: str):
        self.text = text
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(text)
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.sentiment_analyzer = pipeline("sentiment-analysis")

    def word_count(self):
        return len([token for token in self.doc if token.is_alpha])

    def sentence_count(self):
        return len(list(self.doc.sents))

    def keyword_extraction(self, top_n=5):
        # Lemmatize and filter stopwords/punctuation
        words = [
            token.lemma_.lower()
            for token in self.doc
            if token.is_alpha and not token.is_stop
        ]
        most_common = Counter(words).most_common(top_n)
        return [word for word, count in most_common]

    def named_entities(self):
        return [(ent.text, ent.label_) for ent in self.doc.ents]

    def summarize(self):
        summary = self.summarizer(self.text, max_length=50, min_length=25, do_sample=False)
        return summary[0]['summary_text']

    def sentiment(self):
        return self.sentiment_analyzer(self.text)[0]

    def extract_skills(self, skill_list=None):
        if skill_list is None:
            skill_list = [
                "python", "machine learning", "statistics", "data analysis",
                "html", "css", "javascript", "react",
                "java", "c++", "algorithms",
                "excel", "presentation", "communication",
                "deep learning", "tensorflow", "pytorch"
            ]
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(skill) for skill in skill_list]
        matcher.add("SKILLS", patterns)
        matches = matcher(self.doc)
        found_skills = set([self.doc[start:end].text for match_id, start, end in matches])
        return list(found_skills)

# Example usage:
if __name__ == "__main__":
    sample_text = """
    PathPilot.AI is an intelligent platform for career guidance.
    It analyzes resumes and job descriptions to provide actionable insights.
    John Doe has experience with Python and machine learning at Microsoft.
    """
    analyzer = DocumentAnalysis(sample_text)
    print("Word count:", analyzer.word_count())
    print("Sentence count:", analyzer.sentence_count())
    print("Keywords:", analyzer.keyword_extraction())
    print("Named Entities:", analyzer.named_entities())
    print("Summary:", analyzer.summarize())
    print("Sentiment:", analyzer.sentiment())
    print("Extracted Skills:", analyzer.extract_skills())
