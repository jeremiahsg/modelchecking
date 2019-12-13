class DiGraphError(ValueError):
    pass


class Vertex:
	def __init__(self, name):
		# name是一个字符串
		self.state = name

	def __repr__(self):
		return self.state

	def __hash__(self):
		return hash(str(self.state))


class DiGraph:
	def __init__(self, vertexs=[], edges=[]):
		self.vertexs = vertexs
		self.vnum = len(vertexs)
		self.edges = edges
		self.outEdges = {}
		# 出边表示成为一个字典，字典的关键码为顶点，值为出边的到达顶点的集合
		self.verdict = {vertex.state: vertex for vertex in self.vertexs}
		for edge in edges:
			if edge[0] not in vertexs or edge[1] not in vertexs:
				raise DiGraphError('egdes must be in the form of pairs of vertexs.')
			if edge[0] not in self.outEdges:
				self.outEdges[edge[0]] = set([edge[1]])
			# 这里用集合还是用表有待商榷
			else:
				self.outEdges[edge[0]].add(edge[1])

	def addVertex(self, newVertex):
		if newVertex in self.vertexs:
			raise DiGraphError('vertex is in the vertxs list!')
		self.vnum += 1
		self.vertexs.append(newVertex)
		self.verdict[newVertex.state] = newVertex

	def getVertexs(self):
		return self.vertexs

	def getAVertex(self, name):
		return self.verdict[name]

	def addEdge(self, edge):
		if type(edge) != tuple or len(edge) != 2:
			raise DiGraphError('input a wrong edge.')
		if edge[0] not in self.outEdges:
			self.outEdges[edge[0]] = set([edge[1]])
			self.edges.append((edge))
		elif edge[1] in self.outEdges[edge[0]]:
			raise DiGraphError('edge is already in the graph.')
		else:
			self.outEdges[edge[0]].add(edge[1])
			self.edges.append((edge))

	def getOutEdge(self, vertex):
		if vertex not in self.outEdges:
			raise DiGraphError('vertex not in the graph,input again.')
		return self.outEdges[vertex]

	def getEdges(self):
		return self.edges

	def __repr__(self):
		return '%s %s' % (self.getVertexs(), self.getEdges())

	def preExist(self, vertexset):
		# 输入的参数是一个顶点的集合
		if not vertexset: return set()
		ansset = set()
		for i, j in self.getEdges():
			if j in vertexset:
				ansset.add(i)
		return ansset

	def preAny(self, vertexset):
		# 输入的参数是一个顶点的集合
		if not vertexset: return set()
		ansset = set()
		for i, j in self.outEdges.items():
			if j.issubset(vertexset):
				ansset.add(i)
		return ansset

	def stronglyConnectedComponents(self):
		# 求图中的强连通分量
		mark = {ver: 0 for ver in self.getVertexs()}
		findingTime = {}
		time = 0
		low = {}
		outedges = {v: list(self.outEdges[v])
		if v in self.outEdges else []
					for v in self.getVertexs()}
		sccs = []
		alreadyInScc = set()
		sccstack = []
		for v in self.getVertexs():  # 这个循环基本只是一个摆设
			if mark[v] == 1:
				continue
			mark[v] = 1
			findingTime[v] = time
			low[v] = time
			stack = []
			stack.append((v, 0))
			while stack:
				ver, nextpos = stack.pop()
				if nextpos < len(outedges[ver]):
					newver = outedges[ver][nextpos]
					if mark[newver] == 1:
						stack.append((ver, nextpos + 1))
						continue
					time += 1
					mark[newver] = 1
					findingTime[newver] = time
					low[newver] = time
					stack.append((ver, nextpos + 1))
					stack.append((newver, 0))
				else:
					ver1 = ver
					for nextver in outedges[ver1]:
						if nextver not in alreadyInScc:
							low[ver1] = min(low[ver1], low[nextver])
					if not low[ver1] == findingTime[ver1]:
						sccstack.append(ver1)
						continue
					else:
						newscc = set()
						newscc.add(ver1)
						alreadyInScc.add(ver1)
						while sccstack:
							newscc.add(sccstack[-1])
							alreadyInScc.add(sccstack[-1])
							sccstack.pop()
						sccs.append(newscc)
		return sccs

	def isTrival(self, scc):
		if len(scc) > 1:
			return False
		else:
			v = list(scc)[0]
			if (v not in self.outEdges or
					v not in self.outEdges[v]):
				return True
		return False

	def reversedReach(self, vertexs):
		# vertexs 是一个顶点集合
		reversedEdges = {}
		for edge in self.getEdges():
			if edge[1] not in reversedEdges:
				reversedEdges[edge[1]] = [edge[0]]
			else:
				reversedEdges[edge[1]].append(edge[0])
		reachable = vertexs.copy()
		squeue = SQueue()
		for v in vertexs:
			if v in reversedEdges:
				for w in reversedEdges[v]:
					if w not in reachable:
						reachable.add(w)
						squeue.enqueue(w)
		while not squeue.is_empty():
			v = squeue.dequeue()
			if v in reversedEdges:
				for w in reversedEdges[v]:
					if w not in reachable:
						reachable.add(w)
						squeue.enqueue(w)
		return reachable
# 返回的是可以逆向到达的集合

	def reversedGraph(self):
		RGvertexs = self.getVertexs().copy()
		RGedges = list(map(lambda x:(x[1],x[0]),self.getEdges().copy()))
		return DiGraph(RGvertexs,RGedges)
#返回的是原图边反向得到的新图

	def subGraph(self, chosenvertexs):
		#chosenvertexs是原图中部分顶点的集合或列表
		SGvertexs = self.getVertexs().copy()
		SGedges = []
		for edge in self.edges:
			if edge[0] in chosenvertexs:
				SGedges.append(edge)
		return DiGraph(SGvertexs,SGedges)
#返回的是顶点和原图相同，所有边起点在chosenvertexs中的子图
