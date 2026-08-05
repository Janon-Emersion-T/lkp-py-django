from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Sum

from .models import Account, AccountType, LedgerEntry


MONEY_QUANTIZER = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(
        MONEY_QUANTIZER,
        rounding=ROUND_HALF_UP,
    )


def account_balance(account: Account) -> Decimal:
    totals = account.entries.aggregate(
        total_debit=Sum("debit"),
        total_credit=Sum("credit"),
    )

    total_debit = totals["total_debit"] or Decimal("0.00")
    total_credit = totals["total_credit"] or Decimal("0.00")

    if account.account_type in (
        AccountType.ASSET,
        AccountType.EXPENSE,
    ):
        movement = total_debit - total_credit
    else:
        movement = total_credit - total_debit

    return money(account.opening_balance + movement)


def refresh_account_balance(account: Account) -> Account:
    account.current_balance = account_balance(account)

    account.save(
        update_fields=[
            "current_balance",
            "updated_at",
        ],
    )

    return account


def validate_balanced_entries(
    entries: list[dict],
) -> None:
    total_debit = sum(
        (
            Decimal(str(entry.get("debit", "0.00")))
            for entry in entries
        ),
        Decimal("0.00"),
    )

    total_credit = sum(
        (
            Decimal(str(entry.get("credit", "0.00")))
            for entry in entries
        ),
        Decimal("0.00"),
    )

    if money(total_debit) != money(total_credit):
        raise ValueError(
            "Ledger entries must have equal debit and credit totals."
        )

    if money(total_debit) <= Decimal("0.00"):
        raise ValueError(
            "Ledger transaction amount must be greater than zero."
        )

    for entry in entries:
        debit = Decimal(str(entry.get("debit", "0.00")))
        credit = Decimal(str(entry.get("credit", "0.00")))

        if debit < 0 or credit < 0:
            raise ValueError(
                "Ledger debit and credit values cannot be negative."
            )

        if debit > 0 and credit > 0:
            raise ValueError(
                "A ledger entry cannot contain both debit and credit."
            )

        if debit == 0 and credit == 0:
            raise ValueError(
                "A ledger entry must contain a debit or credit."
            )
