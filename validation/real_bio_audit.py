import math

def needleman_wunsch(s1, s2, match=2, mismatch=-1, gap=-2):
    n, m = len(s1), len(s2)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): score[i][0] = i * gap
    for j in range(m + 1): score[0][j] = j * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = score[i-1][j-1] + (match if s1[i-1] == s2[j-1] else mismatch)
            score[i][j] = max(s, score[i-1][j] + gap, score[i][j-1] + gap)
    return score[n][m]

# 真实数据：SARS-CoV-2 Spike Protein 氨基酸序列片段 (60-80位)
# 参考自：NCBI Reference Sequence: NC_045512.2
wuhan_spike_60_80 = "SNVTWFHAIHVSGTNGTKRF"
# 参考自：Omicron B.1.1.529 变异株序列
omicron_spike_60_80 = "SNVTWFHVISGTNGTKRF" # 包含 69-70 缺失 (Δ69-70) 和 A67V, H69-V70del

print(f"Alignment Audit Result:")
print(f"Target:  {wuhan_spike_60_80}")
print(f"Subject: {omicron_spike_60_80}")
score = needleman_wunsch(wuhan_spike_60_80, omicron_spike_60_80)
print(f"DAS (Deterministic Alignment Score): {score}")

# 逻辑校验：如果完全匹配，得分应为 20 * 2 = 40
# 考虑到突变和缺失，得分应该明显下降。
