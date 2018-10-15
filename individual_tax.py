# encoding: utf-8

'''
calculate individual tax
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def calc_tax(salary, allowance, endowment, medical, unemployment, housing):
    insurance_fund = endowment + medical + unemployment + housing
    pretax_income = salary + allowance + 50
    tax_base = salary + allowance - insurance_fund - 3500
    # print(tax_base)

    level = 0
    tax_rate = 0.0
    quick_deduction = 0
    if tax_base < 1500:
        level = 1
        tax_rate = 0.03
        quick_deduction = 0
    elif tax_base < 4500:
        level = 2
        tax_rate = 0.10
        quick_deduction = 105
    elif tax_base < 9000:
        level = 3
        tax_rate = 0.20
        quick_deduction = 555
    elif tax_base < 35000:
        level = 4
        tax_rate = 0.25
        quick_deduction = 1005
    elif tax_base < 55000:
        level = 5
        tax_rate = 0.30
        quick_deduction = 2755
    elif tax_base < 80000:
        level = 6
        tax_rate = 0.35
        quick_deduction = 5505
    else:
        level = 7
        tax_rate = 0.45
        quick_deduction = 13505

    tax = tax_base * tax_rate - quick_deduction
    tax_income = pretax_income - insurance_fund - 10 - tax

    return (level, tax, tax_income)


if __name__ == '__main__':
    level, tax, tax_income = calc_tax(10000, 600, 200, 50, 10, 300)
    print('level={}  tax={:.2f} tax_income={:.2f}'.format(level, tax, tax_income))

    '''
    levels = []
    taxes = []
    tax_incomes = []
    funds = np.arange(300, 5000, 300)
    for fund in funds:
        level, tax, tax_income = calc_tax(10000, 631, 225.54, 56.39, 14.10, fund)
        #print('level={}  tax={:.2f} tax_income={:.2f}'.format(level, tax, tax_income))
        levels.append(level)
        taxes.append(tax)
        tax_incomes.append(tax_income)

    ax = plt.subplot(111)
    ax.xaxis.set_major_locator(MultipleLocator(1000))
    plt.plot(funds, levels)
    plt.title('level')

    plt.subplot(132)
    plt.plot(funds, taxes)
    plt.title('tax')

    plt.subplot(133)
    plt.plot(funds, tax_incomes)
    plt.title('tax_income')

    #plt.legend(loc='best', ncol=1)
    #plt.axis([0, 5000, None, None])
    #plt.gca().xaxis.set_major_locator(MultipleLocator(100))
    plt.tight_layout() 
    plt.show()
    '''
