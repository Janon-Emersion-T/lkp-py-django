from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class AccountType(models.TextChoices):
    ASSET = "asset", "Asset"
    LIABILITY = "liability", "Liability"
    EQUITY = "equity", "Equity"
    INCOME = "income", "Income"
    EXPENSE = "expense", "Expense"


class Account(BaseModel):
    account_code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )

    name = models.CharField(
        max_length=200,
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        db_index=True,
    )

    description = models.TextField(
        blank=True,
    )

    opening_balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    current_balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    is_system = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["account_code"]

    def __str__(self):
        return f"{self.account_code} - {self.name}"


class TransactionType(models.TextChoices):
    INCOME = "income", "Income"
    EXPENSE = "expense", "Expense"
    TRANSFER = "transfer", "Transfer"
    ADJUSTMENT = "adjustment", "Adjustment"


class Transaction(BaseModel):
    transaction_number = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        db_index=True,
    )

    transaction_date = models.DateField(
        db_index=True,
    )

    description = models.CharField(
        max_length=300,
    )

    reference = models.CharField(
        max_length=120,
        blank=True,
    )

    total_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        ordering = [
            "-transaction_date",
            "-created_at",
        ]

    def __str__(self):
        return self.transaction_number


class LedgerEntry(BaseModel):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="entries",
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="entries",
    )

    debit = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    credit = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    narration = models.CharField(
        max_length=300,
        blank=True,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.transaction} - {self.account}"


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"
    OVERDUE = "overdue", "Overdue"
    CANCELLED = "cancelled", "Cancelled"


class Invoice(BaseModel):
    invoice_number = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
    )

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="invoices",
    )

    project = models.ForeignKey(
        "projects.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invoices",
    )

    quotation = models.ForeignKey(
        "quotations.Quotation",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invoices",
    )

    status = models.CharField(
        max_length=30,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.DRAFT,
        db_index=True,
    )

    issue_date = models.DateField(
        db_index=True,
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    subtotal = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    discount_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    tax_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    paid_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    balance_due = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    notes = models.TextField(blank=True)
    terms = models.TextField(blank=True)

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta(BaseModel.Meta):
        ordering = (
            "-issue_date",
            "-created_at",
        )
        indexes = [
            models.Index(
                fields=("client", "status"),
            ),
            models.Index(
                fields=("status", "due_date"),
            ),
            models.Index(
                fields=("project", "status"),
            ),
        ]

    def __str__(self):
        return self.invoice_number


class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items",
    )

    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("1.00"),
    )
    unit_price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    discount_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    tax_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    subtotal = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    tax_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta(BaseModel.Meta):
        ordering = (
            "sort_order",
            "created_at",
        )
        indexes = [
            models.Index(
                fields=("invoice", "sort_order"),
            ),
        ]

    def __str__(self):
        return self.title


class PaymentMethod(models.TextChoices):
    CASH = "cash", "Cash"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    CARD = "card", "Card"
    PAYPAL = "paypal", "PayPal"
    STRIPE = "stripe", "Stripe"
    CRYPTO = "crypto", "Cryptocurrency"
    OTHER = "other", "Other"


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"
    VOIDED = "voided", "Voided"


class Payment(BaseModel):
    payment_number = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
    )

    invoice = models.ForeignKey(
        Invoice,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="payments",
    )

    client = models.ForeignKey(
        "clients.Client",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="payments",
    )

    project = models.ForeignKey(
        "projects.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="payments",
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="payments",
    )

    transaction = models.OneToOneField(
        Transaction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="payment",
    )

    payment_date = models.DateField(
        db_index=True,
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        default=PaymentMethod.BANK_TRANSFER,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.COMPLETED,
        db_index=True,
    )

    reference = models.CharField(
        max_length=150,
        blank=True,
    )
    notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        ordering = (
            "-payment_date",
            "-created_at",
        )
        indexes = [
            models.Index(
                fields=("invoice", "status"),
            ),
            models.Index(
                fields=("client", "payment_date"),
            ),
            models.Index(
                fields=("account", "payment_date"),
            ),
        ]

    def __str__(self):
        return self.payment_number


class ExpenseCategory(models.TextChoices):
    HOSTING = "hosting", "Hosting"
    OFFICE = "office", "Office"
    SALARY = "salary", "Salary"
    MARKETING = "marketing", "Marketing"
    SOFTWARE = "software", "Software"
    EQUIPMENT = "equipment", "Equipment"
    MISCELLANEOUS = "miscellaneous", "Miscellaneous"


class ExpenseStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    APPROVED = "approved", "Approved"
    PAID = "paid", "Paid"
    REJECTED = "rejected", "Rejected"
    VOIDED = "voided", "Voided"


class Expense(BaseModel):
    expense_number = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="expenses",
    )

    expense_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="expense_postings",
    )

    project = models.ForeignKey(
        "projects.Project",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="expenses",
    )

    transaction = models.OneToOneField(
        Transaction,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="expense",
    )

    expense_date = models.DateField(
        db_index=True,
    )

    category = models.CharField(
        max_length=30,
        choices=ExpenseCategory.choices,
        default=ExpenseCategory.MISCELLANEOUS,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ExpenseStatus.choices,
        default=ExpenseStatus.DRAFT,
        db_index=True,
    )

    vendor = models.CharField(
        max_length=200,
        blank=True,
    )

    description = models.CharField(max_length=300)

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    reference = models.CharField(
        max_length=150,
        blank=True,
    )

    receipt = models.FileField(
        upload_to="finance/expenses/%Y/%m/",
        blank=True,
    )

    notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        ordering = (
            "-expense_date",
            "-created_at",
        )
        indexes = [
            models.Index(
                fields=("status", "expense_date"),
            ),
            models.Index(
                fields=("category", "expense_date"),
            ),
            models.Index(
                fields=("project", "expense_date"),
            ),
        ]

    def __str__(self):
        return self.expense_number


class RecurringFrequency(models.TextChoices):
    WEEKLY = "weekly", "Weekly"
    MONTHLY = "monthly", "Monthly"
    QUARTERLY = "quarterly", "Quarterly"
    YEARLY = "yearly", "Yearly"


class RecurringTransaction(BaseModel):
    name = models.CharField(max_length=200)

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
    )

    source_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="recurring_source_transactions",
    )

    destination_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="recurring_destination_transactions",
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=3,
        default="LKR",
    )

    frequency = models.CharField(
        max_length=20,
        choices=RecurringFrequency.choices,
        default=RecurringFrequency.MONTHLY,
    )

    next_run_date = models.DateField(
        db_index=True,
    )
    last_run_date = models.DateField(
        null=True,
        blank=True,
    )

    description = models.CharField(
        max_length=300,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta(BaseModel.Meta):
        indexes = [
            models.Index(
                fields=("is_active", "next_run_date"),
            ),
        ]

    def __str__(self):
        return self.name
