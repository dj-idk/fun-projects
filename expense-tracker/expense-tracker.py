"""
A simple CLI application that allow users to track their expenses.
"""

import json
import argparse
from datetime import datetime


REPORT_FILE = "expense_report.json"


class ExpenseTracker:

    def __init__(self, file=REPORT_FILE):
        self.file = file
        self.expenses = self.load_expenses()

    def load_expenses(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print(
                "Warning: Could not read JSON file, initializing an empty expense list."
            )
            return {"total_count": 0, "summary": 0, "expenses": []}

    def save_expenses(self):
        try:
            with open(self.file, "w") as f:
                json.dump(self.expenses, f, indent=4)
        except IOError:
            print("Error: Could not save expenses to file.")

    def add_expense(
        self,
        amount,
        description,
        category="General",
    ):
        expnses = self.expenses["expenses"]
        new_id = max((expense["id"] for expense in expnses), default=0) + 1
        new_expense = {
            "id": new_id,
            "amount": amount,
            "description": description,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        expnses.append(new_expense)
        self.expenses["total_count"] = len(expnses)
        self.expenses["summary"] += amount
        self.save_expenses()
        print(f"Expense {new_id} was successfully added.")

    def update_expense(self, expense_id, amount, description, category):
        for expense in self.expenses["expenses"]:
            if expense["id"] == int(expense_id):
                expense["amount"] = amount
                expense["description"] = description
                expense["category"] = category
                expense["updated_at"] = datetime.now().isoformat()
                self.save_expenses()
                print(f"Expense {expense_id} was successfully updated.")
                return
        print("Error: Expense not found.")

    def delete_expense(self, expense_id):
        for expense in self.expenses["expenses"]:
            if expense["id"] == int(expense_id):
                self.expenses["expenses"].remove(expense)
                self.expenses["total_count"] -= 1
                self.expenses["summary"] -= expense["amount"]
                self.save_expenses()
                print(f"Expense {expense_id} was successfully deleted.")
                return
        print("Error: Expense not found.")

    def list_expenses(self):
        print("# ID   Date        Description   Amount")
        for expense in self.expenses["expenses"]:
            date = expense["created_at"].split("T")[0]  # Extract YYYY-MM-DD
            print(
                f"# {expense['id']}   {date}   {expense['description']}   ${expense['amount']}"
            )

    def view_expenses_by_month(self, month, year=datetime.now().year):
        total = 0
        for expense in self.expenses["expenses"]:
            expense_date = datetime.fromisoformat(expense["updated_at"])
            if expense_date.year == year and expense_date.month == month:
                total += expense["amount"]
                print(
                    f"ID: {expense['id']}, Description: {expense['description']}, "
                    f"Amount: {expense['amount']}, Category: {expense['category']}"
                )
        print(f"Total expenses for {year}-{month:02d}: {total}")

    def view_expenses_by_category(self, category):
        total = 0
        for expense in self.expenses["expenses"]:
            if category == expense["category"]:
                total += expense["amount"]
                print(
                    f"ID: {expense['id']}, Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['updated_at']}"
                )
        print(f"Total expenses for {category}: {total}")

    def view_summary(self, month=None):
        if month:
            total = 0
            for expense in self.expenses["expenses"]:
                expense_date = datetime.fromisoformat(expense["updated_at"])
                if expense_date.month == month:
                    total += expense["amount"]
            print(f"Total expenses for month {month}: ${total}")
        else:
            print(f"Total expenses: ${self.expenses['summary']}")

    def set_monthly_budget(self, month, budget):
        self.expenses["monthly_budget"] = {month: budget}
        self.save_expenses()
        print(f"Monthly budget for {month} set to {budget}")

    def export_expenses(self, file):
        try:
            with open(file, "w") as f:
                for expense in self.expenses["expenses"]:
                    f.write(
                        f"{expense['id']},{expense['description']},{expense['amount']},{expense['category']}\n"
                    )
            print(f"Expenses exported to {file}")
        except IOError:
            print("Error: Could not export expenses to file.")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add Expense
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument(
        "--description", type=str, required=True, help="Description of the expense"
    )
    add_parser.add_argument("--amount", type=float, required=True, help="Amount spent")
    add_parser.add_argument(
        "--category", type=str, default="General", help="Category of the expense"
    )

    # Update Expense
    update_parser = subparsers.add_parser("update", help="Update an existing expense")
    update_parser.add_argument(
        "--id", type=int, required=True, help="ID of the expense"
    )
    update_parser.add_argument(
        "--description", type=str, help="Description of the expense"
    )
    update_parser.add_argument("--amount", type=float, help="Amount spent")
    update_parser.add_argument("--category", type=str, help="Category of the expense")

    # Delete Expense
    delete_parser = subparsers.add_parser("delete", help="Delete an existing expense")
    delete_parser.add_argument(
        "--id", type=int, required=True, help="ID of the expense"
    )

    # List Expenses
    list_parser = subparsers.add_parser("list", help="List all expenses")

    # View Expenses by month
    view_parser = subparsers.add_parser("monthly", help="View expenses by month")
    view_parser.add_argument(
        "--month", type=int, required=True, help="Month to filter by(1-12)"
    )
    view_parser.add_argument("--year", type=int, help="Year to filter by")

    # View Expenses by category
    category_parser = subparsers.add_parser(
        "category", help="View expenses by category"
    )
    category_parser.add_argument(
        "--category", type=str, required=True, help="Category to filter by"
    )

    # View Summary
    summary_parser = subparsers.add_parser("summary", help="View expense summary")
    summary_parser.add_argument("--month", type=int, help="Filter by month")

    # Set Monthly Budget
    budget_parser = subparsers.add_parser("budget", help="Set monthly budget")
    budget_parser.add_argument(
        "--month", type=int, required=True, help="Month to set budget for"
    )
    budget_parser.add_argument(
        "--budget", type=float, required=True, help="Monthly budget"
    )

    # Export Expenses
    export_parser = subparsers.add_parser("export", help="Export expenses to a file")
    export_parser.add_argument(
        "--file", type=str, required=True, help="File to export expenses to"
    )

    args = parser.parse_args()
    tracker = ExpenseTracker()

    if args.command == "add":
        tracker.add_expense(args.amount, args.description, args.category)
    elif args.command == "update":
        tracker.update_expense(args.id, args.amount, args.description, args.category)
    elif args.command == "delete":
        tracker.delete_expense(args.id)
    elif args.command == "list":
        tracker.list_expenses()
    elif args.command == "monthly":
        tracker.view_expenses_by_month(args.month, args.year)
    elif args.command == "category":
        tracker.view_expenses_by_category(args.category)
    elif args.command == "summary":
        tracker.view_summary(args.month)
    elif args.command == "budget":
        tracker.set_monthly_budget(args.month, args.budget)
    elif args.command == "export":
        tracker.export_expenses(args.file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
