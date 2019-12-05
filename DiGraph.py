class Vertex:
	def __init__(self, key):
		self.id = key
		self.connectedTo = {}

	def addNeighbor(self, nbr, weight):
		self.connectedTo[nbr] = weight

	def __str__(self):
		return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

	def getConnections(self):
		return self.connectedTo.keys()

	def getId(self):
		return self.id

	def getWeight(self, nbr):
		return self.connectedTo[nbr]


class DiGraph:
	def __init__(self):
		self.vertList = {}
		self.numVertices = 0

	def addVertex(self, key):
		newv = Vertex(key)
		self.vertList[key] = newv
		self.numVertices += 1

	def getVertex(self, key):
		if key in self.vertList:
			return self.vertList[key]
		else:
			return None

	def __contains__(self, key):
		return key in self.vertList

	def addEdge(self, head, rear, weight=None):
		if head not in self.vertList:
			self.addVertex(head)
		if rear not in self.vertList:
			self.addVertex(rear)
		self.vertList[head].addNeighbor(rear, weight)

	def getVertices(self):
		return self.vertList.keys()

	def outEdges(self, head):
		return self.vertList[head].connectedTo.keys()