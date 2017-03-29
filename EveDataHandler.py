#!/usr/bin/env python3

import sqlite3
import random
import time
import datetime
import urllib.request
from lxml import etree

#EIF SpokesPerson's API (WalletJournalOnly)
MyChar = "EIF SpokesPerson"
keyID = 6073947
vCode = "Uidq5umcox6rgLI7GDsAqngaMQWCy4FyWQuRHaBCu9AuTDeYieyY2X5mBGbVM9zH"

def UpdateJournal():
    #Interrogate the API & parse the XML response
    opener = urllib.request.build_opener()
    #Handle EveOnline server not responding (DT for example)
    while True:
        try:
            root = etree.parse(opener.open('https://api.eveonline.com/char/WalletJournal.xml.aspx?keyID={0}&vCode={1}'.format(keyID, vCode))).getroot()
        except:
            time.sleep(600)
            pass
        else:
            break

    rowset = root.find("result/rowset")

    #Create counter for going backwards (oldest to most recent)
    RowCount = 0
    for row in rowset.findall("row"):
        RowCount += 1
    RowCount -= 1

    #Parse all rows
    while RowCount != -1:
        row = rowset[RowCount]
           
        if int(row.get('refTypeID')) == 10:
            TransactionDate = row.get('date')
            Comment = row.get('reason')
            Comment = Comment[6:]
            TransactionFrom = row.get('ownerName1')
            TransactionTo = row.get('ownerName2')
            Amount = float(row.get('amount'))
            RefID = row.get('refID')
            
            #Open DB and verify if RefID is already present
            DB = sqlite3.connect("db.sqlite3")
            Cursor = DB.cursor()
            Cursor.execute("SELECT id FROM WalletJournal_transaction WHERE RefID = {0}".format(RefID))
            #Returns False if the RefID is not already in DB, the following therefore evaluates to True
            if not Cursor.fetchone():

                #Determine TransactionID
                Cursor.execute("SELECT MAX(id) FROM WalletJournal_transaction")
                TopID = Cursor.fetchone()
                TopID = TopID[0]
                try:
                    NewID = int(TopID) + 1
                except TypeError:
                    NewID = 1
                #Determine BalanceAfterTransaction
                NewBalance = 0

                #Write actual entry in DB
                Cursor.execute('INSERT INTO WalletJournal_transaction VALUES ({0},"{1}","{2}","{3}","{4}","{5}",{6},"{7}")'.format(int(NewID), Amount, TransactionDate, Comment, TransactionFrom, TransactionTo, int(RefID), NewBalance))

                #Commit and close cursors and DB
                Cursor.close()
                DB.commit()
                DB.close()
        RowCount -= 1


def UpdateDB():
    DB = sqlite3.connect("db.sqlite3")
    Cursor = DB.cursor()
    Cursor.execute("SELECT * FROM WalletJournal_transaction")
    Investments = Cursor.fetchall()
    Cursor.execute("SELECT * FROM WalletJournal_charactertotalinvestment")
    CharsInDB = Cursor.fetchall()
    Cursor.execute("SELECT RefID FROM WalletJournal_pasttransactions")
    PastTransactions = Cursor.fetchall()
    PastTransactions = [int(t[0]) for t in PastTransactions]
    Cursor.execute('SELECT * FROM WalletJournal_transaction')
    AllDivs = Cursor.fetchall()

    TotalInvestors = 0
    TotalInvestments = 0
    TotalDivPaid = 0
    TotalRefferalsPaid = 0
    InvestorList = []

    for row in CharsInDB :
        if row[1] not in InvestorList:
            InvestorList.append(row[1])
        if row[2] == 0:
            Cursor.execute('DELETE from WalletJournal_charactertotalinvestment WHERE CharacterName = "{0}"'.format(row[1]))

    #Update Investments based on transactions
    for row in Investments:
        #If transaction not already processed
        if int(row[6]) not in PastTransactions:
            Cursor.execute("SELECT MAX(id) FROM WalletJournal_pasttransactions")
            TopID = Cursor.fetchone()
            TopID = TopID[0]
            try:
                NewID = int(TopID) + 1
            except TypeError:
                NewID = 1
            #Insert Entry
            Cursor.execute('INSERT INTO WalletJournal_pasttransactions VALUES ({0}, {1})'.format(NewID, row[6]))
            
            if row[4] not in InvestorList and row[4] != MyChar:
                InvestorList.append(row[4])

                #Determine ID
                Cursor.execute("SELECT MAX(id) FROM WalletJournal_charactertotalinvestment")
                TopID = Cursor.fetchone()
                TopID = TopID[0]
                try:
                    NewID = int(TopID) + 1
                except TypeError:
                    NewID = 1
                #Insert Entry
                Cursor.execute('INSERT INTO WalletJournal_charactertotalinvestment VALUES ({0},"{1}",{2},{3},{4},{5})'.format(NewID, row[4], row[1], 0, 0, 0))
                Comment = row[3]
                Comment = Comment.replace("\r","")
                Comment = Comment.replace("\n","")

#TEST CODE FOR REFFERALS
                if Comment in InvestorList:
                    print("Trying to apply a refferal for {0}".format(Comment))
                    Cursor.execute('UPDATE WalletJournal_charactertotalinvestment SET Refferals = Refferals + 1  WHERE CharacterName = "{0}"'.format(Comment))
                    Cursor.execute('SELECT Refferals FROM WalletJournal_charactertotalinvestment WHERE CharacterName = "{0}"'.format(Comment))
                    Refferals = Cursor.fetchone()
                    Refferals = Refferals[0]
                    if Refferals in (1, 5):
                        Cursor.execute('SELECT TotalInvestment FROM WalletJournal_charactertotalinvestment WHERE CharacterName = "{0}"'.format(Comment))
                        MaxRefferalPayment = Cursor.fetchone()
                        MaxRefferalPayment = float(MaxRefferalPayment[0])*0.05
                        if MaxRefferalPayment > 25000000:
                            MaxRefferalPayment = 25000000
                        if MaxRefferalPayment > row[1]:
                            Cursor.execute('UPDATE WalletJournal_charactertotalinvestment SET RefferalBalance = RefferalBalance + {0} WHERE CharacterName = "{1}"'.format(row[1], Comment))
                        else:
                            Cursor.execute('UPDATE WalletJournal_charactertotalinvestment SET RefferalBalance = RefferalBalance + {0} WHERE CharacterName = "{1}"'.format(MaxRefferalPayment, Comment))
#TEST CODE FOR REFFERALS


            elif row[4] != MyChar:
                #Get new investment value
                Cursor.execute('SELECT TotalInvestment FROM WalletJournal_charactertotalinvestment WHERE CharacterName = "{0}"'.format(row[4]))
                CurrentInvestment = Cursor.fetchone()
                CurrentInvestment = CurrentInvestment[0]
                NewInvestment = float(CurrentInvestment) + float(row[1])
                #Update Entry
                Cursor.execute('UPDATE WalletJournal_charactertotalinvestment SET TotalInvestment = {0} WHERE CharacterName = "{1}"'.format(NewInvestment, row[4]))
            
            if row[4] == MyChar and "WITHDRAWAL" in row[3]:
                print("Trying to apply withdrawal")
                #Get new investment value
                Cursor.execute('SELECT TotalInvestment FROM WalletJournal_charactertotalinvestment WHERE CharacterName = "{0}"'.format(row[5]))
                CurrentInvestment = Cursor.fetchone()
                CurrentInvestment = CurrentInvestment[0]
                NewInvestment = float(CurrentInvestment) + float(row[1])
                #Update Entry
                Cursor.execute('UPDATE WalletJournal_charactertotalinvestment SET TotalInvestment = {0} WHERE CharacterName = "{1}"'.format(NewInvestment, row[5]))

#TEST CODE FOR REFFERALS
            if row[4] == MyChar and "REFFERAL" in row[3]:
                print("Trying to apply refferal payment")
                #Get new investment value
                Cursor.execute('UPDATE WalletJournal_charactertotalinvestment SET RefferalBalance = RefferalBalance + {0} WHERE CharacterName = "{1}"'.format(row[1], row[5]))
#TEST CODE FOR REFFERALS

    #Update Statistics
    for row in CharsInDB:
        TotalInvestors += 1
        TotalInvestments += row[2]
    for row in AllDivs:
        if row[4] == MyChar and "INTEREST" in row[3]:
            TotalDivPaid += row[1]            
        if row[4] == MyChar and "REFFERAL" in row[3]:
            TotalRefferalsPaid += row[1]
    try:
        AvInv = TotalInvestments / TotalInvestors
    except:
        AvInv = TotalInvestments / 1

    LiquidISK = TotalInvestments + TotalDivPaid + TotalRefferalsPaid
    NextDiv = TotalInvestments * 0.05
    
    try:
        Cursor.execute('INSERT INTO WalletJournal_statistics VALUES ({0},{1},{2},{3},{4},{5},{6},{7})'.format(1, TotalInvestors, TotalInvestments, AvInv, TotalDivPaid, LiquidISK, NextDiv, TotalRefferalsPaid))
    except:    
        Cursor.execute('UPDATE WalletJournal_statistics SET TotalInvestors = {0}, TotalInvestments = {1}, AverageInvestment = {2}, TotalDividendsPaid = {3}, TotalISKLeft = {4}, NextDivPayment = {5}, TotalRefferalsPaid = {6} WHERE id = 1'.format(TotalInvestors, TotalInvestments, AvInv, TotalDivPaid, LiquidISK, NextDiv, TotalRefferalsPaid))

    #Reset table
    Cursor.execute('DELETE FROM WalletJournal_weeklypayment')
    #Update WeeklyPayments
    for row in CharsInDB:
        #Determine amount to transfer
        WeekPayment = float(row[2])*0.05
        #Determine ID
        Cursor.execute("SELECT MAX(id) FROM WalletJournal_weeklypayment")
        TopID = Cursor.fetchone()
        TopID = TopID[0]
        try:
            NewID = int(TopID) + 1
        except TypeError:
            NewID = 1
        #Insert Entry
        Cursor.execute('INSERT INTO WalletJournal_weeklypayment VALUES ({0},"{1}",{2})'.format(NewID, row[1], WeekPayment))

    Cursor.close()
    DB.commit()
    DB.close()


while True:
    UpdateJournal()
    UpdateDB()
    time.sleep(900)
