class Category:
    def __init__(self, category) -> None:
        self.category = category
        self.ledger = []
        self.balance = 0.0
    
    def __repr__(self) -> str:
        asteriscs = int((30 - len(self.category)) / 2)
        header = '*' * asteriscs + '{}'.format(self.category) + '*' * asteriscs + '\n'
        listing = ''
        for element in self.ledger:
            description = element['description']
            amount = '%.2f' % element['amount']
            space_between = 30 - len(amount) - len(description)
            if len(description) > 23:
                space_between = 7 - len(amount)
                listing += '{}'.format(description[:23]) + ' ' * space_between +'{}'.format(amount) + '\n'
            else: 
                listing += '{}'.format(description) + ' ' * space_between +'{}'.format(amount) + '\n'
        total = 'Total: {:.2f}'.format(self.balance)
        printed = header + listing + total
        return printed

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount

    def withdraw(self, amount, description=''): 
        if amount <= self.balance:
            self.ledger.append({'amount': -abs(amount), 'description': description})
            self.balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self.balance
    
    def transfer(self, amount, category):
        if amount <= self.balance:
            category.ledger.append({'amount': amount, 'description': 'Transfer from {}'.format(self.category)})
            category.balance += amount
            self.withdraw(amount, 'Transfer to {}'.format(category.category))
            return True
        return False
    
    def check_funds(self, amount):
        if amount > self.balance:
            return False
        return True



def create_spend_chart(categories):
    percentages = []
    to_name = lambda x: x.category
    for category in categories:
        withdrawls = 0
        for element in category.ledger:
            amount = element['amount']
            withdrawls += amount if amount < 0 else 0    
        percentages.append(withdrawls)

    suma = sum(percentages)
    percentages = list(map(lambda x: x/suma * 100, percentages))

    chart = 'Percentage spent by category\n'
    for n in range(100, -1, -10):
        chart += str(n).rjust(3, ' ') + '|'
        for percentage in percentages:
            if percentage > n:
                chart += ' o '
            else:
                chart += '   '
        chart += ' \n'
    chart += "    ----------\n"

    footer = ''  
    for n in range(len(max(list(map(to_name,categories)), key=len))):
        # print(n)
        footer += '    ' 
        for category in categories:
            if n >= len(category.category):
                footer += '   '
            else:
                footer += ' {} '.format(category.category[n])
        footer += ' \n'
                
    return chart + footer[:-1]