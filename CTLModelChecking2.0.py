class QueueUnderFlow(ValueError):
	pass


class SQueue():
	def __init__(self, init_len=8):
		self._elems = [0] * init_len
		# 引用着队列元素的储存区
		self._len = init_len
		# 队列的储存区的有效容量
		self._head = 0
		# 队头元素的下标
		# 这里不需要rear这个变量
		self._elnum = 0

	# 队列内部的元素个数

	def is_empty(self):
		# 判空操作
		return self._elnum == 0

	def first(self):
		if self._elnum == 0:
			# 首先进行判空操作
			raise QueueUnderFlow
		return self._elems[self._head]

	# 然后取得头部指标下的元素

	def dequeue(self):
		if self.is_empty():
			raise QueueUnderFlow
		tmp = self._elems[self._head]
		self._head = (self._head + 1) % self._len
		self._elnum -= 1
		# 分成三步：取得队头的元素作为暂时获得的值，
		# 修改队头元素下标，
		# 修改元素个数
		return tmp

	def enqueue(self, elem):
		if self._elnum == self._len:
			self.__extend()
		# 如果满了，自动扩充，把扩充的部分作为单独的一个函数
		self._elems[(self._head + self._elnum) % self._len] = elem
		self._elnum += 1

	def __extend(self):
		old_len = self._len
		self._len *= 2
		elems = [0] * self._len
		# 创建一张容量为原来两倍的表格
		for x in range(old_len):
			elems[x] = self._elems[(self._head + x) % self._len]
		# 在这张表里从头填写元素
		self._elems = elems
		self._head = 0
	# 修改对头元素下标和队列元素储存区的值，保持数据不变式不变

class DiGraphError(ValueError):
	pass

class Vertex:
	def __init__(self,name):
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

	def subGraph1(self, chosenvertexs):
		#chosenvertexs是原图中部分顶点的列表
		SGvertexs = self.getVertexs().copy()
		SGedges = []
		for edge in self.edges:
			if edge[0] in chosenvertexs:
				SGedges.append(edge)
		return DiGraph(SGvertexs,SGedges)
#返回的是顶点和原图相同，所有边起点在chosenvertexs中的子图

	def subGraph2(self, chosenvertexs):
		#chosenvertexs是部分顶点的列表
		SGvertexs = chosenvertexs
		SGedges = []
		for edge in self.edges:
			if edge[0] in SGvertexs and edge[1] in SGvertexs:
				SGedges.append(edge)
		return DiGraph(SGvertexs, SGedges)
#返回的图是顶点集为所选列表，边集为两端都在顶点集中的边





class CTLFormulaError(ValueError):
	pass

class CTLFormula:
	def __init__(self,subformulas):
		self.subformulas = [x.simplified() for x in subformulas]

	def getSubformulas(self):
		# 获得全部的子公式，返回一个表格
		return self.subformulas

	def subformula(self,i):
		# 获得某一个子公式，返回一个Formula 类的实例对象
		if not self.subformulas:
			raise FormulaError('This formula doesnot have subformula.')
		if not (0<= i < len(self.subformulas)):
			raise FormulaError('Index Error.')
		return self.subformulas[i]

	def setSubformula(self,i,newsubformula):
		# 修改一个子公式
		self.subformulas[i] = newsubformula

	def formulaHash(self):
		return hash(str(self))

	def __eq__(self,other):
		return str(self.simplified()) == str(other.simplified())

	def __hash__(self):
		# 为了让formula的实例对象成为一个hashable的对象，才能加入集合中
		return hash(str(self))

class CTLState(CTLFormula):
	def __init__(self,name):
		self.state = name # name的类型不固定（？）
		self.subformulas= []
		self.depth = 1

	def simplified(self):
		return CTLState(self.state)

	def __repr__(self):
		return str(self.state)

class CTLBools(CTLFormula):
	def __init__(self,value):
		self.value = value # value的类型是bool
		self.subformulas = []
		self.depth = 1

	def simplified(self):
		return CTLBools(self.value)

	def __repr__(self):
		return str(self.value)

class CTLAnd(CTLFormula):
	def __init__(self,subformula1,subformula2):
		self.subformulas = [subformula1.simplified(),
						   subformula2.simplified()]
		self.depth = max(subformula1.simplified().depth,
						subformula2.simplified().depth) + 1

	def simplified(self):
		return CTLAnd(self.subformulas[0],
					 self.subformulas[1])

	def __repr__(self):
		return "(%s and %s)" % (self.subformulas[0],
								self.subformulas[1])

class CTLOr(CTLFormula):
	def __init__(self,subformula1,subformula2):
		self.subformulas = [subformula1.simplified(),
						   subformula2.simplified()]
		self.depth = max(subformula1.simplified().depth,
						subformula2.simplified().depth) + 1

	def simplified(self):
		return CTLOr(self.subformulas[0],
					 self.subformulas[1])

	def __repr__(self):
		return "(%s or %s)" % (self.subformulas[0],
								self.subformulas[1])

class CTLNot(CTLFormula):
	def __init__(self,subformula1):
		self.subformulas = [subformula1.simplified()]
		self.depth = subformula1.simplified().depth

	def simplified(self):
		if isinstance(self.subformulas[0],CTLNot):
			if isinstance(self.subformulas[0].subformulas[0],CTLNot):
				return self.subformulas[0].subformulas[0].simplified()
			return self.subformulas[0].subformulas[0]
		else:
			return CTLNot(self.subformulas[0])

	def __repr__(self):
		return "(not %s)" % (self.subformulas[0])

class CTLImply(CTLFormula):
	def __init__(self,subformula1,subformula2):
		self.subformulas = [subformula1.simplified(),
							subformula2.simplified()]
		self.depth = max(subformula1.simplified().depth,
						subformula2.simplified().depth) + 1

	def simplified(self):
		return CTLOr(CTLNot(self.subformulas[0]),
					self.subformulas[1])

	def __repr__(self):
		return "(%s --> %s)" % (self.subformulas[0],
								self.subformulas[1])

class CTLEX(CTLFormula):
	def __init__(self,subformula1):
		self.subformulas = [subformula1.simplified()]
		self.depth = subformula1.simplified().depth + 1

	def simplified(self):
		return CTLEX(self.subformulas[0])

	def __repr__(self):
		return "(EX %s)" % (self.subformulas[0])

class CTLEU(CTLFormula):
	def __init__(self,subformula1,subformula2):
		self.subformulas = [subformula1.simplified(),
						   subformula2.simplified()]
		self.depth = max(subformula1.simplified().depth,
						 subformula2.simplified().depth) + 1

	def simplified(self):
		return CTLEU(self.subformulas[0],
					 self.subformulas[1])

	def __repr__(self):
		return "(%s EU %s)" % (self.subformulas[0],
							  self.subformulas[1])

class CTLAF(CTLFormula):
	def __init__(self,subformula1):
		self.subformulas = [subformula1.simplified()]
		self.depth = subformula1.simplified().depth + 1

	def simplified(self):
		return CTLNot(CTLEG(CTLNot(self.subformulas[0])))

	def __repr__(self):
		return "(AF %s)" % (self.subformulas[0])

class CTLAX(CTLFormula):
	def __init__(self,subformula1):
		self.subformulas = [subformula1.simplified()]
		self.depth = subformula1.simplified().depth + 1

	def simplified(self):
		return CTLNot(CTLEX(CTLNot(self.subformulas[0])))

	def __repr__(self):
		return "(AX %s)" % (self.subformulas[0])

class CTLEF(CTLFormula):
	def __init__(self,subformula1):
		self.subformulas = [subformula1.simplified()]
		self.depth = subformula1.simplified().depth + 1

	def simplified(self):
		return CTLEU(CTLBools(True),self.subformulas[0])

	def __repr__(self):
		return "(EF %s)" % (self.subformulas[0])

class CTLEG(CTLFormula):
	def __init__(self,subformula1):
		self.subformulas = [subformula1.simplified()]
		self.depth = subformula1.simplified().depth + 1

	def simplified(self):
		return CTLEG(self.subformulas[0])

	def __repr__(self):
		return "(EG %s)" % (self.subformulas[0])

class CTLAG(CTLFormula):
	def __init__(self,subformula1):
		self.subformulas = [subformula1.simplified()]
		self.depth = subformula1.simplified().depth + 1

	def simplified(self):
		return CTLNot(CTLEU(CTLBools(True),CTLNot(self.subformulas[0])))

	def __repr__(self):
		return "(AG %s)" % (self.subformulas[0])

class CTLAU(CTLFormula):
	def __init__(self,subformula1,subformula2):
		self.subformulas = [subformula1.simplified(),
						   subformula2.simplified()]
		self.depth = max(subformula1.depth,
						 subformula2.depth) + 1

	def simplified(self):
		return CTLNot(CTLOr(CTLEU(CTLNot(self.subformulas[1]),
								 (CTLAnd(CTLNot(self.subformulas[0]),
										CTLNot(self.subformulas[1])))),
					  CTLEG(CTLNot(self.subformulas[1]))))

	def __repr__(self):
		return "(%s AU %s)" % (self.subformulas[0],
							  self.subformulas[1])

def SAT(TS,formula):
	# 返回的一定是一个集合
	formula = formula.simplified()
	if formula == CTLBools(True):return set(TS.getVertexs())
	elif formula == CTLBools(False):return set()
	elif isinstance(formula,CTLState):
		return {TS.getAVertex(formula.state)}
	elif isinstance(formula,CTLNot):
		return set(TS.getVertexs()) - SAT(TS,formula.subformulas[0])
	elif isinstance(formula,CTLAnd):
		return SAT(TS,formula.subformulas[0]) & SAT(TS,formula.subformulas[1])
	elif isinstance(formula,CTLOr):
		return SAT(TS,formula.subformulas[0]) | SAT(TS,formula.subformulas[1])
	elif isinstance(formula,CTLImply):
		return SAT(TS,
				  CTLOr(CTLNot(formula.subformulas[0]).simplified(),
					   formula.subformulas[1]))
	elif isinstance(formula,CTLEX):
		return SATEX(TS,formula.subformulas[0])
	elif isinstance(formula,CTLEG):
		return SATEG(TS,formula.subformulas[0])
	elif isinstance(formula,CTLEU):
		return SATEU(TS,formula.subformulas[0],
					 formula.subformulas[1])
	else:
		return SAT(TS,formula.simplified())

def SATEX(TS,formula):
	return TS.preExist(SAT(TS,formula))

def SATEG(TS,formula):
	Y = list(SAT(TS, formula))
	subTS = TS.subGraph2(Y)
	sccs = subTS.stronglyConnectedComponents()
	resset = set()
	rsTS = subTS.reversedGraph()#子图的逆图
	for scc in sccs:
		if subTS.isTrival(scc):
			continue
		else:
			squeue = SQueue()
			for vertex in scc:
				resset.add(vertex)
				for prev in rsTS.getOutEdge(vertex):
					if prev not in scc:
						squeue.enqueue(prev)
			while len(resset) < subTS.vnum and not squeue.is_empty():
				v = squeue.dequeue()
				if v in resset:
					continue
				else:
					resset.add(v)
					for priov in rsTS.getOutEdge(v):
						if priov not in resset:
							squeue.enqueue(priov)
	return resset

def SATEU(TS,formula1,formula2):
	W = SAT(TS,formula1)
	Y = SAT(TS,formula2)
	rTS = TS.reversedGraph()
	visited = []
	squeue = SQueue()
	resset = set()
	for v in Y:
		squeue.enqueue(v)
	while len(visited) < TS.vnum and not squeue.is_empty():
		vertex = squeue.dequeue()
		if vertex in visited:
			continue
		elif vertex in W or vertex in Y:
			visited.append(vertex)
			resset.add(vertex)
			for prev in rTS.getOutEdge(vertex):
				squeue.enqueue(prev)
		else:
			visited.append(vertex)


		Y = Y | (W & TS.preExist(Y))
	return Y

def CTLModelchecking(TS, formula, init):
	if not isinstance(TS, DiGraph):
		raise DiGraphError(TS, 'is not a digraph,please input again!')
	if not isinstance(init, Vertex):
		raise DiGraphError(init, 'is not a vertex,please input again!')
	if not isinstance(formula, CTLFormula):
		raise CTLFormulaError(formula, 'is not a CTLFormula,please input again!')
	sat = SAT(TS, formula)
	if init in sat:
		if isinstance(formula, CTLEX):
			print(True, witnessEX(TS, formula.subformulas[0], init))
		elif isinstance(formula, CTLEU):
			print(True, witnessEG(TS, formula.subformulas[0], init))

def witnessEX(TS, formula, init):
	X = SAT(TS, formula)
	Y = TS.getOutEdge(init)
	for v in Y:
		if v in X:
			return [init, v]

def witnessEG(TS, formula, init):
	X = list(SAT(TS, formula))
	subTS = TS.subGraph2(X)
	stack = [init]
	visited = [init]
	pt = init
	while stack:
		go_out = True
		for outv in subTS.getOutEdge(pt):
			if outv not in visited:
				visited.append(outv)
				stack.append(outv)
				pt = outv
				go_out = False
				break
			elif outv in stack:
				i = 0
				res = []
				circle = []
				while stack[i] != outv:
					res.append(stack[i])
					i += 1
				while i < len(stack):
					circle.append(stack[i])
				res.append(tuple(circle))
				return res
		if go_out:
			stack.pop()
			if stack:
				pt = stack[-1]
			else:
				return False#检查时应该不会出现这种情况

def witnessEU(TS, formula1, formula2, init):
	X = list(SAT(TS,formula1))
	Y = list(SAT(TS,formula2))
	if init in Y:
		return [init]
	subTS = TS.subGraph1(formula1)
	stack = []
	visited = []
	pt = init
	while stack:
		go_out = True
		for outv in subTS.getOutEdge(pt):
			if outv in visited:
				continue
			elif outv not in Y and outv in X:
				visited.append(outv)
				stack.append(outv)
				pt = outv
				go_out = False
				break
			elif outv in Y:
				stack.append(outv)
				return stack
		if go_out:
			stack.pop()
			if stack:
				pt = stack[-1]
			else:
				return False#检查时应该不会出现这种情况

def counterexAX(TS, formula, init):
	return witnessEX(TS, CTLNot(formula), init)

def counterexAG(TS, formula, init):
	return witnessEU(TS, CTLBools(True), CTLNot(formula), init)

def counterexAU(TS, formula1, formula2, init):
	res1 = witnessEG(TS, CTLAnd(formula1,CTLNot(formula2)), init):
	if res1:
		return res1
	else:
		res2 = witnessEU(TS, CTLAnd(formula1,CTLNot(formula2)),
						 CTLAnd(CTLNot(formula1),CTLNot(formula2)), init)
		return res2






#以下是第一部分测试样例，测试模型检测部分
a = Vertex('a')
b = Vertex('b')
c = Vertex('c')
d = Vertex('d')
ts = DiGraph(vertexs = [a,b,c,d],
			edges = [(a,b),(b,c),(c,d),(d,a),
				   (b,a),(c,b)])
print(a,b,c,d)
print(ts)
for1 = CTLState('a')
print(SAT(ts,for1))
for2 = CTLNot(for1)
print(SAT(ts,for2))
for3 = CTLNot(CTLNot(for1))
print(SAT(ts,for3))
for4 = CTLAnd(for1,CTLState('b'))
print(SAT(ts,for4))
for5 = CTLOr(for1,CTLState('b'))
print(SAT(ts,for5))
for6 = CTLOr(CTLNot(for1),CTLNot(CTLState('b')))
print(SAT(ts,for6))
for7 = CTLImply(CTLState('c'),CTLState('d'))
print(SAT(ts,for7))
for8 = CTLEX(for1)
print(SAT(ts,for8))
for9 = CTLAX(for1)
print(SAT(ts,for9))
for10 = CTLEF(for1)
print(SAT(ts,for10))
for11 = CTLAX(CTLEX(for1))
print(SAT(ts,for11))
for12 = CTLEG(for11)
print(SAT(ts,for12))
for13 = CTLEG(for1)
print(SAT(ts,for13))
for14 = CTLAG(for10)
print(SAT(ts,for14))
for15 = CTLEG(for14)
print(SAT(ts,for15))
for16 = CTLEU(for1,CTLState('b'))
print(SAT(ts,for16))
for17 = CTLAU(for1,CTLNot(CTLState('b')))
print(SAT(ts,for17))
for18 = CTLAF(for2)
print(SAT(ts,for18))
for19 = CTLNot(CTLEU(CTLAF(for11),CTLEG(for14)))
print(SAT(ts,for19))
for20 = CTLEU(CTLAF(for11),CTLEG(for14))
print(SAT(ts,for20))

# 以下是第二部分检验案例，检验公式类的建立。
a = CTLState('lala')
b = CTLState('haha')
print(a == b)
print(a.depth)
print(b.depth)
c = CTLBools(True)
d = CTLBools(True)
print(c)
print(c==d)
print(c.depth)
print(CTLAnd(a,b))
print(CTLAnd(a,c))
print(CTLAnd(a,c).depth)
print(CTLAnd(a,c).subformulas)
print(CTLOr(b,d))
print(CTLOr(b,d).depth)
print(CTLOr(b,c).subformulas)
e = CTLAnd(CTLOr(a,b),c)
f = CTLAnd(CTLOr(a,b),c)
print(e,f)
print(e == f)
print(e.depth)
print(e.subformulas)
ff = set()
ff.add(f)
print(ff)
print(e in ff)

g = CTLNot(e)
print(g)
h = CTLNot(g)
print(h)
print(h.simplified())
i = CTLNot(h)
print(i)
print(g == i)

j = CTLImply(g,h)
print(j,j.depth)
print(j.simplified(),j.simplified().depth)
k = CTLImply(e,a)
print(k,k.depth)
print(k.simplified(),k.simplified().depth)

l = CTLEX(e)
print(l,l.depth)
print(l.subformulas)
m = CTLAF(f)
print(m,m.depth)
print(m.subformulas)
n = CTLEU(CTLNot(e),f)
print(n,n.depth)
print(n.subformulas)

o = CTLAX(a)
print(o,o.depth)
print(o.simplified(),o.simplified().depth)

p = CTLEX(o)
print(p,p.depth)
print(p.simplified())

q = CTLEF(a)
print(q,q.depth)
print(q.simplified(),q.simplified().depth)
r = CTLEF(m)
print(r.simplified(),r.simplified().depth)

s = CTLEG(CTLNot(CTLNot((a))))
print(s,s.depth)
s = s.simplified()
print(s,s.depth)

t = CTLAU(a,b)
print(t)
print(t.simplified())
t = CTLNot(CTLNot(CTLAU(a,b)))
print(t,t.depth)
t = t.simplified()
print(t,t.depth)
