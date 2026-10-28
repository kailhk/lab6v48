#Варіант 48. Заявки на оцифрування
#Завдання 1. Формування й відправлення пакетів


class Item:  # батько для записів
    def __init__(self, item_type, value, item_id):  # item_type - A або B, value - значення x, item_id - номер команди ADD
        self.type = item_type
        self.value = value
        self.id = item_id

    def get_score(self):
        raise NotImplementedError  # якщо викличемо через батьківський клас

    def get_label(self):
        return str(self.id)  # як запис виглядає у виводі


# Два типи A і B з різною оцінкою по завданню
class ItemA(Item):  # наслідування
    def get_score(self):
        return 2 * self.value


class ItemB(Item):  # наслідування
    def get_score(self):
        return 4 * self.value + 5


# Пакет містить об'єкти записів, має свою оцінку як і запис
class Packet:
    def __init__(self, items):
        self.items = items  # записи у порядку вилучення зі стека

    def get_score(self):
        return sum(item.get_score() for item in self.items)  # сума оцінок записів пакета

    def get_label(self):
        return ",".join(str(item.id) for item in self.items)  # id через коми без пробілів


# Спільний батько для стека і черги 
class Structure:
    def __init__(self, capacity=None):
        self.capacity = capacity
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def is_full(self):
        if self.capacity is None:
            return False
        return len(self.items) >= self.capacity

    def size(self):
        return len(self.items)  # кількість елементів

    def add(self, item):
        if self.is_full():
            return False  # стан не міняється
        self.items.append(item)
        return True

    def remove(self):
        raise NotImplementedError  # у кожного класу своє правило

    def peek(self):
        raise NotImplementedError

    def order(self):
        raise NotImplementedError  # елементи у порядку наступного вилучення

    def get_sum(self):
        return sum(item.get_score() for item in self.items)  # сума порожньої структури = 0

    def get_state(self, separator=" "):
        if self.is_empty():
            return "-"  # порожньо по завданню
        return separator.join(item.get_label() for item in self.order())


# клас Стек (LIFO)
class Stack(Structure):
    def remove(self):
        if self.is_empty():
            return None
        return self.items.pop()  # останній доданий

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def order(self):
        return list(reversed(self.items))  # від вершини до основи


# клас Черга (FIFO)
class Queue(Structure):
    def remove(self):
        if self.is_empty():
            return None
        return self.items.pop(0)  # перший доданий

    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]

    def order(self):
        return list(self.items)  # від початку до кінця


# Одна спільна функція вилучення працює і зі стеком, і з чергою, правило бере з самого обєкта 
def polymorph_remove(structure):
    return structure.remove()


class all_system:
    def __init__(self):
        # система містить власні стек і чергу (незалежні між собою)
        self.s = Stack()  # без обмеження
        self.q = Queue(4)  # місткість 4 пакети
        self.log_sent = []  # відправлені записи
        self.counter_packets_sent = 0
        self.counter_empty_s = 0
        self.counter_empty_q = 0
        self.counter_rejected = 0
        self.command_id_counter = 0  # порядковий номер ADD

    def process_command(self, command_line):
        parts = command_line.split()
        if not parts:
            return
        cmd = parts[0]

        if cmd == "ADD":
            self.command_id_counter += 1
            if parts[1] == "A":
                new_item = ItemA("A", int(parts[2]), self.command_id_counter)
            else:
                new_item = ItemB("B", int(parts[2]), self.command_id_counter)
            self.s.add(new_item)

        elif cmd == "PACK":
            k = int(parts[1])
            if k == 0:
                return  # нічого не змінюється
            # спочатку перевірка порожнього джерела, потім місткості приймача
            if self.s.is_empty():
                self.counter_empty_s += 1
            elif self.q.is_full():
                self.counter_rejected += 1  # записи зі стека не вилучаємо
            else:
                count = min(k, self.s.size())
                taken = [polymorph_remove(self.s) for _ in range(count)]
                self.q.add(Packet(taken))

        elif cmd == "SEND":
            k = int(parts[1])
            for _ in range(k):
                packet = polymorph_remove(self.q)
                if packet is None:
                    self.counter_empty_q += 1
                else:
                    for item in packet.items:
                        self.log_sent.append(item.id)
                    self.counter_packets_sent += 1

    def print_results(self):
        sent_str = " ".join(map(str, self.log_sent)) if self.log_sent else "-"

        print(f"S: {self.s.get_state()}")
        print(f"Q: {self.q.get_state(' | ')}")
        print(f"Сума S: {self.s.get_sum()}")
        print(f"Сума Q: {self.q.get_sum()}")
        print(f"Відправлено: {sent_str}")
        print(f"Пакетів відправлено: {self.counter_packets_sent}")
        print(f"Порожньо S: {self.counter_empty_s}")
        print(f"Порожньо Q: {self.counter_empty_q}")
        print(f"Відхилено пакетів: {self.counter_rejected}")


def main():
    n = int(input())  # кількість команд без запрошень і зайвого тексту
    system = all_system()
    for _ in range(n):
        system.process_command(input().strip())
    system.print_results()  # друкуємо тільки підсумок


if __name__ == "__main__":
    main()