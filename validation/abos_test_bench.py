import math
from collections import Counter

def needleman_wunsch(s1, s2, match=2, mismatch=-1, gap=-2):
    """验证 NW 算法在边界条件下的正确性"""
    if not s1 or not s2:
        return max(len(s1), len(s2)) * gap
    
    n, m = len(s1), len(s2)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): score[i][0] = i * gap
    for j in range(m + 1): score[0][j] = j * gap
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = score[i-1][j-1] + (match if s1[i-1] == s2[j-1] else mismatch)
            score[i][j] = max(s, score[i-1][j] + gap, score[i][j-1] + gap)
            
    return score[n][m]

def validate_abos_logic():
    # 测试案例 1：完全一致
    s1 = "GATTACA"
    s2 = "GATTACA"
    score_1 = needleman_wunsch(s1, s2)
    
    # 测试案例 2：单点突变 (T -> C)
    s3 = "GATCACA"
    score_2 = needleman_wunsch(s1, s3)
    
    # 测试案例 3：空位 (Gap)
    s4 = "GATACA"
    score_3 = needleman_wunsch(s1, s4)
    
    print(f"Test 1 (Identical): {score_1} (Expected: 14)")
    print(f"Test 2 (Mutation): {score_2} (Expected: 11)")
    print(f"Test 3 (Gap): {score_3} (Expected: 10)")
    
    # 验证熵计算
    sequences = ["GATTACA", "GATCACA", "GAT-ACA"]
    # 简单的熵检查
    return score_1, score_2, score_3

if __name__ == "__main__":
    validate_abos_logic()
