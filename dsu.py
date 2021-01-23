class DSU:


    def __init__(self):
        self.parent = []
        self.rank = []


    def clear(self):
        self.parent = []
        self.rank = []


    def set_size(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n


    def size(self):
        return len(self.parent)


    def find(self, v):
        if v == self.parent[v]:
            return v
        self.parent[v] = self.find(self.parent[v])
        return self.parent[v]


    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a != b:
            if self.rank[a] < self.rank[b]:
                a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1


    def find_classes(self):
        classes = []
        n = len(self.parent)
        for i in range(n):
            classes.append(self.find(i))
        return classes