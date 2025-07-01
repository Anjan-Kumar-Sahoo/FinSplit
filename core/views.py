from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Pool, Bill, BillSplit

@csrf_exempt
def add_expense(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        data = json.loads(request.body)
        title = data['title']
        amount = float(data['amount'])
        paid_by_upi = data['paid_by']
        pool_id = data['pool_id']
        split_method = data['split_method']
        splits = data['splits']

        paid_by = User.objects.get(upi_id=paid_by_upi)
        pool = Pool.objects.get(id=pool_id)

        bill = Bill.objects.create(
            pool=pool,
            paid_by=paid_by,
            title=title,
            amount=amount
        )

        total_split = 0

        if split_method == 'equal':
            share = round(amount / len(splits), 2)
            for person in splits:
                user = User.objects.get(upi_id=person['upi_id'])
                if user != paid_by:
                    BillSplit.objects.create(
                        bill=bill,
                        owed_by=user,
                        owed_to=paid_by,
                        amount=share
                    )

        elif split_method == 'percent':
            for person in splits:
                user = User.objects.get(upi_id=person['upi_id'])
                percent = float(person['amount'])  # amount = percent here
                split_amt = round((percent / 100) * amount, 2)
                total_split += split_amt
                if user != paid_by:
                    BillSplit.objects.create(
                        bill=bill,
                        owed_by=user,
                        owed_to=paid_by,
                        amount=split_amt
                    )

        elif split_method == 'manual':
            for person in splits:
                user = User.objects.get(upi_id=person['upi_id'])
                split_amt = float(person['amount'])
                total_split += split_amt
                if user != paid_by:
                    BillSplit.objects.create(
                        bill=bill,
                        owed_by=user,
                        owed_to=paid_by,
                        amount=split_amt
                    )

        else:
            return JsonResponse({'error': 'Invalid split method'}, status=400)

        return JsonResponse({'message': 'Bill and splits created successfully ✅'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
