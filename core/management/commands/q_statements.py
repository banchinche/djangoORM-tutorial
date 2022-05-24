from django.core.management.base import BaseCommand
from django.db.models import Q

from core.models import (
    Choice,
    Question
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Command, that demonstrates such functionality:

        1) Preparations for filtering / excluding demonstration
        2) No difference between kwarg & Q-object
        3) Default connection for Q-object AND operator too
        4) Combine Q-objects via operator OR
        5) Negate Q-statement using ~ operator
        6) Combine kwargs and Q-objects
        7) Flush tables
        """

        # 1) Creating Question & Choice instances
        print(f'Total count of Choices at start: {Choice.objects.count()}')
        print(f'Total count of Questions at start: {Question.objects.count()}')
        Question.objects.create(
            question_text='Wonderful Question',
            pub_date='2022-07-07'
        )

        print(f'Total count of Choices after creation: {Choice.objects.count()}')
        print(f'Total count of Questions after creation: {Question.objects.count()}')

        # 2) No difference between kwarg & Q-object
        print('\nNo difference between kwarg and Q-object')
        print(
            f"Must be one Question (kwarg): "
            f"{Question.objects.filter(question_text='Wonderful Question')}"
        )
        print(
            f"Must be one Question (Q-object): "
            f"{Question.objects.filter(Q(question_text='Wonderful Question'))}"
        )
        # 3) Default connection for Q-object AND operator too
        print('\nNo difference between kwargs and Q-objects default operator (AND / &)')
        print(
            f"Must be one Question (kwarg): "
            f"{Question.objects.filter(question_text='Wonderful Question', pub_date='2022-07-07')}"
        )
        print(
            f"Must be one Question (Q-object): "
            f"{Question.objects.filter(Q(question_text='Wonderful Question'), Q(pub_date='2022-07-07'))}"
        )

        # 4) Combine Q-objects via operator OR
        print('\nFiltering via Q-objects with OR-operator')
        print(
            f"Must be empty (default filter arguments connecting with AND): "
            f"{Question.objects.filter(question_text='Wonderful Question', pub_date='2022-05-05')}"
        )
        print(
            f"Must be one Question (Q-objects with OR operator): "
            f"{Question.objects.filter(Q(question_text='Wonderful Question') | Q(pub_date='2022-05-05'))}"
        )

        # 5) Negate Q-statement using ~ operator
        print('\nNegate Q-statement using ~ operator')
        print(
            f"Must be one question: "
            f"{Question.objects.filter(~Q(question_text='NO SUCH TEXT') & ~Q(pub_date='3000-03-03'))}"
        )
        # 6) Combine kwargs and Q-objects
        #    (Q-objects must be positional arguments and then use kwargs)
        print('\nCombine kwargs and Q-object')
        result = Question.objects.filter(
            ~Q(question_text='NO SUCH TEXT') & ~Q(pub_date='3000-03-03'),
            pub_date__year=2022
        )
        print(f"Must be one question: {result}")

        # 7) Deleting all Questions & Choices
        Choice.objects.all().delete()
        Question.objects.all().delete()
        print(f'\nTotal count of Questions after delete: {Question.objects.count()}')
        print(f'Total count of Choice after delete: {Choice.objects.count()}')
