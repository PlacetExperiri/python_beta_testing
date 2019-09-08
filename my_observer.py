from abc import ABC, abstractmethod


class ObservableEngine(Engine):
    def __init__(self): 
        self.__subscribers = set() # При инициализации множество подписчиков звдвется пустым
    
    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber) # Для того чтобы подмисать пользователя, он добавляется во множество подписчиков
        
    def unsubscribe(self, subscriber=None):
        if (subscriber in self.__subscribers):
            self.__subscribers.remove(subscriber) # Удаление подписчика из списка
        
    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message) # Отправка уведомления всем подписчикам


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, message):
        self.achievements.add(message['title'])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, message):
        if message not in self.achievements:
            self.achievements.append(message)