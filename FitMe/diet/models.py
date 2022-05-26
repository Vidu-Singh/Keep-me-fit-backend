# from django.db import models
# from ..register.models import Person
#
# # Create your models here.
# class FoodItems:
#     food_item= models.CharField(max_length=100)
#     fat= models.IntegerField()
#     carb = models.IntegerField()
#     protein = models.IntegerField()
#     calories= models.IntegerField()
#
# class UserDiet:
#     user_id=models.ForeignKey(Person,on_delete=models.CASCADE,related_name= "user")
#     breakfast_food= models.ForeignKey(FoodItems,on_delete=models.CASCADE,related_name= "breakfast")
#     breakfast_quantity= models.IntegerField()
#     lunch_food= models.ForeignKey(FoodItems,on_delete=models.CASCADE,related_name= "lunch")
#     lunch_quantity= models.IntegerField()
#     dinner_food= models.ForeignKey(FoodItems,on_delete=models.CASCADE,related_name= "dinner")
#     dinner_quantity= models.IntegerField()
#     total_calories= models.BigIntegerField()