from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Pool, Bill, BillSplit, PoolMember
from decimal import Decimal


@csrf_exempt
def add_expense(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)

    try:
        print("🔵 Raw Data:", request.body)
        data = json.loads(request.body)
        title = data['title']
        amount = float(data['amount'])
        paid_by_upi = data['paid_by']
        pool_id = data['pool_id']
        split_method = data['split_method']
        splits = data['splits']

        try:
            paid_by = User.objects.get(upi_id=paid_by_upi)
        except User.DoesNotExist:
            return JsonResponse({'error': f'User {paid_by_upi} not found'}, status=404)

        try:
            pool = Pool.objects.get(id=pool_id)
        except Pool.DoesNotExist:
            return JsonResponse({'error': f'Pool with id {pool_id} not found'}, status=404)

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
                upi = person.get('upi_id')
                if not upi:
                    continue
                try:
                    user = User.objects.get(upi_id=upi)
                except User.DoesNotExist:
                    return JsonResponse({'error': f'User {upi} not found'}, status=404)
                if user != paid_by:
                    BillSplit.objects.create(
                        bill=bill,
                        owed_by=user,
                        owed_to=paid_by,
                        amount=share
                    )

        elif split_method == 'percent':
            for person in splits:
                try:
                    user = User.objects.get(upi_id=person['upi_id'])
                except User.DoesNotExist:
                    return JsonResponse({'error': f'User {person["upi_id"]} not found'}, status=404)
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
                try:
                    user = User.objects.get(upi_id=person['upi_id'])
                except User.DoesNotExist:
                    return JsonResponse({'error': f'User {person["upi_id"]} not found'}, status=404)
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

def verify_upi_id(upi_id):
    # Simulated UPI check: must end with '@upi'
    return upi_id.endswith('@upi')

@csrf_exempt
def create_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
        upi_id = data.get('upi_id')

        if not verify_upi_id(upi_id):
            return JsonResponse({'error': 'Invalid UPI ID'}, status=400)

        user, created = User.objects.get_or_create(upi_id=upi_id)

        return JsonResponse({
            'upi_id': user.upi_id,
            'created': created
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def add_pool_member(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
        pool_id = data.get('pool_id')
        upi_id = data.get('upi_id')

        if not verify_upi_id(upi_id):
            return JsonResponse({'error': 'Invalid UPI ID'}, status=400)

        try:
            user = User.objects.get(upi_id=upi_id)
        except User.DoesNotExist:
            return JsonResponse({'error': f'User {upi_id} not found'}, status=404)

        try:
            pool = Pool.objects.get(id=pool_id)
        except Pool.DoesNotExist:
            return JsonResponse({'error': f'Pool with id {pool_id} not found'}, status=404)

        PoolMember.objects.get_or_create(user=user, pool=pool)

        return JsonResponse({'message': f'{upi_id} added to pool {pool.name}'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def settle_debt(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)

        from_upi = data.get('from_upi')
        to_upi = data.get('to_upi')
        amount_raw = data.get('amount')

        if not from_upi or not to_upi or not amount_raw:
            return JsonResponse({'error': 'from_upi, to_upi, and amount are required'}, status=400)

        amount_to_settle = Decimal(str(amount_raw))
        remaining = amount_to_settle

        from_user = User.objects.filter(upi_id=from_upi).first()
        to_user = User.objects.filter(upi_id=to_upi).first()

        if not from_user:
            return JsonResponse({'error': f'User {from_upi} not found'}, status=404)
        if not to_user:
            return JsonResponse({'error': f'User {to_upi} not found'}, status=404)

        unsettled_splits = BillSplit.objects.filter(
            owed_by=from_user,
            owed_to=to_user,
            is_settled=False
        ).order_by('amount')

        if not unsettled_splits.exists():
            return JsonResponse({'error': 'No unsettled dues found'}, status=400)

        settled_ids = []

        for split in unsettled_splits:
            if remaining <= 0:
                break

            if remaining >= split.amount:
                remaining -= split.amount
                split.amount = Decimal('0.00')
                split.is_settled = True
            else:
                split.amount -= remaining
                remaining = Decimal('0.00')

            split.save()
            settled_ids.append(split.id)

        settled_amount = amount_to_settle - remaining

        return JsonResponse({
            'message': f'Settled ₹{settled_amount:.2f} from {from_upi} to {to_upi}',
            'bill_splits_settled': settled_ids
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

   
def add_expense_page(request):
    return render(request, 'core/add_expense.html')

def pool_summary_page(request):
    return render(request, 'core/pool_summary.html')

def user_summary_page(request):
    return render(request, 'core/user_summary.html')

def settle_debt_page(request):
    return render(request, 'core/settle_dues.html')

