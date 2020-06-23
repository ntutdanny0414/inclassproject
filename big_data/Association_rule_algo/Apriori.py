all_inform = {}
def load_data():#inputdata
    '''
    data from text book
    '''
    data = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
            ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
            ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]

    return data

def find_fre_1_item(data,min_sup):#找1-item
    attr = []
    for i in data:
        for item in i:
            if item not in attr:
                attr.append(item)
    f1_num = {}
    f1_support = {}
    for i in data:
        for item in attr:
            if item in i:
                if item not in f1_num:
                    f1_num[item] = 1
                    all_inform[tuple([item])] = 1
                else:
                    f1_num[item] += 1
                    all_inform[tuple([item])] += 1
    num = float(len(data))
    for item in f1_num:
        if (f1_num[item] / num) >= min_sup:
            f1_support[tuple([item])] = f1_num[item] / num

    return f1_support
def has_infre_subset(Ck_one,Lk1_set):
    for i in Ck_one:
        subset = Ck_one - set([i])
        if subset not in Lk1_set:
            return True
    return False

def Apriori_gen(Lk):#ck候選
    Ck = []
    to_set = []
    for i in Lk:
        to_set.append(set(i))
    for i in range(len(to_set)):
        for j in range(i+1,len(to_set)):
            join = (to_set[i] | to_set[j])
            if not has_infre_subset(join,to_set):#prune
                check = sorted(list(join))
                if check not in Ck:
                    Ck.append(check)
    
    return Ck

def find_fre_k_item(data,Ck,min_sup):#找k-item
    fk_num = {}
    fk_support = {}
    for i in data:
        for item in Ck:
            if set(item).issubset(set(i)):
                if tuple(item) not in fk_num:
                    fk_num[tuple(sorted(item))] = 1
                    all_inform[tuple(sorted(item))] = 1
                else:
                    fk_num[tuple(sorted(item))] += 1
                    all_inform[tuple(sorted(item))] += 1
    num = float(len(data))
    for item in fk_num:
        if (fk_num[item] / num) >= min_sup:
            fk_support[item] = fk_num[item] / num
    return fk_support
def printLk(Lk):
    print('itemset----support')
    for i in Lk:
        print(list(i),Lk[i])
def printCK(CK):
    print('CK-------')
    for i in range(len(CK)):
        print(CK[i])
def subset(set):
    alist = [[]]
    for item in set:
        alist += [y + [item] for y in alist]
    alist.remove([])
    alist.remove(set)
    return alist
def getlist(sub,alllist):
    allsub = []
    for i in range(len(alllist)):
        if alllist[i] not in sub:
            allsub.append(alllist[i])
    return allsub
def printrule(Lk):
    print('final-----rule')
    for i in Lk:
        rule = subset(list(i))
        for j in range(len(rule)):
            conf = all_inform[tuple(i)] / all_inform[tuple(rule[j])]
            print(rule[j],'=>',getlist(rule[j],i),'conf:',conf)
            
if __name__ == "__main__":
    min_sup = 0.22 #最小支持(比率)
    data = load_data()
    L1 = find_fre_1_item(data,min_sup)
    print('k = 1')
    printLk(L1)
    Lk = L1
    k = 2
    while True:
        CK = Apriori_gen(Lk)
        if len(CK) == 0:
            break
        print('k = '+str(k))
        printCK(CK) 
        Lk = find_fre_k_item(data,CK,min_sup)
        printLk(Lk)    
        k = k + 1
    printrule(Lk)
