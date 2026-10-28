#Варіант 48. Заявки на оцифрування
#Завдання 2. Опрацювання з поверненням із архіву


class Item:  # батько для записів
    def __init__(self, item_type, value, item_id):  # item_type - A або B, value - значення x, item_id - номер команди ADD
        self.type = item_type
        self.value = value
        self.id = item_id

    def get_score(self):
        raise NotImplementedError  # якщо викличемо через батьківський клас

    def get_label(self):
        return str(self.id)


# Два типи A і B з різною оцінкою по завданню
class ItemA(Item):  # наслідування
    def get_score(self):
        return 3 * self.value


class ItemB(Item):  # наслідування
    def get_score(self):
        return 2 * self.value + 6


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
        return len(self.items)

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
        return sum(item.get_score() for item in self.items)

    def get_state(self):
        if self.is_empty():
            return "-"
        return " ".join(item.get_label() for item in self.order())


# клас Стек (LIFO)
class Stack(Structure):
    def remove(self):
        if self.is_empty():
            return None
        return self.items.pop()

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
        return self.items.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]

    def order(self):
        return list(self.items)  # від початку до кінця


# Одна спільна функція вилучення для стека і черги
def polymorph_remove(structure):
    return structure.remove()


class all_system:
    def __init__(self):
        # композиція: система містить власні стек і чергу
        self.s = Stack()  # без обмеження
        self.q = Queue(5)  # місткість 5 записів
        self.log_processed = []
        self.log_returned = []
        self.counter_empty_q = 0
        self.counter_empty_s = 0
        self.counter_blocked = 0
        self.counter_rejected = 0
        self.command_id_counter = 0  # порядковий номер ADD відхилений теж займає номер

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
            if not self.q.add(new_item):
                self.counter_rejected += 1  # черга заповнена

        elif cmd == "RUN":
            k = int(parts[1])
            for _ in range(k):
                item = polymorph_remove(self.q)  # голова Q
                if item is None:
                    self.counter_empty_q += 1
                else:
                    self.s.add(item)  # на вершину S
                    self.log_processed.append(item.id)

        elif cmd == "UNDO":
            k = int(parts[1])
            for _ in range(k):
                # порожнє джерело перевіряємо раніше за місткість приймача
                if self.s.is_empty():
                    self.counter_empty_s += 1
                elif self.q.is_full():
                    self.counter_blocked += 1  # стан не міняється, тому тільки peek
                else:
                    item = polymorph_remove(self.s)  # вершина S
                    self.q.add(item)  # в кінець Q
                    self.log_returned.append(item.id)

    def print_results(self):
        processed_str = " ".join(map(str, self.log_processed)) if self.log_processed else "-"
        returned_str = " ".join(map(str, self.log_returned)) if self.log_returned else "-"

        print(f"S: {self.s.get_state()}")
        print(f"Q: {self.q.get_state()}")
        print(f"Сума S: {self.s.get_sum()}")
        print(f"Сума Q: {self.q.get_sum()}")
        print(f"Опрацьовано: {processed_str}")
        print(f"Повернено: {returned_str}")
        print(f"Порожньо Q: {self.counter_empty_q}")
        print(f"Порожньо S: {self.counter_empty_s}")
        print(f"Заблоковано: {self.counter_blocked}")
        print(f"Відхилено: {self.counter_rejected}")


def main():
    n = int(input())  # кількість команд, без запрошень і зайвого тексту
    system = all_system()
    for _ in range(n):
        system.process_command(input().strip())
    system.print_results()


if __name__ == "__main__":
    main()