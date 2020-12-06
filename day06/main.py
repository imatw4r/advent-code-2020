import os
from itertools import takewhile, dropwhile
from typing import List, Dict, NamedTuple, Iterable, Union, Literal
from form import Form, FormCollection, Answer, Question, AnsweredQuestions
from analyzer import FormAnalyzer

BASE_DIR = os.path.dirname(__file__)
END_OF_GROUP_CHAR = ""

InputData = Iterable[Union[AnsweredQuestions, Literal[""]]]


def create_form(answered_questions: Iterable[Question]) -> Form:
    """
    A single Form stores single Passenger answers.
    """
    form = Form()
    form.add_answers((Answer(question, True) for question in answered_questions))
    return form


def build_forms(data: InputData) -> List[Form]:
    # Pick until END_OF_GROUP_CHAR found
    passengers_answered_questions: Iterable[AnsweredQuestions] = takewhile(
        lambda v: v != END_OF_GROUP_CHAR, data
    )
    # Drop as long as END_OF_GROUP_CHAR found
    dropwhile(lambda v: v == END_OF_GROUP_CHAR, data)

    passengers_forms = []
    for questions in passengers_answered_questions:
        form = create_form(answered_questions=questions)
        passengers_forms.append(form)
    return passengers_forms


def create_form_collection(data: InputData) -> FormCollection:
    """
    A FormCollection stores a single Passenger's group Forms.
    """
    forms = build_forms(data)
    if not forms:
        return None

    collection = FormCollection()
    collection.add_forms(forms)
    return collection


def build_collections(data: InputData) -> List[FormCollection]:
    all_collections = []
    collection = create_form_collection(data)
    while collection is not None:
        all_collections.append(collection)
        collection = create_form_collection(data)
    return all_collections


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = iter(map(str.strip, fp))
    all_collections = build_collections(data)
    analyzer = FormAnalyzer()
    count = sum(map(analyzer.count_questions_answered_by_any, all_collections))
    print("Part 1 answer:", count)


with open(os.path.join(BASE_DIR, "data.in"), "r") as fp:
    data = iter(map(str.strip, fp))
    all_collections = build_collections(data)
    analyzer = FormAnalyzer()
    count = sum(map(analyzer.count_questions_answered_by_all, all_collections))
    print("Part 2 answer:", count)
