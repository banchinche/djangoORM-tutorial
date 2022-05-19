from django.core.management.base import BaseCommand

from core.models import (
    Choice,
    Question
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Command, that demonstrates such functionality:

        1) Preparations for filtering / excluding demonstration
        2) Filtering exact / iexact
        3) Exclude exact / iexact
        4) Filtering related attributes
        5) Chaining filter & exclude
        6) Flush tables
        """

        # 1) Creating Question & Choice instances
        print(f'Total count of Choices at start: {Choice.objects.count()}')
        print(f'Total count of Questions at start: {Question.objects.count()}')
        question = Question.objects.create(
            question_text='Wonderful Question',
            pub_date='2022-07-07'
        )
        Choice.objects.create(
            question=question,
            choice_text='Accepted',
            votes=5,
            new_field='New field text'
        )

        print(f'Total count of Choices after creation: {Choice.objects.count()}')
        print(f'Total count of Questions after creation: {Question.objects.count()}')

        # 2) Filtering exact / iexact
        print('\nFiltering exact / iexact')
        print(
            f"Must be one Question: "
            f"{Question.objects.filter(question_text='Wonderful Question')}"  # same as question_text__exact
        )
        print(
            f"Must be one Question: "
            f"{Question.objects.filter(question_text__iexact='wonderful question')}"
        )

        # 3) Exclude exact / iexact
        print('\nExclude exact / iexact')
        print(
            f"Must be one Question: "
            f"{Question.objects.exclude(question_text='Wonderful QueStIoN')}"  # same as question_text__exact
        )
        print(
            f"Must be one Question: "
            f"{Question.objects.exclude(question_text__iexact='wonderful question, very wonderful')}"
        )

        # 4) Filtering related attributes
        print('\nFiltering related attributes')
        print(
            f"Must be one Question: "
            f"{Question.objects.filter(choice__choice_text='Accepted')}"
        )
        print(
            f"Must be one Question: "
            f"{Question.objects.filter(choice__votes__gte=5)}"  # Greater than or equal lookup
        )

        # 5) Chaining filter & exclude
        print('\nChaining filter & exclude')
        filtered = Question.objects.filter(pub_date__year='2022')
        print(f"Must be one Question: {filtered}")

        excluded = filtered.exclude(choice__votes__range=(1, 4)).exclude(choice__votes__range=(6, 10))
        print(f"Must be one Question: {excluded}")

        # 6) Deleting all Questions & Choices
        Choice.objects.all().delete()
        Question.objects.all().delete()
        print(f'\nTotal count of Questions after delete: {Question.objects.count()}')
        print(f'Total count of Choice after delete: {Choice.objects.count()}')
