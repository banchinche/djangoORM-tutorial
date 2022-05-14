from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict

from core.models import Question


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Command, that demonstrates such functionality:

        1) Creating Questions via .bulk_create() method
        2) Updating Question via .bulk_update() method
        3) Mapping unique Question fields to Question objects via .in_bulk() method
        4) Deleting all created Question objects

        """
        # 1) Creating new Questions via manager-method .bulk_create()
        questions = [
            Question(question_text='What a question, wow!', pub_date='2022-05-02'),
            Question(question_text='Second question, wow!', pub_date='2022-06-06'),
            Question(question_text='Third question, wow!', pub_date='2022-07-07'),
        ]

        # There are still no questions in the database
        print(f'Total count of Questions: {Question.objects.count()}')
        Question.objects.bulk_create(questions)
        print()  # for visual indent
        # Note, that all these objects will not have ID !
        for q in questions:
            print('Newly created Question values:', model_to_dict(q))

        print(f'\nAll questions {Question.objects.all().values_list()}\n')

        # 2) Demonstration of the .bulk_update() - add #number for every odd Question
        questions = Question.objects.all()
        updatable = list()
        for i, q in enumerate(questions, start=1):
            if i % 2 == 1:
                q.question_text = f'{q.question_text}#{i}'
                updatable.append(q)
        Question.objects.bulk_update(updatable, fields=['question_text'])
        # For three Questions first and third were updated
        print(f'Updated questions\n {Question.objects.all().values_list()}\n')

        # 3) Demonstration of the .in_bulk() - different mapping types
        # use values_list('pk', flat=True)
        print('Mapping pk to object:', Question.objects.in_bulk())
        # Cannot use in_bulk with not unique fields !
        try:
            print('Mapping pub_date to object:', Question.objects.in_bulk(field_name='pub_date'))
        except ValueError:
            print("Error! 'in_bulk()'s field_name must be a unique field but 'pub_date' isn't")
        # Same behaviour with question_text
        try:
            print('Mapping question_text to object:', Question.objects.in_bulk(field_name='question_text'))
        except ValueError:
            print("Error! 'in_bulk()'s field_name must be a unique field but 'question_text' isn't")
        # Let's filter Questions with odd ID
        questions_with_odd_pk = [pk for pk in Question.objects.values_list('pk', flat=True) if pk % 2 == 1]
        print('Odd primary keys:', questions_with_odd_pk)
        print(f'Mapping odd Questions (pk to object): {Question.objects.in_bulk(id_list=questions_with_odd_pk)}\n')

        # 4) Deleting all Questions
        Question.objects.all().delete()
