import SQueue

class FormulaError(ValueError):
    pass

class Formula:
    def __init__(self,subformulas = []):
        self.subformulas = [x.simplified() for x in subformulas]
        
    def getSubformulas(self):
        # 获得全部的子公式，返回一个表格
        return self.subformulas
    
    def subfomula(self,i):
        # 获得某一个子公式，返回一个Formula 类的实例对象
        if not self.subformulas:
            raise FormulaError('This formula doesnot have subformula.')
        if not (0<= i < len(self.subformulas)):
            raise FormulaError('Index Error.')
        return self.subformulas[i]
    
    def setSubformula(self,i,newsubformula):
        # 修改一个子公式
        self.subformulas[i] = newsubformula
    
class State(Formula):
    def __init__(self,name):
        # name的类型是一个字符串
        self.state = name
        self.subformulas = []
        self.depth = 1
        # depth这个属性记录公式的层数，每在外面套一层就加一，
        # 这是为了计算后面的基本集合Elementary Set而设立的；
        
    def isAState(self):
        return True
    
    def __str__(self):
        return self.state
    
    def simplified(self):
        return State(self.state)
    
class Bools(Formula):
    def __init__(self,value):
        # value是一个布尔值，只有true和false两种
        self.value = value
        self.subformulas = []
        self.depth = 1
        
    def isAState(self):
        return True
    
    def __str__(self):
        return str(slf.value)
    
    def simplified(self):
        return Bools(self.value)
    
class And(Formula):
    def __init__(self,subformula1,subformula2):
        assert isinstance(subformula1,Formula)
        assert isinstance(subformula2,Formula)
        self.subformulas = [subformula1,subformula2]
        self.depth = max(subformula1.depth,
                        subformula2.depth) + 1
        
    def isAState(self):
        return False
    
    def __str__(self):
        return ('( '+str(self.subformulas[0])+' and '
                + str(self.subformulas[1])+' )')
    
    def simplified(self):
        return And(self.subformulas[0],
                  self.subformulas[1])
    
class Or(Formula):
    def __init__(self,subformula1,subformula2):
        assert isinstance(subformula1,Formula)
        assert isinstance(subformula2,Formula)
        self.subformulas = [subformula1,subformula2]
        self.depth = max(subformula1.depth,
                        subformula2.depth) + 1
        
    def isAState(self):
        return False
    
    def __str__(self):
        return ('( '+str(self.subformulas[0])+' or '
                + str(self.subformulas[1])+' )')
    
    def simplified(self):
        return And(self.subformulas[0],
                  self.subformulas[1])
    
class Not(Formula):
    def __init__(self,subformula1):
        assert isinstance(subformula1,Formula)
        self.subformulas = [subformula1]
        self.depth = subformula1.depth + 1
        # not 这里应该涉及到双重否定的简化问题
        
    def isAState(self):
        return False
    
    def __str__(self):
        return 'not ' + str(self.subformulas[0])
    
    def simplified(self):
        if isinstance(self.subformulas[0],Not):
            tmp = self.subformulas[0].subformulas[0]
            if isinstance(tmp,Not):
                tmp = tmp.simplified()
            return tmp
        return Not(self.subformulas[0])
    
class Next(Formula):
    def __init__(self,subformula1):
        assert isinstance(subformula1,Formula)
        self.subformulas = [subformula1]
        self.depth = subformula1.depth + 1
        
    def isAState(self):
        return False
    
    def __str__(self):
        return 'next (' + str(self.subformulas[0]) + ')'
    
    def simplified(self):
        return Next(subformulas[0])
    
class Until(Formula):
    def __init__(self,subformula1,subformula2):
        assert isinstance(subformula1,Formula)
        assert isinstance(subformula2,Formula)
        self.subformulas = [subformula1,subformula2]
        self.depth = max(subformula1.depth,
                        subformula2.depth) + 1
        
    def isAState(self):
        return False

    def __str__(self):
        return ('( '+str(self.subformulas[0])+' until '
                + str(self.subformulas[1])+' )')
    
    def simplified(self):
        return Until(self.subformulas[0],
                  self.subformulas[1])
    
def constructAFormula(string):
    assert isinstance(string,str)
    stack = []
    # 假设输入的格式为空格分开每两个需要分开的元素
    # 一个状态名中间没有空格，
    # 括号和状态名之间空格，状态名和运算符之间空格
    # 所有的子公式都有括号括起，一对括号之间至多只有一对运算符
    operators = {'X','U','not','and','or'}
    bools = {True,False}
    for x in string.split():
        if x != ')':
            stack.append(x)
        else:
            sub1 = stack.pop()
            if isinstance(sub1,str):
                sub1 = State(sub1)
            elif isinstance(sub1,bool):
                sub1 = Bools(sub1)
            op = stack.pop()
            if op not in operators:
                raise FormulaError(op,'is not a operator.')
            if op == 'X':
                sub1 = Next(sub1)
                stack.pop()
                stack.append(sub1)
                continue
            elif op == 'not':
                sub1 = Not(sub1)
                stack.pop()
                stack.append(sub1)
                continue
            else:
                sub2 = stack.pop()
                if isinstance(sub2,str):
                    sub2 = State(sub2)
                elif isinstance(sub2,bool):
                    sub2 = Bools(sub2)
                elif not isinstance(sub2,Formula):
                    return FormulaError(sub2,'is not a formula.')
                if op == 'and':
                    sub = And(sub2,sub1)
                    stack.pop()
                    stack.append(sub)
                    continue
                elif op == 'or':
                    sub = Or(sub2,sub1)
                    stack.pop()
                    stack.append(sub)
                elif op == 'U':
                    sub = Until(sub2,sub1)
                    stack.pop()
                    stack.append(sub)
                else:
                    raise FormulaError('Not a Formula.')
    if len(stack) != 1:
        raise FormulaError('Formula is Wrong.Please input again.')
    return stack[0]
                
class ClosureError(ValueError):
    pass

class Closure:
    def __init__(self,formula):
        if not isinstance(formula,Formula):
            raise ClosureError(formula,'is not a formula.')
        self.closure = self.constructAClosure(formula)
        
    def constructAClosure(self,formula):
        queue = SQueue()
        closure = set()
        queue.enqueue(formula)
        while not queue.is_empty():
            crf = queue.dequeue().simplified()
            # crf for current formula
            if isinstance(crf,Not):
                crf = crf.subformulas[0]
            if not crf in closure:
                closure.add(crf.simplified())
                closure.add(Not(crf).simplified())
                if (isinstance(crf,State) or
                    isinstance(crf,Bools)):
                    continue
                elif (isinstance(crf,Not) or
                      isinstance(crf,Next)):
                    queue.enqueue(crf.subformulas[0])
                else:
                    queue.enqueue(crf.subformulas[0])
                    queue.enqueue(crf.subformulas[1])
        return closure
    
    def __str__(self):
        return str({(str(x),x.depth) for x in self.closure})
