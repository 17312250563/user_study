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
    a = b = c = d = e = 0
    all = [a, b, c, d, e]

    for row in matrix:
        for i in range(cols):
            if i % 5 == 0:
                all[0] += int(row[i]) + 1
            elif i % 5 == 1:
                all[1] += int(row[i]) + 1
            elif i % 5 == 2:
                all[2] += int(row[i]) + 1
            elif i % 5 == 3:
                all[3] += int(row[i]) + 1
            elif i % 5 == 4:
                all[4] += int(row[i]) + 1

    # 计算平均值并保留两位小数
    for i in range(5):
        all[i] = round(all[i] / rows / (cols / 5), 2)  # 保留两位小数

    return all



import pandas as pd

if __name__ == '__main__':
    Methods = ['camn', 'diffsheg', 'ours','semantic gesticulator', 'diffusestylegesture']
    method_num = len(Methods)
    dataset=['comparsion']
    excel_path = 'output.xlsx'

    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        for data in dataset:
            folder_path = fr'result1\{data}'
            human_likeness = []
            smoothness = []
            semantic_accuracy = []
            compute(folder_path)
            Human_likeness = calculate_average(human_likeness)
            Smoothness = calculate_average(smoothness)
            Semantic_Accuracy = calculate_average(semantic_accuracy)

            df = pd.DataFrame({
                'method': Methods,
                'human_likeness': Human_likeness,
                'smoothness': Smoothness,
                'semantic_accuracy': Semantic_Accuracy
            })

            df.columns.values[0] = f'{data}'
            df.to_excel(writer, sheet_name=data, index=False)

            print(df)
            #print('\n')