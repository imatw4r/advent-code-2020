from typing import Dict, Tuple
from form import FormCollection, Answer, Question
from collections import defaultdict

Count = int


class FormAnalyzer(object):
    def _get_questions_count(self, collection: FormCollection) -> Dict[Question, Count]:
        forms = collection.all()
        question_count = defaultdict(int)
        for form in forms:
            for answer in form.get_answers():
                question_count[answer.question] += 1
        return question_count

    def count_questions_answered_by_any(self, collection: FormCollection) -> Count:
        questions = self._get_questions_count(collection)
        return len(questions)

    def count_questions_answered_by_all(self, collection: FormCollection) -> Count:
        questions = self._get_questions_count(collection=collection)

        def answered_by_all(question: Tuple[Question, Count]):
            _, count = question
            return count == len(collection)

        return len(list(filter(answered_by_all, questions.items())))