from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.clients.models import Client

from .models import (
    Account,
    AccountType,
    InvoiceStatus,
    PaymentMethod,
)
from .services import FinanceService


User = get_user_model()


class FinanceServiceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="finance-admin",
            email="finance-admin@example.com",
            password="StrongPassword123!",
        )

        self.client = Client.objects.create(
            company_name="Finance Client",
            client_code="LKP-CL-00001",
            created_by=self.admin,
            updated_by=self.admin,
        )

        self.request = type(
            "Request",
            (),
            {
                "auth": self.admin,
                "META": {},
            },
        )()

        self.bank = FinanceService.create_account(
            request=self.request,
            values={
                "account_code": "1000",
                "name": "Main Bank Account",
                "account_type": AccountType.ASSET,
                "opening_balance": Decimal("1000.00"),
                "currency": "LKR",
            },
        )

        self.income = FinanceService.create_account(
            request=self.request,
            values={
                "account_code": "4000",
                "name": "Service Revenue",
                "account_type": AccountType.INCOME,
                "currency": "LKR",
            },
        )

        self.expense_account = FinanceService.create_account(
            request=self.request,
            values={
                "account_code": "5000",
                "name": "Office Expenses",
                "account_type": AccountType.EXPENSE,
                "currency": "LKR",
            },
        )

    def test_account_opening_balance_is_applied(self):
        self.assertEqual(
            self.bank.current_balance,
            Decimal("1000.00"),
        )

    def test_unbalanced_transaction_is_rejected(self):
        with self.assertRaises(ValueError):
            FinanceService.post_transaction(
                request=self.request,
                transaction_type="income",
                transaction_date=date.today(),
                description="Invalid transaction",
                entries=[
                    {
                        "account": self.bank,
                        "debit": Decimal("100.00"),
                        "credit": Decimal("0.00"),
                    },
                ],
            )

    def test_balanced_transaction_updates_accounts(self):
        FinanceService.post_transaction(
            request=self.request,
            transaction_type="income",
            transaction_date=date.today(),
            description="Service income",
            entries=[
                {
                    "account": self.bank,
                    "debit": Decimal("500.00"),
                    "credit": Decimal("0.00"),
                },
                {
                    "account": self.income,
                    "debit": Decimal("0.00"),
                    "credit": Decimal("500.00"),
                },
            ],
        )

        self.bank.refresh_from_db()
        self.income.refresh_from_db()

        self.assertEqual(
            self.bank.current_balance,
            Decimal("1500.00"),
        )
        self.assertEqual(
            self.income.current_balance,
            Decimal("500.00"),
        )

    def test_invoice_totals_are_calculated(self):
        invoice = FinanceService.create_invoice(
            request=self.request,
            values={
                "client": self.client,
                "currency": "LKR",
                "discount_amount": Decimal("1000.00"),
            },
            items=[
                {
                    "title": "Website Development",
                    "quantity": Decimal("1.00"),
                    "unit_price": Decimal("100000.00"),
                    "discount_amount": Decimal("0.00"),
                    "tax_rate": Decimal("10.00"),
                },
            ],
        )

        self.assertEqual(
            invoice.subtotal,
            Decimal("100000.00"),
        )
        self.assertEqual(
            invoice.tax_amount,
            Decimal("10000.00"),
        )
        self.assertEqual(
            invoice.total_amount,
            Decimal("109000.00"),
        )
        self.assertEqual(
            invoice.balance_due,
            Decimal("109000.00"),
        )

    def test_partial_and_full_payments_update_invoice(self):
        invoice = FinanceService.create_invoice(
            request=self.request,
            values={
                "client": self.client,
                "currency": "LKR",
            },
            items=[
                {
                    "title": "Software Project",
                    "quantity": Decimal("1.00"),
                    "unit_price": Decimal("100000.00"),
                    "discount_amount": Decimal("0.00"),
                    "tax_rate": Decimal("0.00"),
                },
            ],
        )

        FinanceService.record_payment(
            request=self.request,
            invoice=invoice,
            account=self.bank,
            income_account=self.income,
            payment_date=date.today(),
            amount=Decimal("40000.00"),
            method=PaymentMethod.BANK_TRANSFER,
        )

        invoice.refresh_from_db()

        self.assertEqual(
            invoice.status,
            InvoiceStatus.PARTIALLY_PAID,
        )
        self.assertEqual(
            invoice.balance_due,
            Decimal("60000.00"),
        )

        FinanceService.record_payment(
            request=self.request,
            invoice=invoice,
            account=self.bank,
            income_account=self.income,
            payment_date=date.today(),
            amount=Decimal("60000.00"),
            method=PaymentMethod.BANK_TRANSFER,
        )

        invoice.refresh_from_db()

        self.assertEqual(
            invoice.status,
            InvoiceStatus.PAID,
        )
        self.assertEqual(
            invoice.balance_due,
            Decimal("0.00"),
        )
        self.assertIsNotNone(invoice.paid_at)

    def test_overpayment_is_rejected(self):
        invoice = FinanceService.create_invoice(
            request=self.request,
            values={
                "client": self.client,
            },
            items=[
                {
                    "title": "Small service",
                    "quantity": Decimal("1.00"),
                    "unit_price": Decimal("1000.00"),
                    "discount_amount": Decimal("0.00"),
                    "tax_rate": Decimal("0.00"),
                },
            ],
        )

        with self.assertRaises(ValueError):
            FinanceService.record_payment(
                request=self.request,
                invoice=invoice,
                account=self.bank,
                income_account=self.income,
                payment_date=date.today(),
                amount=Decimal("1001.00"),
                method=PaymentMethod.CASH,
            )

    def test_expense_posts_double_entry_transaction(self):
        expense = FinanceService.record_expense(
            request=self.request,
            account=self.bank,
            expense_account=self.expense_account,
            expense_date=date.today(),
            category="office",
            vendor="Office Supplier",
            description="Office supplies",
            amount=Decimal("250.00"),
        )

        self.bank.refresh_from_db()
        self.expense_account.refresh_from_db()

        self.assertEqual(
            expense.amount,
            Decimal("250.00"),
        )
        self.assertEqual(
            self.bank.current_balance,
            Decimal("750.00"),
        )
        self.assertEqual(
            self.expense_account.current_balance,
            Decimal("250.00"),
        )
        self.assertIsNotNone(expense.transaction)


from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api


class FinanceApiTests(TestCase):
    def setUp(self):
        self.api_client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="finance-api-admin",
            email="finance-api-admin@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

        self.client_record = Client.objects.create(
            company_name="Finance API Client",
            client_code="LKP-CL-00970",
            created_by=self.admin,
            updated_by=self.admin,
        )

    def create_account(
        self,
        *,
        code,
        name,
        account_type,
        opening_balance="0.00",
    ):
        return self.api_client.post(
            "/finance/accounts",
            json={
                "account_code": code,
                "name": name,
                "account_type": account_type,
                "opening_balance": opening_balance,
                "currency": "LKR",
                "is_active": True,
            },
            headers=self.headers,
        )

    def create_invoice(self):
        return self.api_client.post(
            "/finance/invoices",
            json={
                "client_id": str(
                    self.client_record.pk
                ),
                "currency": "LKR",
                "discount_amount": "1000.00",
                "items": [
                    {
                        "title": "Business Website",
                        "description": "Website development",
                        "quantity": "1.00",
                        "unit_price": "100000.00",
                        "discount_amount": "0.00",
                        "tax_rate": "10.00",
                        "sort_order": 0,
                    },
                ],
            },
            headers=self.headers,
        )

    def test_superuser_can_create_account(self):
        response = self.create_account(
            code="1100",
            name="Cash in Hand",
            account_type="asset",
            opening_balance="5000.00",
        )

        self.assertEqual(response.status_code, 201)

        body = response.json()

        self.assertEqual(
            body["account_code"],
            "1100",
        )
        self.assertEqual(
            body["current_balance"],
            "5000.00",
        )

    def test_duplicate_account_code_is_rejected(self):
        self.create_account(
            code="1100",
            name="Cash in Hand",
            account_type="asset",
        )

        response = self.create_account(
            code="1100",
            name="Duplicate Cash Account",
            account_type="asset",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "duplicate_account_code",
        )

    def test_superuser_can_list_accounts(self):
        self.create_account(
            code="1100",
            name="Cash in Hand",
            account_type="asset",
        )

        response = self.api_client.get(
            "/finance/accounts",
            data={
                "search": "Cash",
                "account_type": "asset",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["pagination"][
                "total_items"
            ],
            1,
        )

    def test_superuser_can_post_balanced_transaction(self):
        bank = self.create_account(
            code="1200",
            name="Main Bank",
            account_type="asset",
        ).json()

        income = self.create_account(
            code="4100",
            name="Service Revenue",
            account_type="income",
        ).json()

        response = self.api_client.post(
            "/finance/transactions",
            json={
                "transaction_type": "income",
                "transaction_date": str(date.today()),
                "description": "Website income",
                "reference": "TXN-001",
                "entries": [
                    {
                        "account_id": bank["id"],
                        "debit": "25000.00",
                        "credit": "0.00",
                        "narration": "Bank receipt",
                    },
                    {
                        "account_id": income["id"],
                        "debit": "0.00",
                        "credit": "25000.00",
                        "narration": "Service revenue",
                    },
                ],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["total_amount"],
            "25000.00",
        )
        self.assertEqual(
            len(response.json()["entries"]),
            2,
        )

    def test_unbalanced_transaction_is_rejected(self):
        bank = self.create_account(
            code="1200",
            name="Main Bank",
            account_type="asset",
        ).json()

        income = self.create_account(
            code="4100",
            name="Service Revenue",
            account_type="income",
        ).json()

        response = self.api_client.post(
            "/finance/transactions",
            json={
                "transaction_type": "income",
                "transaction_date": str(date.today()),
                "description": "Invalid transaction",
                "entries": [
                    {
                        "account_id": bank["id"],
                        "debit": "1000.00",
                        "credit": "0.00",
                    },
                    {
                        "account_id": income["id"],
                        "debit": "0.00",
                        "credit": "900.00",
                    },
                ],
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "invalid_ledger_transaction",
        )

    def test_superuser_can_create_invoice(self):
        response = self.create_invoice()

        self.assertEqual(response.status_code, 201)

        body = response.json()

        self.assertTrue(
            body["invoice_number"].startswith(
                "LKP-INV-"
            )
        )
        self.assertEqual(
            body["subtotal"],
            "100000.00",
        )
        self.assertEqual(
            body["tax_amount"],
            "10000.00",
        )
        self.assertEqual(
            body["total_amount"],
            "109000.00",
        )
        self.assertEqual(
            body["balance_due"],
            "109000.00",
        )

    def test_superuser_can_get_invoice_detail(self):
        created = self.create_invoice().json()

        response = self.api_client.get(
            f"/finance/invoices/{created['id']}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["invoice_number"],
            created["invoice_number"],
        )

    def test_superuser_can_record_partial_payment(self):
        invoice = self.create_invoice().json()

        bank = self.create_account(
            code="1200",
            name="Main Bank",
            account_type="asset",
        ).json()

        income = self.create_account(
            code="4100",
            name="Service Revenue",
            account_type="income",
        ).json()

        response = self.api_client.post(
            "/finance/payments",
            json={
                "invoice_id": invoice["id"],
                "account_id": bank["id"],
                "income_account_id": income["id"],
                "payment_date": str(date.today()),
                "amount": "40000.00",
                "method": "bank_transfer",
                "reference": "PAY-001",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["amount"],
            "40000.00",
        )

        detail = self.api_client.get(
            f"/finance/invoices/{invoice['id']}",
            headers=self.headers,
        )

        self.assertEqual(
            detail.json()["status"],
            InvoiceStatus.PARTIALLY_PAID,
        )
        self.assertEqual(
            detail.json()["balance_due"],
            "69000.00",
        )

    def test_overpayment_is_rejected_by_api(self):
        invoice = self.create_invoice().json()

        bank = self.create_account(
            code="1200",
            name="Main Bank",
            account_type="asset",
        ).json()

        income = self.create_account(
            code="4100",
            name="Service Revenue",
            account_type="income",
        ).json()

        response = self.api_client.post(
            "/finance/payments",
            json={
                "invoice_id": invoice["id"],
                "account_id": bank["id"],
                "income_account_id": income["id"],
                "payment_date": str(date.today()),
                "amount": "200000.00",
                "method": "bank_transfer",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["code"],
            "invalid_payment",
        )

    def test_superuser_can_record_expense(self):
        bank = self.create_account(
            code="1200",
            name="Main Bank",
            account_type="asset",
            opening_balance="10000.00",
        ).json()

        office_expense = self.create_account(
            code="5100",
            name="Office Expense",
            account_type="expense",
        ).json()

        response = self.api_client.post(
            "/finance/expenses",
            json={
                "account_id": bank["id"],
                "expense_account_id": (
                    office_expense["id"]
                ),
                "expense_date": str(date.today()),
                "category": "office",
                "vendor": "Office Supplier",
                "description": "Printer paper",
                "amount": "1500.00",
                "currency": "LKR",
                "reference": "EXP-001",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["amount"],
            "1500.00",
        )
        self.assertEqual(
            response.json()["status"],
            "paid",
        )

    def test_finance_summary_returns_balances(self):
        bank = self.create_account(
            code="1200",
            name="Main Bank",
            account_type="asset",
            opening_balance="10000.00",
        ).json()

        income = self.create_account(
            code="4100",
            name="Service Revenue",
            account_type="income",
        ).json()

        self.api_client.post(
            "/finance/transactions",
            json={
                "transaction_type": "income",
                "transaction_date": str(date.today()),
                "description": "Service income",
                "entries": [
                    {
                        "account_id": bank["id"],
                        "debit": "5000.00",
                        "credit": "0.00",
                    },
                    {
                        "account_id": income["id"],
                        "debit": "0.00",
                        "credit": "5000.00",
                    },
                ],
            },
            headers=self.headers,
        )

        response = self.api_client.get(
            "/finance/summary",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["total_assets"],
            "15000.00",
        )
        self.assertEqual(
            response.json()["total_income"],
            "5000.00",
        )
        self.assertEqual(
            response.json()["profit"],
            "5000.00",
        )

    def test_unauthenticated_finance_request_is_rejected(self):
        response = self.api_client.get(
            "/finance/accounts"
        )

        self.assertEqual(response.status_code, 401)
