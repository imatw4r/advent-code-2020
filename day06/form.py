from typing import List, NamedTuple

# Represent a single question, like: a, b, c, d
Question = str
# Represent answered questions like: abdcdf, xyz, cdg
AnsweredQuestions = str


class Answer(NamedTuple):
    question: Question
    value: bool


class Form(object):
    def __init__(self):
        self.answers: List[Answer] = []

    def add_answers(self, answers: List[Answer]):
        self.answers.extend(answers)

    def get_answers(self):
        return self.answers[:]


class FormCollection(object):
    def __init__(self):
        self.forms: List[Form] = []

    def add_forms(self, forms: List[Form]):
        self.forms.extend(forms)

    def all(self):
        return self.forms[:]

    def __len__(self):
        return len(self.forms)

    def __repr__(self):
        return f"FormCollection(forms={len(self.forms)})"
