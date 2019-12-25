import os

from python.intcode import Intcode, InputNeededException


class Arcade:
    def __init__(self, data, part=1):
        self.part = part

        self.n = 50
        self.vms = []
        self.nat_x = self.nat_y = None
        self.active = [True] * self.n

        for i in range(self.n):
            current_vm = Intcode(data)
            current_vm.add_input(i)
            self.vms.append(current_vm)

    def ping(self):
        if self.nat_y is not None:
            queue_empty = True
            for vm in self.vms:
                if vm.input and vm.input != [-1]:
                    queue_empty = False
            if queue_empty:
                self.vms[0].add_input(self.nat_x)
                self.vms[0].add_input(self.nat_y)
                # For some reason ping goes twice...
                # So for part 2 you need not the value that pops up twice, but more than twice...
                print(f'NAT pinging, Y = {self.nat_y}')

    def handle_outputs(self, index):
        vm = self.vms[index]
        if vm.unread_outputs and len(vm.unread_outputs) % 3 == 0:
            send_smth = False
            while vm.unread_outputs:
                send_smth = True
                address = vm.unread_outputs.pop(0)
                x = vm.unread_outputs.pop(0)
                y = vm.unread_outputs.pop(0)
                if address == 255:
                    if self.nat_x is None:
                        print(f'Part 1, package to NAT: {x}, {y}')
                    self.nat_x = x
                    self.nat_y = y
                else:
                    self.vms[address].add_input(x)
                    self.vms[address].add_input(y)

            self.active[index] = send_smth

    def play(self):
        while True:
            self.ping()
            for i, vm in enumerate(self.vms):
                try:
                    vm.tick()
                    self.handle_outputs(i)
                except InputNeededException:
                    self.handle_outputs(i)

                    vm.add_input(-1)
                    continue

                except InterruptedError:
                    print('\nGAME OVER!')
                    break


if __name__ == '__main__':
    with open(os.path.join('..', 'day_23_input.txt'), 'r') as f:
        data = list(map(int, f.read().split(',')))

    automat = Arcade(data, part=1)
    automat.play()

    # First part answer: 23815
    # Second part answer: 16666
