from abc import ABC, abstractmethod
import copy


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        
        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,
            
            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        } 
        
    def get_positive_effects(self):
        return self.positive_effects
    
    def get_negative_effects(self):
        return self.negative_effects


class AbstractEffect(Hero, ABC):
    def __init__(self, base=None):
        self.stats = []
        self.positive_effects = []
        self.negative_effects = []
        if isinstance(base, AbstractEffect):
            self.base = base
        else:
            self.base = Hero()
    
    @abstractmethod    
    def get_stats(self): # Возвращает итоговые хараетеристики
        pass             # после применения эффекта 
        
    
    @abstractmethod
    def get_positive_effects(self):
        pass
    
    @abstractmethod
    def get_negative_effects(self):
        pass



class AbstractPositive(AbstractEffect, ABC):
    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass
    

class Berserk(AbstractPositive):
    def get_positive_effects(self):
        positive_effects = copy.deepcopy(self.base.get_positive_effects())
        positive_effects.append("Berserk")
        return positive_effects

    def get_stats(self):
        if isinstance(self.base, AbstractEffect):
            stats = copy.deepcopy(self.base.get_stats())
        else:
            stats = copy.deepcopy(self.base.stats)
        stats["Strength"] +=7
        stats["Perception"] -=3
        stats["Endurance"] +=7
        stats["Charisma"] -=3
        stats["Intelligence"] -=3
        stats["Agility"] +=7
        stats["Luck"] +=7
        stats["HP"] +=50
        return stats


class Blessing(AbstractPositive):
    def get_positive_effects(self):
        positive_effects = copy.deepcopy(self.base.get_positive_effects())
        positive_effects.append("Blessing")
        return positive_effects
        
    def get_stats(self):
        if isinstance(self.base, AbstractEffect):
            stats = copy.deepcopy(self.base.get_stats())
        else:
            stats = copy.deepcopy(self.base.stats)
        stats["Strength"] +=2
        stats["Perception"] +=2
        stats["Endurance"] +=2
        stats["Charisma"] +=2
        stats["Intelligence"] +=2
        stats["Agility"] +=2
        stats["Luck"] +=2
        return stats


class AbstractNegative(AbstractEffect, ABC):
    @abstractmethod
    def get_negative_effects(self):
        pass

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_stats(self):
        pass


class Weakness(AbstractNegative):
    def get_negative_effects(self):
        negative_effects = copy.deepcopy(self.base.get_negative_effects())
        negative_effects.append("Weakness")
        return negative_effects

    def get_stats(self):
        if isinstance(self.base, AbstractEffect):
            stats = copy.deepcopy(self.base.get_stats())
        else:
            stats = copy.deepcopy(self.base.stats)
        stats["Strength"] -=4
        stats["Endurance"] -=4
        stats["Agility"] -=4
        return stats


class Curse(AbstractNegative):
    def get_negative_effects(self):
        negative_effects = copy.deepcopy(self.base.get_negative_effects())
        negative_effects.append("Curse")
        return negative_effects

    def get_stats(self):
        if isinstance(self.base, AbstractEffect):
            stats = copy.deepcopy(self.base.get_stats())
        else:
            stats = copy.deepcopy(self.base.stats)
        stats["Strength"] -=2
        stats["Perception"] -=2
        stats["Endurance"] -=2
        stats["Charisma"] -=2
        stats["Intelligence"] -=2
        stats["Agility"] -=2
        stats["Luck"] -=2
        return stats


class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        negative_effects = copy.deepcopy(self.base.get_negative_effects())
        negative_effects.append("EvilEye")
        return negative_effects

    def get_stats(self):
        if isinstance(self.base, AbstractEffect):
            stats = copy.deepcopy(self.base.get_stats())
        else:
            stats = copy.deepcopy(self.base.stats)
        stats["Luck"] -=10
        return stats