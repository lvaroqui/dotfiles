#!/usr/bin/env python3

import csv
import sys
import os
from datetime import datetime


def process_bourso_csv(input_file, month):
    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        accounts = {}
        for row in reader:
            account_label = row["accountLabel"]

            if account_label == "VISA ULTIM":
                description = row["label"]
                description = description.removeprefix("CARTE ")
                [date, description] = description.split(" ", 1)
                try:
                    dt = datetime.strptime(date, "%d/%m/%y")
                    date = dt.strftime("%Y-%m-%d")
                except ValueError:
                    pass
            else:
                date = row["dateVal"]
                description = row["label"]

            account = "À trier"
            amount = row["amount"]

            transactionMonth = date.split("-")[1]
            if month != transactionMonth:
                continue

            accounts[account_label] = accounts.get(account_label, [])
            accounts[account_label].append(
                {
                    "date": date,
                    "description": description,
                    "account": account,
                    "amount": amount,
                }
            )

    for account_label, rows in accounts.items():
        print(f"Account: {account_label}")
        filename = f"bourso-{account_label.replace(' ', '_').lower()}.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["date", "description", "account", "amount"],
                delimiter=";",
            )
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} rows to {filename}")


if __name__ == "__main__":
    input_file = sys.argv[1]
    month = sys.argv[2]
    process_bourso_csv(input_file, month)
