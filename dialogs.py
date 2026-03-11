dialogs = {
    "jon": "hej",
    "bob": "tjo",
    "jim": "Def"
}

class Dialog:
    def __init__(self, id):
        self.id = id
        if id in dialogs:
            self.text = dialogs[id]
        else:
            self.text = "don't talk to me"
