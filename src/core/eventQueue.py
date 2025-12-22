"""Event queue responsible for scheduling evaluation events."""
 


class EventQueue:
    def __init__(self):
        self.events = []


    def put(self, event) -> None:
        self.events.append(event)


    def pop(self, event):
        return self.events.pop(0)
