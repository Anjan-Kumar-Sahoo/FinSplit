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

# 🟢 Pool-Level Summary
def get_pool_summary(request, pool_id):
    try:
        pool = Pool.objects.get(id=pool_id)
        splits = BillSplit.objects.filter(bill__pool=pool, is_settled=False)

        summary = []
        for split in splits:
            summary.append({
                "owed_by": split.owed_by.upi_id,
                "owed_to": split.owed_to.upi_id,
                "amount": float(split.amount),
                "bill_title": split.bill.title
            })

        return JsonResponse({
            "pool": pool.name,
            "summary": summary
        })

    except Pool.DoesNotExist:
        return JsonResponse({"error": "Pool not found"}, status=404)

# 🟢 User-Level Summary
def get_user_summary(request, upi_id):
    try:
        user = User.objects.get(upi_id=upi_id)

        gets_from = BillSplit.objects.filter(owed_to=user, is_settled=False)
        owes_to = BillSplit.objects.filter(owed_by=user, is_settled=False)

        gets = []
        for g in gets_from:
            gets.append({
                "from": g.owed_by.upi_id,
                "amount": float(g.amount),
                "bill": g.bill.title
            })

        owes = []
        for o in owes_to:
            owes.append({
                "to": o.owed_to.upi_id,
                "amount": float(o.amount),
                "bill": o.bill.title
            })

        return JsonResponse({
            "upi_id": user.upi_id,
            "gets_from": gets,
            "owes_to": owes
        })

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
