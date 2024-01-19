class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to " + category.category)
            category.deposit(amount, "Transfer from " + self.category)
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        title = f"{self.category:*^30}\n"
        items = ""
        total = 0
        for item in self.ledger:
            items += f"{item['description'][0:23]:23}" + f"{item['amount']:>7.2f}\n"
            total += item['amount']
        output = title + items + "Total: " + str(total)
        return output

def create_spend_chart(categories):
    total_spent = sum(sum(-item['amount'] for item in category.ledger if item['amount'] < 0) for category in categories)
    category_spent = [(category.category, sum(-item['amount'] for item in category.ledger if item['amount'] < 0)) for category in categories]
    category_percentages = [(category, int((spent / total_spent) * 100)) for category, spent in category_spent]

    chart = "Percentage spent by category\n"
    for percentage in range(100, -10, -10):
        chart += str(percentage).rjust(3) + "|"
        for category, percent in category_percentages:
            chart += " o " if percent >= percentage else "   "
        chart += " \n"

    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"

    max_length = max(len(category) for category, _ in category_percentages)
    for i in range(max_length):
        chart += "     "
        for category, _ in category_percentages:
            chart += category[i] + "  " if i < len(category) else "   "
        if i < max_length - 1:
            chart += "\n"

    return chart
