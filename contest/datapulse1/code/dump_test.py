import pandas as pd
test = pd.read_csv('contest/datapulse1/dataset/test.csv')
with open('contest/datapulse1/code/test_texts.txt', 'w', encoding='utf-8') as f:
    for i, r in test.iterrows():
        f.write(f"{r['id']}: {r['text']}\n")
print(f"Wrote {len(test)} sentences to test_texts.txt")
