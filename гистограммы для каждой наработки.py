import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('db.csv', engine='python', encoding='cp1251', quoting=3, delimiter=';')

steel_name = "15Х1М1ФЛ"
df_filtered = df[df['steel'] == steel_name]


operating_ranges = {
    '150_200': df_filtered.query('operating < 200000'),
    '200_250': df_filtered.query('200000 < operating < 250000'),
    '250_300': df_filtered.query('250000 < operating < 300000'),
    '300_350': df_filtered.query('300000 < operating < 350000'),
    '350_400': df_filtered.query('350000 < operating < 400000'),
    '400_450': df_filtered.query('operating > 400000')
}


params = ['yieldstr', 'tensstr', 'elongation', 'relnarr', 'hardness',
          'yieldstr500', 'tensstr500', 'elongation500', 'relnarr500', 
          'hardness500', 'discosure', 'kcv80', 'kcv150',  'viscosity80', 
          'viscosity150', 'spheroidization2', 'carbides', 'betcarbs']
params_dict = {'yieldstr': 'Предел текучести, МПа', 
               'tensstr': "Предел прочности, МПа",
               'elongation': "Относительное удлинение, %",
               'relnarr': "Относительное сужение, %",
               'hardness': "Твёрдость, НВ",
               'yieldstr500': "Предел прочности (температура эксплутации), МПа",
               'tensstr500':"Предел прочности (температура эксплутации), МПа", 
               'elongation500':"Относительное удлинение (температура эксплутации), %",
               'relnarr500': "Относительное сужение (температура эксплутации), %", 
               'hardness500': "Твёрдость (температура эксплутации), МПа", 
               'discosure': "Раскрытие трещины, мм", 
               'kcv80': "Ударная вязкость (при 80 град), Дж/см2",
               'kcv150': "Ударная вязкость (при 150 град), Дж/см2", 
               'viscosity80': "Доля вязкой составляющей (80 град), %", 
               'viscosity150': "Доля вязкой составляющей (150 град), %", 
               'spheroidization2': "Балл сфероидизации",
               'carbides': "Размер карбидов, мкм", 
               'betcarbs' : " Расстояние между карбидами, мкм"}


def add_labels(ax):
    for p in ax.patches:
        height = p.get_height()
        if height > 0:  #пустые столбики без числа наверху
            ax.annotate(f'{int(height)}', 
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='center', 
                        xytext=(0, 9), 
                        textcoords='offset points')


for param in params:
    for range_name, data in operating_ranges.items():
        if param in data.columns:
            data_non_null = data[param].dropna()
            plt.figure(figsize=(12, 8))
            num_bins = int(np.cbrt(len(data[param])))
            ax = sns.histplot(data[param], kde=False, bins=num_bins, alpha=0.7)
            add_labels(ax)
            plt.xlabel(f'{params_dict[param]} для наработки {range_name}, сталь {steel_name}' )
            plt.ylabel('Frequency')
       
            ax.grid(which = "major", linewidth = 1)
            ax.grid(which = "minor", linewidth = 0.2)
            ax.minorticks_on()
            plt.show()

