from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50, blank=True)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    items = models.ManyToManyField(Item)
    pub_date = models.DateField()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    new_field = models.CharField(max_length=10, blank=True)
