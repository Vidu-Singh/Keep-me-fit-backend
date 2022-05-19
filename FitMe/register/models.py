from enum import Enum

from django.db import models

# Registration model
class Person(models.Model):
    email=models.EmailField(max_length=80,null=False)
    password= models.CharField(max_length=50, null=False)
    code= models.CharField(max_length=10)

# Profile model
class Profile(models.Model):
    user_id= models.ForeignKey(Person,on_delete=models.CASCADE,related_name= "user")
    name= models.CharField(max_length=150)
    dob= models.DateField()
    class Gender(Enum):
        Male = ('Male', 'Male')
        Female=('Female', 'Female')
        Other = ('Other', 'Other')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    gender=models.CharField(
        max_length=32,
        choices=[x.value for x in Gender],
        default=Gender.get_value('Male'),
        null=False
    )

    height= models.CharField(max_length=50)
    weight= models.DecimalField(max_digits=5,decimal_places=1)
    allergies= models.CharField(max_length=500)
    health_issues=models.CharField(max_length=500)

# Coach model
class Coach(models.Model):
    expert_name= models.CharField(max_length=200)
    experience= models.IntegerField()
    expertise_area= models.CharField(max_length=100)
