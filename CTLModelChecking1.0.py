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
    def __init__(self,vertexs = [],edges = []):
        self.vertexs = vertexs
        self.vnum = len(vertexs)
        self.edges = edges
        self.outEdges = {}
        self.verdict = {vertex.state:vertex for vertex in self.vertexs}
        # 出边表示成为一个字典，字典的关键码为顶点，值为出边的到达顶点的集合
        for edge in edges:
            if edge[0] not in vertexs or edge[1] not in vertexs:
                raise DiGraphError('egdes must be in the form of pairs of vertexs.')
            if edge[0] not in self.outEdges:
                self.outEdges[edge[0]] = set([edge[1]])
                # 这里用集合还是用表有待商榷
            else:
                self.outEdges[edge[0]].add(edge[1])
    
    def addVertex(self,newVertex):
        if newVertex in self.vertexs:
            raise DiGraphError('vertex is in the vertxs list!')
        self.vnum += 1
        self.vertex.append(newVertex)
        self.verdict[newVertex.state] = newVertex
        
    def getVertexs(self):
        return self.vertexs
    
    def getAVertex(self,name):
        return self.verdict[name]
    
    def addEdge(self,edge):
        if type(edge) != tuple or len(edge) != 2:
            raise DiGraphError('input a wrong edge.')
        if edge[0] not in self.outEdges:
            self.outEdges[edge[0]] = set([edge[1]])
        if edge[1] in self.outEdges[edge[0]]:
            raise DiGraphError('edge is already in the graph.')
        self.outEdges[edge[0]].add(edge[1])
        
    def getOutEdge(self,vertex):
        if vertex not in self.outEdges:
            raise DiGraphError('vertex not in the graph,input again.')
        return self.outEdges[vertex]
    
    def getEdges(self):
        edges = []
        for i in self.outEdges.keys():
            for j in self.outEdges[i]:
                edges.append((i,j))
        return edges
    
    def __str__(self):
        return '%s %s' % (self.getVertexs(),self.getEdges())
    
    def preExist(self,vertexset):
        # 输入的参数是一个顶点的集合
        if not vertexset:return set()
        ansset = set()
        for i,j in self.getEdges():
            if j in vertexset:
                ansset.add(i)
        return ansset
    
    def preAny(self,vertexset):
        # 输入的参数是一个顶点的集合
        if not vertexset:return set()
        ansset = set()
        for i,j in self.outEdges.items():
            if j.issubset(vertexset):
                ansset.add(i)
        return ansset
    
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
        
    def __str__(self):
        return str(self.state)
    
    def simplified(self):
        return CTLState(self.state)
    
    def __repr__(self):
        return str(self.state)
    
class CTLBools(CTLFormula):
    def __init__(self,value):
        self.value = value # value的类型是bool
        self.subformulas = []
        self.depth = 1
    
    def __str__(self):
        return str(self.value)
    
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
    
    def __str__(self):
        return "(%s and %s)" % (self.subformulas[0],
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
    
    def __str__(self):
        return "(%s or %s)" % (self.subformulas[0],
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
        
    def __str__(self):
        return "(not %s)" % (self.subformulas[0])
    
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
    
    def __str__(self):
        return "(%s --> %s)" % (self.subformulas[0],
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
    
    def __str__(self):
        return "(EX %s)" % (self.subformulas[0])
    
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
    
    def __str__(self):
        return "(%s EU %s)" % (self.subformulas[0],
                              self.subformulas[1])
    
    def __repr__(self):
        return "(%s EU %s)" % (self.subformulas[0],
                              self.subformulas[1])
    
class CTLAF(CTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = subformula1.simplified().depth + 1
        
    def simplified(self):
        return CTLAF(self.subformulas[0])
    
    def __str__(self):
        return "(AF %s)" % (self.subformulas[0])
    
    def __repr__(self):
        return "(AF %s)" % (self.subformulas[0])
    
class CTLAX(CTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = subformula1.simplified().depth + 1
        
    def simplified(self):
        return CTLNot(CTLEX(CTLNot(self.subformulas[0])))
    
    def __str__(self):
        return "(AX %s)" % (self.subformulas[0])
    
    def __repr__(self):
        return "(AX %s)" % (self.subformulas[0])
    
class CTLEF(CTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = subformula1.simplified().depth + 1
        
    def simplified(self):
        return CTLEU(CTLBools(True),self.subformulas[0])
    
    def __str__(self):
        return "(EF %s)" % (self.subformulas[0])
    
    def __repr__(self):
        return "(EF %s)" % (self.subformulas[0])
    
class CTLEG(CTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = subformula1.simplified().depth + 1
        
    def simplified(self):
        return CTLNot(CTLAF(CTLNot(self.subformulas[0])))
    
    def __str__(self):
        return "(EG %s)" % (self.subformulas[0])
    
    def __repr__(self):
        return "(EG %s)" % (self.subformulas[0])

class CTLAG(CTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = subformula1.simplified().depth + 1
        
    def simplified(self):
        return CTLNot(CTLEF(CTLNot(self.subformulas[0])))
    
    def __str__(self):
        return "(AG %s)" % (self.subformulas[0])
    
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
    
    def __str__(self):
        return "(%s AU %s)" % (self.subformulas[0],
                              self.subformulas[1])
    
    def __repr__(self):
        return "(%s AU %s)" % (self.subformulas[0],
                              self.subformulas[1])
    
def SAT(TS,formula):
    # 返回的一定是一个集合
    formula = formula.simplified()
    if formula == CTLBools(True):return set(TS.getVertexs())
    elif formula == CTLBools(False):return set()
    elif isinstance(formula,CTLState):
        return set([TS.getAVertex(formula.state)])
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
    elif isinstance(formula,CTLAF):
        return SATAF(TS,formula.subformulas[0])
    elif isinstance(formula,CTLEU):
        return SATEU(TS,formula.subformulas[0],
                     formula.subformulas[1])
    else:
        return SAT(TS,formula.simplified())
    
def SATEX(TS,formula):
    return TS.preExist(SAT(TS,formula))

def SATAF(TS,formula):
    X = set(TS.getVertexs())
    Y = SAT(TS,formula)
    while X != Y:
        X = Y
        Y = Y | TS.preAny(Y)
    return Y

def SATEU(TS,formula1,formula2):
    W = SAT(TS,formula1)
    X = set(TS.getVertexs())
    Y = SAT(TS,formula2)
    while X != Y:
        X = Y
        Y = Y | (W & TS.preExist(Y))
    return Y

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
