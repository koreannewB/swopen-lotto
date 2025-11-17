from django.db import models

import random
# Create your models here.
class LottoRound(models.Model):
    round_number = models.PositiveIntegerField(default=1)
    winning_numbers = models.JSONField(blank=True, null=True)  # 당첨번호
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.round_number}회차"
#숫자 6개
class LottoEntry(models.Model):
    round_number = models.PositiveIntegerField()
    number1 = models.PositiveSmallIntegerField()
    number2 = models.PositiveSmallIntegerField()
    number3 = models.PositiveSmallIntegerField()
    number4 = models.PositiveSmallIntegerField()
    number5 = models.PositiveSmallIntegerField()
    number6 = models.PositiveSmallIntegerField()
    round = models.ForeignKey(LottoRound, on_delete=models.CASCADE)  # 회차 연결
    created_at = models.DateTimeField(auto_now_add=True)

    def numbers(self):
        return [self.number1, self.number2, self.number3, self.number4, self.number5, self.number6]
    def __str__(self):
        return f"{self.round_number}회차:{self.number1}, {self.number2}, {self.number3}, {self.number4}, {self.number5}, {self.number6}"




