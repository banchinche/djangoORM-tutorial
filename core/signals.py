from django.db.models.signals import (
    m2m_changed,
    post_save,
    pre_save
)
from django.dispatch import receiver
from django.forms.models import model_to_dict

from .models import Question


@receiver(pre_save, sender=Question)
def pre_save_question_handler(sender, instance, **kwargs):
    print('\nPRE_SAVE HANDLER')
    print(f'Such instance will be saved: {model_to_dict(instance)}')


@receiver(post_save, sender=Question)
def post_save_question_handler(sender, instance, created, **kwargs):
    print('\nPOST_SAVE HANDLER')
    if created:
        print('Question was created!')
    else:
        print('Question was updated!')
    print('Question was saved')


@receiver(m2m_changed, sender=Question.items.through)
def m2m_changed_question(sender, instance, action, **kwargs):
    print('M2M_CHANGED HANDLER')
    print(f'Action: {action}')
