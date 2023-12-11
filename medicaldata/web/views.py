# -*- coding: utf-8 -*-

from hashlib import sha256
import json
from time import time

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import BlockChain


class Block:
    # Эта функция ниже создана для создания самого первого блока и установки его хэша равным "0"

    def __init__(self, timestamp=None, data=None):
        self.timestamp = timestamp or time()
        self.data = [] if data is None else data
        self.prevHash = None
        self.nonce = 0
        self.hash = self.getHash()

    # Получаем необходимый хэш
    def getHash(self):

        hash = sha256()
        hash.update(str(self.prevHash).encode("utf-8"))
        hash.update(str(self.timestamp).encode("utf-8"))
        hash.update(str(self.data).encode("utf-8"))
        hash.update(str(self.nonce).encode("utf-8"))
        return hash.hexdigest()

    # Получаем данные
    def mine(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.getHash()


class Blockchain:
    # Это функция для проверки работы и используется для успешного майнинга блока
    def __init__(self):
        self.chain = [Block(str(int(time())))]
        self.difficulty = 1
        self.blockTime = 30000

    # Последний блок
    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    # Добавление блока в строй
    def addBlock(self, block):
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()
        block.mine(self.difficulty)
        self.chain.append(block)

        self.difficulty += (-1, 1)[
            int(time()) - int(self.getLastBlock().timestamp) < self.blockTime
        ]

    # Ликвидный ли блок
    def isValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            if (
                currentBlock.hash != currentBlock.getHash()
                or prevBlock.hash != currentBlock.prevHash
            ):
                return False

        return True

    def __repr__(self):
        return json.dumps(
            [
                {
                    "data": item.data,
                    "timestamp": item.timestamp,
                    "nonce": item.nonce,
                    "hash": item.hash,
                    "prevHash": item.prevHash,
                }
                for item in self.chain
            ],
            indent=4,
        )


# Создание приложение
@csrf_exempt
def index(request):
    blchn = Blockchain()

    if request.method == "POST":
        blchn.addBlock(
            Block(
                str(int(time())),
                (
                    {
                        "Name": request.POST.get("from", "Undefined"),
                        "Lastname": request.POST.get("to", "Undefined"),
                        "Height": request.POST.get("Height", "Undefined"),
                        "Age": request.POST.get("Age", "Undefined"),
                        "Weight": request.POST.get("Weight", "Undefined"),
                        "Body temparatyre": request.POST.get("Body", "Undefined"),
                        "Pressure": request.POST.get("pressure"),
                        "Oxygen in blood": request.POST.get("Oxygen"),
                        "Blood": request.POST.get("Blood", "Undefined"),
                        "Rate": request.POST.get("Rate", "Undefined"),
                        "Pulse": request.POST.get("amount", "Undefined"),
                    }
                ),
            )
        )
        print(blchn)
        
        blockchain_medical_database = BlockChain()
        
        blockchain_medical_database.blockchain_medical_data = blchn
        blockchain_medical_database.save()
        
        return render(
            request,
            "pages/home.html",
            {
                "Name": request.POST.get("from", "Undefined"),
                "Lastname": request.POST.get("to", "Undefined"),
                "Height": request.POST.get("Height", "Undefined"),
                "Age": request.POST.get("Age", "Undefined"),
                "Weight": request.POST.get("Weight", "Undefined"),
                "Body": request.POST.get("Body", "Undefined"),
                "Pressure": request.POST.get("pressure"),
                "Oxygen": request.POST.get("Oxygen"),
                "Blood": request.POST.get("Blood", "Undefined"),
                "Rate": request.POST.get("Rate", "Undefined"),
                "Pulse": request.POST.get("amount", "Undefined"),
            },
        )

    return render(request, "pages/index.html")


# РЕЗУЛЬТАТ В КОНСОЛИ
