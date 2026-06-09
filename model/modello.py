import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._points = None
        self._bestSolution = None
        self._grafo=nx.DiGraph() #orientato e pesato
        self._map={}

    def getAnni(self):
        return DAO.get_anni()

    def getShape(self, anno):
        return DAO.get_shape(anno)

    def buildGraph(self, anno, shape):
        self._grafo.clear()
        self._map={}

        nodi=DAO.get_sightings(anno, shape)
        self._grafo.add_nodes_from(nodi)

        for nodo in nodi:
            self._map[nodo.id]=nodo

        #aggiungo gli archi
        tuple_archi=DAO.get_archi(anno, shape)
        for tupla in tuple_archi:
            #per come è costruita la query dovrebbero essere sicuro nella id Map
            nodo1=self._map[tupla[0]]
            nodo2=self._map[tupla[1]]

            if nodo1.longitude<nodo2.longitude:
                peso=nodo2.longitude-nodo1.longitude
                self._grafo.add_edge(nodo1, nodo2, weight=peso)
            elif nodo1.longitude>nodo2.longitude:
                peso = nodo1.longitude - nodo2.longitude
                self._grafo.add_edge(nodo2, nodo1, weight=peso)
        return

    def num_nodi(self):
        return len(self._grafo.nodes)

    def num_archi(self):
        return len(self._grafo.edges)

    def archi_maggiori(self):
        archi=list(self._grafo.edges(data=True)) #((id1, id2), {weight: peso})
        archi.sort(key=lambda x:x[2]["weight"], reverse=True)
        return archi[:5]

    def get_cammino(self):
        self._bestSolution=[]
        self._points=0
        #devo trovare il primo nodo più conveniente
        for nodo in self._grafo.nodes:
            parziale=[nodo]
            self._ricorsione(parziale)
        return self._bestSolution, self._points

    def _ricorsione(self, parziale):
        #condizione terminale
        #best soluzione
        if self.getPoints(parziale)>self._points:
            self._points=self.getPoints(parziale)
            self._bestSolution=copy.deepcopy(parziale)

        for n in nx.neighbors(self._grafo,parziale[-1]):
            if self._isAdmissible(parziale, n):
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()


    def getPoints(self, parziale):
        score=0
        if len(parziale)==1:
            return 100

        for nodo in parziale:
            if nodo.datetime.month==parziale[-1].datetime.month:
                score += 200
            else:
                score += 100
        return score


    def _isAdmissible(self, parziale, nodo):
        if nodo.duration<=parziale[-1].duration:
            return False
        mese=nodo.datetime.month
        count=0
        for n in parziale:
            if n.datetime.month==mese:
                count+=1
                
        if count>=3:
            return False
        return True

