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

# Food Items API
class Food(models.Model):
    food_item= models.CharField(max_length=100,unique=True)
    fat= models.IntegerField()
    carb = models.IntegerField()
    protein = models.IntegerField()
    calories= models.IntegerField()

    def __str__(self):
        return self.food_item

# API for user diet
class UserDiet(models.Model):
    user_diet=models.ForeignKey(Person,on_delete=models.CASCADE,related_name= "user_diet")
    breakfast_food= models.ForeignKey(Food,on_delete=models.CASCADE,related_name= "breakfast",blank=True)
    breakfast_quantity= models.IntegerField()
    lunch_food= models.ForeignKey(Food,on_delete=models.CASCADE,related_name= "lunch",blank=True)
    lunch_quantity= models.IntegerField()
    dinner_food= models.ForeignKey(Food,on_delete=models.CASCADE,related_name= "dinner",blank=True)
    dinner_quantity= models.IntegerField()
    water= models.IntegerField()
    total_calories= models.BigIntegerField()

    def __str__(self):
        return self.total_calories