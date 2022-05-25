from django.core.management.base import BaseCommand

from core.models import (
    Item,
    Question
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Command, that demonstrates such functionality:

        1) Pre-post save signals handling via creating
        2) Pre-post save signals handling via updating
        3) M2M changed (adding values) handling
        4) M2M changed (removing value) handling
        5) M2M changed (clearing relations) handling
        6) Flush tables
        """

        # 1) Creating Question
        print(f'Total count of Items at start: {Item.objects.count()}')
        print(f'Total count of Questions at start: {Question.objects.count()}')
        question = Question.objects.create(question_text='Wonderful Question', pub_date='2022-07-07')

        # 2) Updating question (changing field value and call .save())
        question.question_text = 'Wonderful Question (modified)'
        question.save()

        # 3) Adding m2m values
        print('\nAdding m2m values')
        item1, item2 = Item.objects.create(name='First item!'), Item.objects.create(name='Second item')
        question.items.add(item1, item2)

        # 4) Removing m2m value
        print('\nRemoving m2m value')
        question.items.remove(item2)

        # 5) Clearing m2m relations
        print('\nClearing m2m relations')
        question.items.clear()

        # 6) Deleting all Questions & Choices
        Question.objects.all().delete()
        Item.objects.all().delete()
        print(f'\nTotal count of Questions after delete: {Question.objects.count()}')
        print(f'Total count of Items after delete: {Item.objects.count()}')
