from django.core.management.base import BaseCommand
from django.forms.models import model_to_dict

from core.models import Question


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Get all Questions instances
        print('\nAll existing Question instances:', Question.objects.all())

        # Creating new Question via manager-method .create()
        question = Question.objects.create(question_text='What a question, wow!', pub_date='2022-05-02')
        print('\nNewly created Question instance:', question)
        print('Question values:', model_to_dict(question))

        # Updating Question via Queryset-method .update()
        Question.objects.filter(question_text='What a question, wow!').update(pub_date='3033-05-05')
        question.refresh_from_db(fields=['pub_date'])
        print('\nUpdated Question values via Queryset-method:', model_to_dict(question))

        # Deleting object via model method .delete()
        question.delete()

        # Creating new Question via model-class instance and .save()
        question = Question(question_text='New text', pub_date='2022-03-03')
        try:
            print('Already created?', model_to_dict(Question.objects.get(question_text='New text')))
        except Question.DoesNotExist:
            print('\nThere is no object yet!')
            question.save()
            print('But after save it is!', model_to_dict(Question.objects.get(question_text='New text')))

        # Updating Question object via .save()
        question.question_text = 'After second save text'
        question.save()
        print('\nAfter second save Question object was updated:', model_to_dict(question))

        # OR-methods (get_or_create, update_or_create)
        # both methods returns tuple of (object, created) where created is a boolean flag that represents
        # if object was created or it was just found

        # get_or_create was found
        question, created = Question.objects.get_or_create(
            question_text='After second save text',
            defaults={'question_text': 'Created by get_or_create', 'pub_date': '2000-01-01'}
        )
        print('\nGet_or_create was found:', model_to_dict(question))
        # get_or_create was not found, created new one
        question, created = Question.objects.get_or_create(
            question_text='Really new text',
            defaults={'question_text': 'Created by get_or_create', 'pub_date': '2000-01-01'}
        )
        print('Get_or_create was not found:', model_to_dict(question))

        # update_or_create
        question, created = Question.objects.update_or_create(
            question_text='Created by get_or_create',
            defaults={'pub_date': '2222-02-22'}
        )
        print('\nQuestion was found, updated just pub_date:', model_to_dict(question))
        # get_or_create was not found, created new one
        question, created = Question.objects.update_or_create(
            question_text='Really new text',
            defaults={'question_text': 'Created by update_or_create', 'pub_date': '2777-07-07'}
        )
        print('Question was not found, created new one:', model_to_dict(question))

        # Deleting all Questions using Queryset-method delete()
        Question.objects.all().delete()
        print('All Questions were deleted!', Question.objects.all())
