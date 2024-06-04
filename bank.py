class BankerAlgorithm:
    def __init__(self, p, r, available, max, allocation):
        self.p = p
        self.r = r
        self.available = available
        self.max = max
        self.allocation = allocation
        self.need = self.need(self.max, self.allocation)

    def need(self, max, allocation):
        need=[]
        for i in range(self.p):
            temp = []
            for j in range(self.r):
                temp.append(max[i][j]-allocation[i][j])
            need.append(temp)
        return need
    def chacksafe(self):
        work = self.available[:]
        finish = [False for i in range(self.p)]
        safe = []
        while True:
            flag = False
            for i in range(self.p):
                if not finish[i]:
                    flag1 = False
                    # print("当前进程",i)
                    # print(flag1)
                    for j in range(self.r):
                        if(work[j] < self.need[i][j]):
                            # print(j)
                            # print(work[j],"---",self.need[i][j])
                            flag1 = True
                            # print(flag1)

                    if(flag1 == False):
                        # print(i)
                        # print(work)
                        # print(self.need)
                        safe.append(i)
                        for j in range(self.r):
                            work[j] += self.allocation[i][j]
                        flag = True
                        finish[i] = True
            if not flag:
                break
        return all(finish), safe
if __name__ == "__main__":
    p = 4
    r = 3
    # available = [3, 3, 2]
    # max_claim = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    # allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    available = [1, 1, 1]
    max_claim = [[3, 2, 2],[6, 1, 3],[3, 1, 4],[4, 2, 2]]
    allocation = [[1, 0, 0], [5, 1, 1],[2, 1, 1],[0, 0, 2]]

    banker = BankerAlgorithm(p,r,available,max_claim,allocation)
    is_safe, sequence = banker.chacksafe()

    if is_safe:
        print("系统处于安全状态，安全序列为:", sequence)
    else:
        print("系统处于不安全状态")


