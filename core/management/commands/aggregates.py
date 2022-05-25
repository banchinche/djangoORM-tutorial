from django.core.management.base import BaseCommand
from django.db.models import (
    Avg,
    Count,
    Max,
    Min,
)

from core.models import (
    Choice,
    Question
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Command, that demonstrates such functionality:

        1) Preparations for aggregation demonstration
        2) Avg example (aggregate)
        3) Max & Min example (aggregate)
        4) Count example (annotate)
        5) Flush tables
        """

        # 1) Creating Question & Choice instances
        print(f'Total count of Choices at start: {Choice.objects.count()}')
        print(f'Total count of Questions at start: {Question.objects.count()}')
        question = Question.objects.create(question_text='Wonderful Question', pub_date='2022-07-07')
        Choice.objects.create(question=question, choice_text='Accepted', votes=5, new_field='New field text')
        Choice.objects.create(question=question, choice_text='Accepted', votes=5, new_field='New field text')
        Choice.objects.create(question=question, choice_text='Accepted', votes=4, new_field='New field text')
        Choice.objects.create(question=question, choice_text='Accepted', votes=3, new_field='New field text')

        print(f'Total count of Choices after creation: {Choice.objects.count()}')
        print(f'Total count of Questions after creation: {Question.objects.count()}')

        # 2) Avg votes for Choices (5 + 5 + 4 + 3) / 4 => vote_avg must be equal to 4.25
        print(
            f'\nAvg choice votes between all Choices: '
            f'{Choice.objects.aggregate(vote_avg=Avg("votes"))}'
        )

        # 3) Max & Min votes for Choices
        print(
            f'\nMax & Min choice votes between all Choices: '
            f'{Choice.objects.aggregate(vote_max=Max("votes"), vote_min=Min("votes"))}'
        )

        # 4) Count of Choices for each Question
        questions = Question.objects.annotate(choices_count=Count("choice"))
        print(
            f'\nEvery existing Question now has number of choices related with it (now just one).'
            f'\nFirst Question has {questions.first().choices_count} Choices'
        )

        # 5) Deleting all Questions & Choices
        Choice.objects.all().delete()
        Question.objects.all().delete()
        print(f'\nTotal count of Questions after delete: {Question.objects.count()}')
        print(f'Total count of Choice after delete: {Choice.objects.count()}')
