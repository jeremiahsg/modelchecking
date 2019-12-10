class QueueUnderFlow(ValueError):
    pass
class SQueue():
    def __init__(self,init_len = 8):
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
        
    def enqueue(self,elem):
        if self._elnum == self._len:
            self.__extend()
            # 如果满了，自动扩充，把扩充的部分作为单独的一个函数
        self._elems[(self._head+self._elnum)%self._len] = elem
        self._elnum += 1
        
    def __extend(self):
        old_len = self._len
        self._len *= 2
        elems = [0] * self._len
        # 创建一张容量为原来两倍的表格
        for x in range(old_len):
            elems[x] = self._elems[(self._head + x)%self._len]
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
    def __init__(self,vertexs = [],edges = []):
        self.vertexs = vertexs
        self.vnum = len(vertexs)
        self.edges = edges
        self.outEdges = {}
        # 出边表示成为一个字典，字典的关键码为顶点，值为出边的到达顶点的集合
        self.verdict = {vertex.state:vertex for vertex in self.vertexs}
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
        self.vertexs.append(newVertex)
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
            self.edges.append((edge))
        elif edge[1] in self.outEdges[edge[0]]:
            raise DiGraphError('edge is already in the graph.')
        self.outEdges[edge[0]].add(edge[1])
        self.edges.append((edge))
        
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
    
    def __repr__(self):
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
    
    def stronglyConnectedComponents(self):
        # 求图中的强连通分量
        mark = {ver:0 for ver in self.getVertexs()}
        findingTime = {}
        time = 0
        low = {}
        outedges = {v:list(self.outEdges[v])
                    if v in self.outEdges else []
                    for v in self.getVertexs()}
        sccs = []
        alreadyInScc = set()
        sccstack = []
        for v in self.getVertexs():#这个循环基本只是一个摆设
            if mark[v] == 1:
                continue
            mark[v] = 1
            findingTime[v] = time
            low[v] = time
            stack = []
            stack.append((v,0))
            while stack:
                ver, nextpos = stack.pop()
                if nextpos < len(outedges[ver]):
                    newver = outedges[ver][nextpos]
                    if mark[newver] == 1:
                        stack.append((ver,nextpos+1))
                        continue
                    time += 1
                    mark[newver] = 1
                    findingTime[newver] = time
                    low[newver] = time
                    stack.append((ver,nextpos+1))
                    stack.append((newver,0))
                else:
                    ver1 = ver
                    for nextver in outedges[ver1]:
                        if nextver not in alreadyInScc:
                            low[ver1] = min(low[ver1],low[nextver])
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
    
    def isTrival(self,scc):
        if len(scc) > 1:
            return False
        else:
            v = list(scc)[0]
            if (v not in self.outEdges or 
                v not in self.outEdges[v]):
                return True
        return False
    
    def reversedReach(self,vertexs):
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
                       
class LTLFormulaError(ValueError):
    pass

class LTLFormula:
    def __init__(self,subformulas):
        self.subformulas = [x.simplified() for x in subformulas]
        
    def getSubformulas(self):
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
        
    def __eq__(self,other):
        return str(self.simplified()) == str(other.simplified())
    
    def __hash__(self):
        # 为了让formula的实例对象成为一个hashable的对象，才能加入集合中
        return hash(str(self))
    
class LTLState(LTLFormula):
    def __init__(self,name):
        self.state = name # name的类型不固定（？）
        self.subformulas= []
        self.depth = 1
    
    def simplified(self):
        return LTLState(self.state)
    
    def __repr__(self):
        return '(' + str(self.state) + ')'
    
class LTLBools(LTLFormula):
    def __init__(self,value):
        self.value = value # value的类型是bool
        self.subformulas = []
        self.depth = 1
    
    def simplified(self):
        return LTLBools(self.value)
    
    def __repr__(self):
        return str(self.value)
    
class LTLAnd(LTLFormula):
    def __init__(self,subformula1,subformula2):
        self.subformulas = [subformula1.simplified(),
                           subformula2.simplified()]
        self.depth = max(subformula1.simplified().depth,
                        subformula2.simplified().depth) + 1
        
    def simplified(self):
        return LTLAnd(self.subformulas[0],
                     self.subformulas[1])
    
    def __repr__(self):
        return "(%s and %s)" % (self.subformulas[0],
                                self.subformulas[1])
    
class LTLOr(LTLFormula):
    def __init__(self,subformula1,subformula2):
        self.subformulas = [subformula1.simplified(),
                           subformula2.simplified()]
        self.depth = max(subformula1.simplified().depth,
                        subformula2.simplified().depth) + 1
        
    def simplified(self):
        return LTLOr(self.subformulas[0],
                     self.subformulas[1])
    
    def __repr__(self):
        return "(%s or %s)" % (self.subformulas[0],
                                self.subformulas[1])

class LTLNot(LTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = subformula1.simplified().depth + 1
        
    def simplified(self):
        if self.subformulas[0] == LTLBools(True):
            return LTLBools(False)
        if self.subformulas[0] == LTLBools(False):
            return LTLBools(True)
        if isinstance(self.subformulas[0],LTLNot):
            if isinstance(self.subformulas[0].subformulas[0],LTLNot):
                return self.subformulas[0].subformulas[0].simplified()
            return self.subformulas[0].subformulas[0]
        else:
            return LTLNot(self.subformulas[0])
        
    def __repr__(self):
        return "(not %s)" % (self.subformulas[0])
    
class LTLImply(LTLFormula):
    def __init__(self,subformula1,subformula2):
        self.subformulas = [subformula1.simplified(),
                            subformula2.simplified()]
        self.depth = max(subformula1.simplified().depth,
                        subformula2.simplified().depth) + 1
    
    def simplified(self):
        return LTLOr(LTLNot(self.subformulas[0]),
                    self.subformulas[1])
    
    def __repr__(self):
        return "(%s --> %s)" % (self.subformulas[0],
                                self.subformulas[1])

class LTLNext(LTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = self.subformulas[0].depth + 1
        
    def simplified(self):
        return LTLNext(self.subformulas[0])
    
    def __repr__(self):
        return "(next %s)" % (self.subformulas[0])
    
class LTLUntil(LTLFormula):
    def __init__(self,subformula1,subformula2):
        self.subformulas = [subformula1.simplified(),
                           subformula2.simplified()]
        self.depth = max(self.subformulas[0].depth,
                        self.subformulas[1].depth) + 1
        
    def simplified(self):
        return LTLUntil(self.subformulas[0],
                       self.subformulas[1])
    
    def __repr__(self):
        return "(%s until %s)" % (self.subformulas[0],
                                 self.subformulas[1])
    
class LTLFuture(LTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = self.subformulas[0].depth + 1
        
    def simplified(self):
        return LTLUntil(LTLBools(True),
                        self.subformulas[0])
    
    def __repr__(self):
        return "(future %s)" % (self.subformulas[0])
    
class LTLGlobal(LTLFormula):
    def __init__(self,subformula1):
        self.subformulas = [subformula1.simplified()]
        self.depth = self.subformulas[0].depth + 1
    
    def simplified(self):
        return LTLNot(LTLFuture(
                        LTLNot(self.subformulas[0]
                        )))
    
    def __repr__(self):
        return "(global %s)" % (self.subformulas[0])
        
class LTLRelease(LTLFormula):
    def __init__(self,subformula1,subformula2):
        self.subformulas = [subformula1.simplified(),
                           subformula2.simplified()]
        self.depth = max(self.subformulas[0].depth,
                         self.subformulas[1].depth) + 1
        
    def simplified(self):
        return LTLNot(
                LTLUntil(
                LTLNot(self.subformulas[0]),
                LTLNot(self.subformulas[1])))
    
    def __repr__(self):
        return "(%s release %s)" % (self.subformulas[0],
                                   self.subformulas[1])
    
def constructCL(formula):
    if not isinstance(formula,LTLFormula):
        raise LTLFormulaError(formula,'is not a LTLformula.')
    formula = formula.simplified()
    CL = set()
    queue = SQueue()
    queue.enqueue(formula)
    while not queue.is_empty():
        crf = queue.dequeue()
        negativecrf = LTLNot(crf).simplified()
        if crf in CL and negativecrf in CL:
            continue
        CL = CL | {crf,negativecrf}
        if (isinstance(crf,LTLNext)):
            CL.add(LTLNext(LTLNot(
                            crf.subformulas[0])))
            CL.add(LTLNot(LTLNext(LTLNot(
                            crf.subformulas[0]))
                    ))
        elif (isinstance(negativecrf,LTLNext)):
            CL.add(LTLNext(LTLNot(
                            negativecrf.subformulas[0])))
            CL.add(LTLNot(LTLNext(LTLNot(
                            negativecrf.subformulas[0]))
                    ))
        elif (isinstance(crf,LTLUntil)):
            queue.enqueue(LTLNext(crf))
        elif (isinstance(negativecrf,LTLUntil)):
            queue.enqueue(LTLNext(negativecrf))
        for subformula in crf.subformulas:
            queue.enqueue(subformula)
        for subformula in negativecrf.subformulas:
            queue.enqueue(subformula)
    return CL

class Atom(Vertex):
    def __init__(self,name,formulaSet = set()):
        super(Atom,self).__init__(name)
        self.formulaSet = formulaSet
        self.formulaSet.add(LTLState(name))
        
    def getState(self):
        return self.state
    
    def getFormulaSet(self):
        return self.formulaSet
    
    def addFormula(self,formula):
        if not isinstance(formula,LTLFormula):
            raise LTLFormulaError(formula,'is not a formula.')
        self.formulaSet.add(formula)
    
    def __repr__(self):
        return '(%s,%s)' % (self.state,
                           self.formulaSet)
    
    def __hash__(self):
        return hash(str(self))
        
class Tableau(DiGraph):
    def __init__(self,vertexs=[],edges=[]):
        super(Tableau,self).__init__(vertexs,edges = [])
        
    def isSelfFulfilling(self,scc,closure):
        fset = set()
        for vertex in scc:
            fset = fset | vertex.getFormulaSet()
        for formula in closure:
            if isinstance(formula,LTLUntil):
                if ((formula.subformulas[1] not in fset and
                    formula in fset) or
                    (formula.subformulas[1] in fset and
                     formula not in fset)):
                    return False
        return True
        
def constructTableau(TS,CL):
    # 这个函数包含两部分
    # 第一部分是构建Tableau的顶点
    # 第二部分是构建Tableau的边
    tableau = []
    for ver in TS.getVertexs():
        tableau.append(Atom(ver.state,set()))
    sortedCL = sorted(list(CL),key = lambda x:x.depth)
    for formula in sortedCL:
        if formula == LTLBools(True):
            for v in tableau:
                v.addFormula(formula)
            continue
        elif isinstance(formula,LTLState):
            for v in tableau:
                if formula not in v.getFormulaSet():
                    v.addFormula(LTLNot(formula))
            continue
            # 这里只对公式里面提到的原子状态做处理，其余的原子状态不做处理，
            # 既不需要加入，也不需要加入其否定
        else:
            if isinstance(formula,LTLOr):
                for v in tableau:
                    if (formula.subformulas[0] in v.getFormulaSet()
                       or formula.subformulas[1] in v.getFormulaSet()):
                        v.addFormula(formula)
                    else:
                        v.addFormula(LTLNot(formula))
            elif isinstance(formula,LTLAnd):
                for v in tableau:
                    if (formula.subformulas[0] in v.getFormulaSet()
                       and formula.subformulas[1] in v.getFormulaSet()):
                        v.addFormula(formula)
                    else:
                        v.addFormula(LTLNot(formula))
            elif (isinstance(formula,LTLNext) and
                 not isinstance(formula.subformulas[0],LTLNot)):
                splitv = []
                for v in tableau:
                    splitv.append(Atom(v.getState(),
                        v.getFormulaSet()|{LTLNot(formula),
                        LTLNext(LTLNot(formula.subformulas[0]))}))
                    v.addFormula(formula)
                    v.addFormula(LTLNot(LTLNext(LTLNot(
                                formula.subformulas[0]))))
                for vv in splitv:
                    tableau.append(vv)
                continue
            # next问题还要仔细琢磨一下
            # 一下until的算法和pymodelchecking 里面的不同，但是和书上的相同
    for formula in sortedCL:
        if isinstance(formula,LTLUntil):
            for v in tableau:
                if formula.subformulas[1] in v.getFormulaSet():
                    v.addFormula(formula)
                elif (formula.subformulas[0] in v.getFormulaSet() and
                      LTLNext(formula) in v.getFormulaSet()):
                    v.addFormula(formula)
                else:
                    v.addFormula(LTLNot(formula))
        # 这里的分类没有分Not类是因为他肯定会被放到集合里面
        # 这里的分类有没有漏掉？
    # tableau是所有的TAB内部的顶点
    TAB = Tableau(vertexs = tableau)
    findState = dict()
    for v in TAB.getVertexs():
        if v.state not in findState:
            findState[v.state] = [v]
        else:
            findState[v.state].append(v)
    NextList = []
    for formula in CL:
        if isinstance(formula,LTLNext):
            NextList.append(formula)
    for edge in TS.getEdges():
        for v1 in findState[edge[0].state]:
            for v2 in findState[edge[1].state]:
                flag = True
                for formula in NextList:
                    if ((formula in v1.getFormulaSet() and
                        formula.subformulas[0] not in v2.getFormulaSet()) or
                        (formula not in v1.getFormulaSet() and
                        formula.subformulas[0] in v2.getFormulaSet())):
                        flag = False
                        break
                if flag:
                    TAB.addEdge((v1,v2))
    return TAB

def findNotSAT(TS,formula):
    if not isinstance(formula,LTLFormula):
        raise LTLFormulaError(formula,'is not a formula.')
    negativeformula = LTLNot(formula).simplified()
    CL = constructCL(negativeformula)
    #print(CL,end = '\n\n')
    tableau = constructTableau(TS,CL)
    #print(tableau,end = '\n\n')
    sccs = tableau.stronglyConnectedComponents()
    ans = set()
    #print(sccs,end = '\n\n')
    for scc in sccs:
        #print(scc,end = '\n\n')
        if ((not tableau.isTrival(scc)) and
            tableau.isSelfFulfilling(scc,CL)):
            ans = ans | tableau.reversedReach(scc)
    return {w.state for w in ans
            if negativeformula in w.getFormulaSet()}
# 返回的应该是不满足formula条件的顶点

def LTLModelChecking(TS,formula,init):
    if not isinstance(TS,DiGraph):
        raise DiGraphError(TS,'is not a digraph,please input again!')
    if not isinstance(init,Vertex):
        raise DigraphError(init,'is not a vertex,please input again!')
    if not isinstance(formula,LTLFormula):
        raise LTLFormulaError(formula,'is not a LTLFormula,please input again!')
    sccs = TS.stronglyConnectedComponents()
    goodPoints = set()
    for scc in sccs:
        if (not TS.isTrival(scc)):
            goodPoints = goodPoints | TS.reversedReach(scc)
    if not init in goodPoints:
        raise DiGraphError('''The initial state must be connected
         to one strongly connected conponent,please choose another
         initial state or input again.''')
    print(init.state)
    if init.state not in findNotSAT(TS,formula):
        return True
    else:return False
    #这里要求被检测的初始顶点必须被可以连接到一个非平凡强连通分量上，否则模型检测无意义。
        
            
                        
   
aaa = LTLState('a')
bbb = LTLState('c')
ccc = LTLUntil(aaa,bbb)
a = Vertex('a')
b = Vertex('b')
c = Vertex('c')
d = Vertex('d')
ts = DiGraph(vertexs = [a,b,c,d],
            edges = [(a,c),(b,a),(d,c),(c,b)])
print(ccc)

print(findNotSAT(ts,ccc))
print(LTLModelChecking(ts,ccc,a))
print(LTLModelChecking(ts,ccc,b))
print(LTLModelChecking(ts,ccc,c))
print(LTLModelChecking(ts,ccc,d))
