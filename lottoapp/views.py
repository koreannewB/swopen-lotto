from django.shortcuts import HttpResponse , render, redirect, get_object_or_404
#render : 템플릿을 화면에 출력할때 사용
#rediurect : 다른 url로 이동할때 사용
from .forms import LottoForm

from .models import LottoEntry,LottoRound
#같은 앱의 모델 LottoEntry를 가져옴
#데이터 베이스에 저장조회할때 사용
from django.contrib.admin.views.decorators import staff_member_required
#관리자 뷰
# Create your views here.
import random

def home(request):
    current_round = LottoRound.objects.order_by('-round_number').first()
    #---------------------
    
    if request.method == "POST": #구매 버튼 누를시
        form = LottoForm(request.POST) #폼에 입력된 데이터로 폼 객체 생성  
        if form.is_valid():
            entry = form.save(commit=False)
            entry.round_number = current_round.round_number
            entry.round = current_round #로또의 회차를 현재로또번호의 회차로 설정
            entry.save()
            return redirect('home') #저장후 홈으로 리다이렉트
    else:
        form = LottoForm()

    # 사용자에게 보여줄 이전 회차 로또

    if current_round:
        entries = LottoEntry.objects.filter(round__round_number__lte=current_round.round_number).order_by('round__round_number')
    else:
        entries = []

    return render(request, 'lottoapp/home.html', {
        'current_round': current_round,
        'entries': entries,
        'form': form
    })
    
def buy_lotto(request):
    if request.method == 'POST':
        current_round = LottoRound.objects.order_by('-round_number').first()
        if not current_round:
            current_round = LottoRound.objects.create(round_number=1)

        numbers = [int(request.POST[f'num{i}']) for i in range(1, 7)]

        LottoEntry.objects.create(
            round_number=current_round.round_number,
            number1=numbers[0],
            number2=numbers[1],
            number3=numbers[2],
            number4=numbers[3],
            number5=numbers[4],
            number6=numbers[5],
            round=current_round
        )

    return redirect('home')
def check_entry(request, entry_id):
    entry = get_object_or_404(LottoEntry, id=entry_id)
    if entry.round.is_closed:
        winning_numbers = entry.round.winning_numbers
        user_numbers = entry.numbers()
        match_count = len(set(user_numbers) & set(winning_numbers))

        if match_count == 6:
            result = "1등 당첨!"
        elif match_count == 5:
            result = "2등 당첨!"
        elif match_count == 4:
            result = "3등 당첨!"
        elif match_count == 3:
            result = "4등 당첨!"
        elif match_count == 2:
            result = "5등 당첨!"
        else:
            result = f"{match_count}개 맞음"
    else:
        result = "아직 당첨 번호가 없습니다."

    return render(request, 'lottoapp/check.html', {
        'entry': entry,
        'result': result,
        'winning_numbers': entry.round.winning_numbers if entry.round.is_closed else []
    })








@staff_member_required
def admin_page(request):
    current_round = LottoRound.objects.order_by('-round_number').first()
    rounds = LottoRound.objects.order_by('round_number')
    entries = LottoEntry.objects.filter(round=current_round) if current_round else []    
    previous_rounds = LottoRound.objects.filter(is_closed=True).order_by('round_number')

    round_data = []


    #판매 수익 계산 및 회차별 데이터
    price_per_ticket=1000  #로또 가격
    
    for round in rounds:
        # 회차별 판매 수익: 구매 수 * 1000원 (예시)
        sales_count = LottoEntry.objects.filter(round=round).count()
        sales_amount = sales_count * 1000  # 1회 구매 1000원 가정

        # 당첨자 수 계산 (회차가 종료된 경우만)
        entries = LottoEntry.objects.filter(round=round)
        first = second = third =fourth=fifth =0
        if round.is_closed and round.winning_numbers:
            for entry in entries:
                match_count = len(set(entry.numbers()) & set(round.winning_numbers))
                if match_count == 6:
                    first += 1
                elif match_count == 5:
                    second += 1
                elif match_count == 4:
                    third += 1
                elif match_count == 3:
                    fourth += 1
                elif match_count == 2:
                    fifth += 1
        round_data.append({
            'round': round,
            'sales_count': sales_count,
            'sales_amount': sales_amount,
            'first': first,
            'second': second,
            'third': third,
            'fourth': fourth,
            'fifth': fifth,
        })
    return render(request, 'lottoapp/admin.html', {
        'round_data': round_data,
        'current_round': current_round,
        'previous_rounds': previous_rounds
    })
@staff_member_required
def close_round(request):
    if request.method == 'POST':
        current_round = LottoRound.objects.order_by('-round_number').first()
        if current_round.is_closed:
            return redirect('admin_page')  # 이미 종료된 경우 무시

        # 당첨 번호 랜덤 생성 (1~45, 6개)
        winning_numbers = sorted(random.sample(range(1, 46), 6))
        current_round.winning_numbers = winning_numbers
        current_round.is_closed = True
        current_round.save()

        # 다음 회차 생성
        LottoRound.objects.create(
            round_number=current_round.round_number + 1,
            is_closed=False
        )

    return redirect('admin_page')
@staff_member_required
def next_round(request):
    # 현재 열려있는 회차 닫기
    current = LottoRound.objects.filter(is_closed=False).first()
    if current:
        current.is_closed = True
        current.save()
    
    # 다음 회차 생성
    last_round = LottoRound.objects.order_by('-round_number').first()
    next_number = last_round.round_number + 1 if last_round else 1
    LottoRound.objects.create(round_number=next_number, is_closed=False)
    
    return redirect('admin_page')