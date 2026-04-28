

class Feedback:
    def __int__(self, sub, group):
        self.subject = sub
        self.group = group

    def feedback(self):
        if self.group == "NotFb":
            pass
        elif self.group == "FullFb":
            pass
        else:
