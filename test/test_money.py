import sys
sys.path.append("/home/nick/Money/src")
from money import stream


buffer = 50
balance = 100
income = [15.50 * 5.75 * 5 * 0.75]
expenses = [6.50 * 5 + buffer]
noise = 0.10
periods = 40

flow = stream(balance, income, expenses, noise, periods)
