import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._shape = None
        self._anno = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        if self._anno == "":
            self._view.create_alert("SELEZIONA UN ANNO PER PROSEGUIRE!")
            return
        if self._shape == "":
            self._view.create_alert("SELEZIONA UNA FORMA PER PROSEGUIRE!")
            return
        self._model.buildGraph(self._anno, self._shape)
        self._view.txt_result1.controls.append(ft.Text(f"Grafo creato correttamente, ha {self._model.num_nodi()} nodi e {self._model.num_archi()} archi. "))
        archi=self._model.archi_maggiori()
        for arco in archi:
            self._view.txt_result1.controls.append(ft.Text(f"Arco: {arco[0].id} --> {arco[1].id}, peso: {arco[2]["weight"]}"))
        self._view.update_page()

    def handle_path(self, e):
        solution=self._model.get_cammino()
        points=solution[1]
        for nodo in solution[0]:
            self._view.txt_result2.controls.append(ft.Text(f"--> {nodo.id}"))
        self._view.txt_result2.controls.append(ft.Text(f"La soluzione ottima vale {points} punti"))
        self._view.update_page()
        return

    def fillDDYear(self):
        aeroporti = self._model.getAnni()
        for n in aeroporti:
            self._view.ddyear.options.append(
                ft.dropdown.Option(key=n, data=n, on_click=self.getYear)
            )
        self._view.update_page()
        return

    def getYear(self, e):
        selected_key = e.control.data
        self._anno = int(selected_key)
        self.fillDDShape()
        return

    def fillDDShape(self):
        aeroporti = self._model.getShape(self._anno)
        for n in aeroporti:
            self._view.ddshape.options.append(
                ft.dropdown.Option(key=n, data=n, on_click=self.getShape)
            )
        self._view.update_page()

    def getShape(self, e):
        selected_key = e.control.data
        self._shape = selected_key
        return