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
