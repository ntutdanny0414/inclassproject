from math import sqrt
from collections import Counter
def euclidean_distance(features,predict,n):
    need_sqrt = 0
    for i in range(n):
        need_sqrt = need_sqrt + (features[i]-predict[i])**2
    return sqrt(need_sqrt)


def k_nearest_neighbors(data, predict,k,n):
    distances = []
    for group in data:
        for features in data[group]:
            distance_out = euclidean_distance(features,predict,n)
            distances.append([distance_out, group])

    votes = [i[1] for i in sorted(distances)[:k]]
    print(votes)
    vote_result = Counter(votes).most_common(1)[0][0]
    confidence = Counter(votes).most_common(1)[0][1] / k
  
    return vote_result, confidence

def main():
    #input#
    data = {'a':[[1,2],[2,3],[3,1]], 'b':[[6,5],[7,7],[8,6]]}
    predict = [4,5]

    result = k_nearest_neighbors(data, predict,3,2)#k=3,n=2
    
    print(result)#b兩個a一個



main()
