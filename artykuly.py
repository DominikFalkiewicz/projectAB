from flask import render_template

class Artykuly:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        return render_template(self.path)