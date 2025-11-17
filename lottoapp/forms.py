from django import forms
from .models import LottoEntry, LottoRound

class LottoForm(forms.ModelForm):
    class Meta:
        model = LottoEntry
        fields = ['number1', 'number2', 'number3', 'number4', 'number5', 'number6']

        #숫자 범위 
    def clean(self):
        cleaned_data = super().clean()
        for i in range(1, 7):
            num = cleaned_data.get(f'number{i}')
            if num is not None and (num < 1 or num > 45):
                self.add_error(f'number{i}', '각각 숫자는 1에서 45 사이여야 합니다.')
        return cleaned_data
    def save(self, commit=True, current_round=None):
        entry = super().save(commit=False)
        if current_round:
            entry.round = current_round
            entry.round_number = current_round.round_number
        if commit:
            entry.save()
        return entry