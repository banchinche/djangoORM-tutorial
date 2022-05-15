from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Question


@transaction.atomic
def create_decorator(data: dict) -> Question:
    question = Question.objects.create(**data)
    print('Inside create_decorator() object is:', Question.objects.filter(**data).first())
    return question


def create_context_manager(data: dict) -> Question:
    question = Question(**data)
    with transaction.atomic():
        question.save()
        print('Inside create_context_manager() object is:', Question.objects.filter(**data).first())
    return question


@transaction.atomic
def rollback_savepoint_creation(data: dict) -> None:
    sid = transaction.savepoint()
    Question.objects.create(**data)
    print(
        f'Inside rollback_savepoint_creation() before savepoint_rollback '
        f'object is: {Question.objects.filter(**data).first()}'
    )
    transaction.savepoint_rollback(sid)
    print(
        f'Inside rollback_savepoint_creation() after savepoint_rollback '
        f'object is : {Question.objects.filter(**data).first()}'
    )


@transaction.atomic
def nested_rollback_creation_first(data1: dict, data2: dict) -> None:
    Question.objects.create(**data1)
    print(f'First object is: {Question.objects.filter(**data1).first()}')
    inner_sid = transaction.savepoint()
    Question.objects.create(**data2)
    print(f'Second object is: {Question.objects.filter(**data2).first()}')
    transaction.savepoint_rollback(inner_sid)

    print(f'First object after rollback is: {Question.objects.filter(**data1).first()}')
    print(f'Second object after rollback is: {Question.objects.filter(**data2).first()}')


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Command, that demonstrates such functionality:

        1) Creating Question inside transaction with transaction.atomic() as a decorator
        2) Creating Question inside transaction with transaction.atomic() as a context manager
        3) Rollback creation Question using transaction.atomic() and savepoint
        4) Rollback creation of second Question using savepoint after creation first Question
        """
        print(f'Total count of Questions at start: {Question.objects.count()}')
        question1_data = {'question_text': 'UNIQUE Question1 text', 'pub_date': '2022-05-15'}
        question2_data = {'question_text': 'UNIQUE Question2 TEXT', 'pub_date': '2022-07-17'}
        question3_data = {'question_text': 'UnIqUe Question3 TeXt', 'pub_date': '2023-03-13'}
        question4_data = {'question_text': 'UnIqUe QUeStIoN4 tExT', 'pub_date': '2023-03-13'}
        question4_data_deletable = {'question_text': 'UnIqUe QUeStIoN4 tExT', 'pub_date': '2023-02-02'}
        print('\nCreate Question using transaction.atomic() as a decorator')
        create_decorator(question1_data)
        print('\nCreate Question using transaction.atomic() as a context manager')
        create_context_manager(question2_data)
        print('\nRollback creation Question using transaction.atomic() and savepoint')
        rollback_savepoint_creation(question3_data)
        print('\nRollback creation of second Question')
        nested_rollback_creation_first(question4_data, question4_data_deletable)

        print(f'\nTotal count of Questions at the end: {Question.objects.count()}')
        # 4) Deleting all Questions
        Question.objects.all().delete()
        print(f'Total count of Questions after delete: {Question.objects.count()}')
