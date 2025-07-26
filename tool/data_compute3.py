import os

def compute(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"): 
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
                l_s = lines[0].strip()
                e_a = lines[1].strip()
                e_f = lines[2].strip()
                
        human_likeness.append(l_s)
        smoothness.append(e_a)
        semantic_accuracy.append(e_f)

def calculate_average(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    a = 0
    b = 0
    c = 0

    for row in matrix:
        for i in range(cols):
            if i%3 == 0:
                a += int(row[i])
            elif i%3 == 1:
                b += int(row[i])
            elif i%3 == 2:
                c += int(row[i])

    a = round(a/rows/(cols/3), 2)
    b = round(b/rows/(cols/3), 2)
    c = round(c/rows/(cols/3), 2)
    return a, b, c

import pandas as pd

if __name__ == '__main__':
    Methods = ['rym', 'rym_sem', 'ours']
    method_num = len(Methods)
    video_num = method_num*3
    dataset=['ablation']
    excel_path = 'output.xlsx'

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for data in dataset:
            folder_path = fr'result\{data}'
            human_likeness = []
            smoothness = []
            semantic_accuracy = []
            compute(folder_path)
            human_likeness1, human_likeness2, human_likeness3 = calculate_average(human_likeness)
            smoothness1, smoothness2, smoothness3 = calculate_average(smoothness)
            semantic_accuracy1, semantic_accuracy2, semantic_accuracy3 = calculate_average(semantic_accuracy)

            Rym = [human_likeness1, human_likeness2, human_likeness3]
            Rym_sem = [smoothness1, smoothness2, smoothness3]
            Ours = [semantic_accuracy1, semantic_accuracy2, semantic_accuracy3]

            df = pd.DataFrame({
                'method': Methods,
                'human_likeness': Rym,
                'smoothness': Rym_sem,
                'semantic_accuracy': Ours
            })

            df.columns.values[0] = f'{data}'
            df.to_excel(writer, sheet_name=data, index=False)

            print(df)
            #print('\n')