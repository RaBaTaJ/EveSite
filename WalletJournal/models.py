from django.db import models

# Create your models here.
class Transaction(models.Model):
    TransactionAmount = models.FloatField("Amount", max_length=75)
    BalanceAfterTransaction = models.CharField("Balance", max_length=75)
    TransactionDateTime = models.DateTimeField("Date & Time")
    TransactionComment = models.CharField("Comment", max_length=75)
    TransactionFrom = models.CharField("From", max_length=75)
    TransactionTo = models.CharField("To", max_length=75)
    RefID = models.CharField("RefID", max_length=25)

    def __str__(self):
        return self.TransactionComment

class CharacterTotalInvestment(models.Model):
    CharacterName = models.CharField("Character Name", max_length=75)
    TotalInvestment = models.FloatField("Total Investment", max_length=75)
    Refferals = models.IntegerField("Number of Refferals")
    RefferalBalance = models.FloatField("Refferal Balance", max_length=75)
    LastRefferalAmount = models.FloatField("Last Refferal Amount", max_length=75)


    def __str__(self):
        return self.CharacterName

class WeeklyPayment(models.Model):
    CharacterName = models.CharField("From", max_length=75)
    PaymentAmount = models.FloatField("Payment Amount", max_length=75)

    def __str__(self):
        return self.CharacterName

class PastTransactions(models.Model):
    RefID = models.CharField("RefID", max_length=75)

class Statistics(models.Model):
    TotalInvestors = models.IntegerField("Total Investors")
    TotalInvestments = models.FloatField("Total Invested Value", max_length=75)
    AverageInvestment = models.FloatField("Average Investment", max_length=75)
    TotalDividendsPaid = models.FloatField("Total Dividends Paid", max_length=75)
    TotalRefferalsPaid = models.FloatField("Total Refferals Paid", max_length=75)
    TotalISKLeft = models.FloatField("Total ISK Left", max_length=75)
    NextDivPayment = models.FloatField("Next Dividend Payment", max_length=75)