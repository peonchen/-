class BankerAlgorithm:
    def __init__(self, p, r, available, max, allocation):
        self.p = p
        self.r = r
        self.available = available
        self.max = max
        self.allocation = allocation
        self.finish = []
        self.need = self.need(self.max, self.allocation)
        self.safe = []
        self.WA = []  # work+allocation
        self.work = []

    def need(self, max, allocation):
        need=[]
        for i in range(self.p):
            temp = []
            for j in range(self.r):
                temp.append(max[i][j]-allocation[i][j])
            need.append(temp)
        return need

    def check_safe_with_request(self, request, process):
        work = self.available[:]
        self.safe = []
        self.finish = [False for _ in range(self.p)]
        for i in range(self.r):
            if request[i] > self.need[process][i] or request[i] > self.available[i]:
                return False, []
        for j in range(self.r):
            self.available[j] -= request[j]
            self.allocation[process][j] += request[j]
            self.need[process][j] -= request[j]
        # is_safe, sequence = self.check_safe()
        # for j in range(self.r):
        #     self.available[j] += request[j]
        #     self.allocation[process][j] -= request[j]
        #     self.need[process][j] += request[j]
        
        return self.check_safe()            
    def check_safe(self):
        self.WA = []
        work = self.available[:]
        self.safe = []
        self.finish = [False for i in range(self.p)]
        while True:
            flag = False
            for i in range(self.p):
                if not self.finish[i]:
                    flag1 = False
                    for j in range(self.r):
                        if(work[j] < self.need[i][j]):
                            flag1 = True
                    if(flag1 == False):
                        self.safe.append(i)
                        self.work.append(work[:])
                        for j in range(self.r):
                            work[j] += self.allocation[i][j]
                        # print(work) 
                        self.WA.append(work[:])
                        flag = True
                        self.finish[i] = True
            if not flag:
                break
        return all(self.finish), self.safe
    def show(self):
        print("系统资源\t\t",self.available)
        print("-"*90)
        print("进程\tMax\t\tWork\t\tAllocation\tNeed\t\tWork+Allocation\t\tFinish")
        for safe, i  in zip(self.safe,range(self.p)):
            print("-"*90)
            print(f"{safe}\t{self.max[safe]}\t{self.work[i]}\t{self.allocation[safe]}\t{self.need[safe]}\t{self.WA[i]}\t\t{self.finish[safe]}")
        print("-"*90)    
if __name__ == "__main__":
    p = 5
    r = 3
    available = [3, 3, 2]
    max_claim = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
    allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    # available = [1, 1, 2]
    # max_claim = [[3, 2, 2],[6, 1, 3],[3, 1, 4],[4, 2, 2]]
    # allocation = [[1, 0, 0], [5, 1, 1],[2, 1, 1],[0, 0, 2]]
    banker = BankerAlgorithm(p,r,available,max_claim,allocation)
    is_safe, sequence = banker.check_safe()
    if is_safe:
        print("系统处于安全状态，安全序列为:", sequence)
        banker.show()
    else:
        print("系统处于不安全状态")
    process = 1
    request = [1, 0, 2]
    is_safe,sequence=banker.check_safe_with_request(request,process)
    if is_safe:
        print("系统处于安全状态，安全序列为:", sequence)
        banker.show()
    else:
        print("系统处于不安全状态")



