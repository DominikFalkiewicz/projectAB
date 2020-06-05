from flask import render_template, redirect, request, session


class Menu:
    def __init__(self, baza, path):
        self.baza = baza
        self.path = path

    def render(self):
        if request.method == "POST":
            form_button = request.form["button"]
            if form_button[0] == "l":
                session["acc"] = ""
                return redirect("/")

        return render_template(self.path)
