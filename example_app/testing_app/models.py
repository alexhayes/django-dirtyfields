from django.db import models
from dirtyfields import DirtyFieldsMixin

class ForeignTestModel(models.Model):
    name = models.CharField(null=True, max_length=50)

class ManyToManyTestModel(models.Model):
    name = models.CharField(null=True, max_length=50)

class TestModel(DirtyFieldsMixin, models.Model):
    """A simple test model to test dirty fields mixin with"""
    boolean = models.BooleanField(default=True)
    characters = models.CharField(blank=True, max_length=80)
    foreign = models.ForeignKey(ForeignTestModel, null=True)
    many_to_many = models.ManyToManyField(ManyToManyTestModel, null=True)
