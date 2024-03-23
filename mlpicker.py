import random

class Player:
    def __init__(self,id,hero,role):
        self.id = id
        self.hero = hero
        self.role = role

Heroes = ["Aamon", "Akai", "Aldous", "Alice", "Alpha", "Alucard", "Angela", "Argus", "Atlas", "Aulus", "Aurora", "Badang", "Balmond", "Bane", "Barats", "Baxia", "Beatrix", "Belerick", "Benedetta", "Brody", "Bruno", "Carmilla", "Cecilion", "Chang\'e", "Chou", "Claude", "Clint", "Cyclops", "Diggie", "Dyrroth", "Esmeralda", "Estes", "Eudora", "Fanny", "Faramis", "Floryn", "Franco", "Freya", "Gatotkaca", "Gloo", "Gord", "Granger", "Grock", "Guinevere", "Gusion", "Hanabi", "Hanzo", "Harith", "Harley", "Hayabusa", "Helcurt", "Hilda", "Hylos", "Irithel", "Jawhead", "Johnson", "Kadita", "Kagura", "Kaja", "Karina", "Karrie", "Khaleed", "Khufra", "Kimmy", "Lancelot", "Lapu-lapu", "Layla", "Leomord", "Lesley", "Ling", "Lolita", "Luo Yi", "Lunox", "Lylia", "Martis", "Masha", "Melissa", "Minotour", "Minsitthar", "Miya", "Moskov", "Mathilda", "Nana", "Natalia", "Natan", "Odette", "Paquito", "Pharsa", "Phoveus", "Edith", "Popol & Kupa", "Rafaela", "Roger", "Ruby", "Saber", "Selena", "Silvanna", "Sun", "Terizla", "Thamuz", "Tigreal", "Uranus", "Vale", "Valentina", "Valir", "Vexana", "Wanwan", "Xavier", "X-Borg", "Yi Sun-Shin", "Yin", "Yu Zhong", "Yve", "Zhask", "Zilong", "Julian",]
Roles = ["Exp Laner","Gold Laner","Mid Laner","Jungler","Roamer"]

def getrandomhero(id):
    return Player(id,random.choice(Heroes),random.choice(Roles))