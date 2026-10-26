import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
p = r'E:\Obsidian仓库\ZhouXuan私人领域\05-个人\人物画像.md'
L = open(p, encoding='utf-8').read().splitlines()
print('TOTAL_LINES', len(L))
print('--- HEADINGS ---')
for i, l in enumerate(L):
    if l.startswith('## ') or l.startswith('### '):
        print(i + 1, l)
print('--- TAIL 40 ---')
for l in L[-40:]:
    print(l)
