class Stack(list):

    def push(self, item): self.append(item)



class Frame: pass



s = Stack()
s.push(Frame())
s.push(Frame())
print(s)
print(s.pop())
