with open(f'D:\project Hlinh\Merged_sorted_converted.csv', 'r', encoding='utf-8') as f:
    text = f.read()

chars = sorted(set(text))
vocabsize = len(chars)

#print(' '.join(chars))
#print(vocabsize)

stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encoding = lambda s: [stoi[c] for c in s] 
decoding = lambda l: ''.join([itos[i] for i in l]) 

print(encoding("hlinh"))
print(decoding(encoding("hlinh")))