import json
import pymongo


class Database():
    def __init__(self, db_token=None) -> None:
        self.db_token = db_token

    def connect(self):
        self.myClient = pymongo.MongoClient(self.db_token)
        self.mydb = self.myClient["balances"]
        self.mycollection = self.mydb["balances_tursu"]
        # self.mycollectionConfig = self.mydb['config']

    def getBalances(self):
        balances = self.mycollection.find_one()
        del balances['_id']
        return balances

    def updateBalances(self, data):
        self.mycollection.find_one_and_update(
            self.getBalances(), {'$set': data})

    def getBalancesFromJson(self):
        with open('balances.json', encoding='UTF-8') as file:
            balances = json.load(file)
        return balances

    def updateBalancesToJson(self, data):
        with open('balances.json', 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
