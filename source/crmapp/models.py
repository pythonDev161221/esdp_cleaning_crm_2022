from django.db import models

# Create your models here.


class TypeOfCleaning(models.Model):
    cleaning_type = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"{self.cleaning_type}"


class TypeOfObjectAndClean(models.Model):
    object_to_clean = models.ForeignKey('crmapp.TypeOfObject', on_delete=models.CASCADE)
    cleaning = models.ForeignKey(TypeOfCleaning, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cleaning} {self.object_to_clean} {self.price}"


class TypeOfObject(models.Model):
    object_type = models.CharField(max_length=200, null=False, blank=False)
    cleanings = models.ManyToManyField(TypeOfCleaning, through=TypeOfObjectAndClean,
                                       related_name='type_of_objects')

    def __str__(self):
        return f"{self.object_type}"
