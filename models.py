# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
# Create your models here.
# 要取得會員的model要這樣寫
from oscar.core.compat import get_user_model
from apps.user.models import User
User = get_user_model()

class Type(models.Model):
    ResType = models.CharField(max_length=10, null=True)
    def __str__(self):
        return self.ResType

class ResProf(models.Model):
    ResName = models.CharField(max_length=30, null=True) # 餐廳名稱
    address = models.CharField(max_length=30, null=True)
    ResLike = models.DecimalField(default=50,max_digits=6, decimal_places=0  ) # always add default value!
    score = models.DecimalField(default=3,max_digits=1, decimal_places=0)
    last_reserv = models.CharField(max_length=20)
    ResType = models.ManyToManyField(Type) # 餐廳的料理類型
    country = models.CharField(max_length=10) # 哪個國家的餐廳
    def __str__(self):
      return self.ResName

class Date(models.Model):
    # Date 是用來存星期幾有開店
    DayOfWeek = models.CharField(max_length=1) # 表示星期幾
    Start = models.CharField(max_length=8) # 開始營業時間
    CloseMid = models.CharField(max_length=8, null=True) # 中午結束營業時間（店家中午不一定休息，所以允許空字串）
    StartMid = models.CharField(max_length=8, null=True) # 下午重新開始營業時間（店家中午不一定休息，所以允許空字串）
    Close = models.CharField(max_length=8) # 結束營業時間
    restaurant = models.ForeignKey(ResProf) # 有開店的日子，一對多的關係
    def __str__(self):
        return self.DayOfWeek + self.Start + '~' + self.Close

class Phone(models.Model):
    phoneNum = models.CharField(max_length=15) # 電話號碼
    restaurant = models.ForeignKey(ResProf) # 考慮到一間店可能有多隻聯絡電話
    def __str__(self):
        return self.phoneNum

class Dish(models.Model):
    DishName = models.CharField(max_length=20, null=True) # 菜名
    price = models.DecimalField(max_digits=6, decimal_places=0) # 價錢
    isSpicy = models.BooleanField()
    restaurant = models.ForeignKey(ResProf) # 餐點的餐廳
    def __str__(self):
        return self.DishName

class EatUser(models.Model):
    # 今天吃什麼的使用者，用來紀錄使用者的飲食習慣
    UpperUser = models.OneToOneField(User)
    FDish = models.ForeignKey(Dish, null=True)
    FType = models.ForeignKey(Type, null=True)
    def __str__(self):
        return str(self.UpperUser)

class FavorType(models.Model):
    EatUser = models.ForeignKey(EatUser)
    type = models.ForeignKey(Type, null=True)
    freq = models.DecimalField(max_digits=4, decimal_places=0) # 紀錄你吃這種類型的餐廳幾次

class FavorDish(models.Model):
    EatUser = models.ForeignKey(EatUser)
    dish = models.ForeignKey(Dish, null=True)
    freq = models.DecimalField(max_digits=4, decimal_places=0) # 紀錄你常常吃哪一道菜

class ResFavorDish(models.Model):
    # 用來紀錄餐廳的各個餐點受到歡迎的程度
    Res = models.ForeignKey(ResProf)
    dish = models.ForeignKey(Dish, null=True)
    freq = models.DecimalField(max_digits=6, decimal_places=0)
    dateOfMon_Year = models.DateTimeField() # 儲存這個月該餐點的銷售量就好


class Order(models.Model):
    # 餐廳的訂單，是一個一對多的關係，因為一間餐廳會有多張訂單
    restaurant = models.ForeignKey(ResProf)
    create = models.DateTimeField() # 訂單的精確時間
    date = models.CharField(max_length=10) # 訂單的年月日
    period = models.CharField(max_length=3) # 標示是早中午哪個時段
    total = models.DecimalField(max_digits=8, decimal_places=0) # 該訂單總額
    def __str__(self):
        return self.date + ' ' + str(self.restaurant)

class UserOrder(models.Model):
    # 以同一道菜去彙整的訂單子集合
    orderUser = models.ForeignKey(EatUser, null=True) # 為了要紀錄使用者有定過哪些菜色（這邊很有問題）
    total = models.DecimalField(max_digits=5, decimal_places=0) # 該使用者這次定餐的總額
    order = models.ForeignKey(Order) # 隸屬的訂單
    create = models.DateTimeField(null=True) # 訂單的精確時間
    def __str__(self):
        return str(self.orderUser) + str(self.order)

class SmallOrder(models.Model):
    dish = models.ForeignKey(Dish)
    amount = models.DecimalField(max_digits=3, decimal_places=0)
    UserOrder = models.ForeignKey(UserOrder)
    def __str__(self):
        return str(self.dish) + ' ' + str(self.amount) + '份'
