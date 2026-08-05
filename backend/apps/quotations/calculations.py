from decimal import Decimal, ROUND_HALF_UP

from .models import Quotation, QuotationItem


MONEY_QUANTIZER = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(
        MONEY_QUANTIZER,
        rounding=ROUND_HALF_UP,
    )


def calculate_item(item: QuotationItem) -> QuotationItem:
    gross = money(item.quantity * item.unit_price)

    discount = money(
        min(
            max(item.discount_amount, Decimal("0.00")),
            gross,
        )
    )

    subtotal = money(gross - discount)

    tax_rate = max(item.tax_rate, Decimal("0.00"))

    tax_amount = money(
        subtotal * tax_rate / Decimal("100")
    )

    total_amount = money(subtotal + tax_amount)

    item.subtotal = subtotal
    item.tax_amount = tax_amount
    item.total_amount = total_amount

    return item


def calculate_quotation_totals(
    quotation: Quotation,
) -> Quotation:
    items = quotation.items.all()

    subtotal = sum(
        (item.subtotal for item in items),
        Decimal("0.00"),
    )
    item_tax = sum(
        (item.tax_amount for item in items),
        Decimal("0.00"),
    )

    subtotal = money(subtotal)

    quotation_discount = money(
        min(
            max(
                quotation.discount_amount,
                Decimal("0.00"),
            ),
            subtotal,
        )
    )

    taxable_total = money(
        subtotal - quotation_discount
    )

    total_tax = money(
        item_tax + max(
            quotation.tax_amount,
            Decimal("0.00"),
        )
    )

    quotation.subtotal = subtotal
    quotation.discount_amount = quotation_discount
    quotation.tax_amount = total_tax
    quotation.total_amount = money(
        taxable_total + total_tax
    )

    return quotation
