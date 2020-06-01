from flask import render_template, request

class Kolekcje:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            delete_form = request.form["delete_button"]
            if delete_form[0] == "d":
                self.delete(delete_form[1:])
        rekordy = self.baza.ask("SELECT * FROM kolekcja")
        return render_template(self.path, rekordy=rekordy)

    def delete(self, id):
        self.baza.exe("DELETE FROM kolekcja WHERE id = " + id)
