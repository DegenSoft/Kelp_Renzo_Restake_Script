import asyncio
import csv
from datetime import datetime
from degensoft.decryption import is_base64
import os

class WalletCSV:
    def __init__(self, config):
        now = datetime.now()
        formatted = now.strftime("%d-%m-%H-%M")  # Day-Month-Hour-Minute
        self.file_path =f'results/{formatted}-result.csv'
        self.config = config
        self._initialize()

    def _initialize(self):
        
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["wallet_address", "status", "action", "error_message","private_key"])

    async def add_wallet(self,pk: str, wallet_address, status, action, error_message=None):
        if self.config.append_private_keys_to_stat:
            if self.config.append_only_encrypted and not is_base64(pk):
                pk = ''
        else: pk = ''
        with open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        
        for i in range(1, len(rows)):
            if rows[i][0] == wallet_address and rows[i][2] == action and rows[i][1] == status:
                return
            
        async with asyncio.Lock():
            with open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([wallet_address, status, action, error_message,pk])

    async def get_failed_wallets(self):
        failed_wallets = []
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["status"] == "error":
                    failed_wallets.append(row["wallet_address"])
        return failed_wallets

    async def update_wallet_status(self, wallet_address, status, module, error_message=None):
        rows = []
        with open(self.file_path, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        
        for i in range(1, len(rows)):
            if rows[i][0] == wallet_address and rows[i][2] == module and rows[i][1] == 'start':
                rows[i][1] = status
                rows[i][3] = error_message
                break

        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

# Пример использования:
# import asyncio
# db = WalletCSV()
# asyncio.run(db.add_wallet("0x1234...", "error", "stake", 10, "Insufficient funds"))
# failed_wallets = asyncio.run(db.get_failed_wallets())
