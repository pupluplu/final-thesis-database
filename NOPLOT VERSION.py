import psycopg2
import tkinter as tk 
from tkinter import ttk
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    host="localhost",
    database="Powerstation_db",
    user="postgres",
    password="") 
cur = conn.cursor()

#Открываем окно
win = tk.Tk()
win.config(bg='#D3E9FF')
win.title("guzelka's app")
win.geometry("500x400+100+10")

steel = tk.StringVar()

def steel_select():
    
    if steel_choice_var.get()==1:
        steel.set('15Х1М1ФЛ')
    elif steel_choice_var.get()==2:
        steel.set('20ХМЛ')
    elif steel_choice_var.get()==3:
        steel.set('20ХМФЛ')
    return steel.get()


        
part_namesq = tk.StringVar()
part_symbols = tk.IntVar()
def get_entry():
    part_namesq.set(part_name.get())
    n = part_name.get()
    part_name.delete("0", tk.END)
    part_symbols.set(len(n))
    return part_namesq, part_symbols.get()


params_name = tk.StringVar()
params = []

def type_select():
    global params_name
    if var1.get() == 1:
        params = ['Предел текучести', "Предел прочности", "Относительное удлинение", "Относительное сужение", "Твердость"]
        params_name.set('mechprops20')  # изменяем значение глобальной переменной
    elif var1.get() == 2:
        params = ['Предел текучести', "Предел прочности", "Относительное удлинение", "Относительное сужение", "Твердость", "Раскрытие трещины"]
        params_name.set('mechprops500')
    elif var1.get() == 3:
        params = ["KCV 80 градусов", "KCV 150 градусов", "Доля вязкой составляющей при T = 80 градусов","Доля вязкой составляющей при T = 150 градусов"]
        params_name.set('impactbending')
    elif var1.get() == 4:
        params = ["Cфероидизация", "Размер карбидов", "Расстояние между карбидами"]
        params_name.set('microstr')
    params_combobox['values'] = params
    
    return params_name.get() # возвращаем значение переменной, чтобы можно было его использовать далее

selected_param = tk.StringVar()
param_key = tk.StringVar()

def param_select():
    global selected_param
    global param_key
    params_values = {'Предел текучести': 'yieldstr',
                     'Предел прочности': 'tensstr',
                     'Относительное удлинение': 'elongation',
                     'Относительное сужение': 'relnarr',
                     'Твердость': 'hardness',
                     'Раскрытие трещины': 'discosure',
                     'KCV 80 градусов':'kcv80',
                     'KCV 150 градусов': 'kcv150',
                     'Доля вязкой составляющей при T = 80 градусов': 'viscosity80',
                     'Доля вязкой составляющей при T = 150 градусов': 'viscosity150',
                     'Cфероидизация': 'spheroidization2',
                     'Размер карбидов': 'carbides',
                     'Расстояние между карбидами':'betcarbs'}
    selected_param =params_combobox.get()
    param_key.set(params_values[selected_param])
    return param_key, selected_param

    

    
#Выбор марки стали
#Сами кнопки
steel_choice_var = tk.IntVar()

label_steel_choice = tk.Label(win, text='Выбор стали')
label_steel_choice.grid()

btn_steel_choice1 = tk.Radiobutton(win, text="15Х1М1ФЛ", variable=steel_choice_var, value=1, command = steel_select)
btn_steel_choice1.grid(row=1, column=0)
btn_steel_choice2 = tk.Radiobutton(win, text="20ХМЛ", variable=steel_choice_var, value=2, command = steel_select)
btn_steel_choice2.grid(row=1, column=1)
btn_steel_choice3 = tk.Radiobutton(win, text="20ХМФЛ", variable=steel_choice_var, value=3, command = steel_select)
btn_steel_choice3.grid(row=1, column=2)


#выбор детали
label_part_choice = tk.Label(win, text='Выбор детали')
label_part_choice.grid(row=2, column=0)
part_name = tk.Entry(win)
part_name.grid(row=3, column=0)
btn_get_entry = tk.Button(win, text='get', command=get_entry)
btn_get_entry.grid(row = 3, column = 1, stick = 'we')

#выбор таблицы
var1 = tk.IntVar()

temperature_radio20 = tk.Radiobutton(win, text="Комнатная температура", variable=var1, value=1, command = type_select)
temperature_radio20.grid(row=5, column=0)

temperature_radio500 = tk.Radiobutton(win, text="Температура эксплуатации", variable=var1, value=2, command = type_select)
temperature_radio500.grid(row=5, column=1)

impactbending_radio = tk.Radiobutton(win, text="Испытания на ударный изгиб", variable=var1, value=3, command = type_select)
impactbending_radio.grid(row=5, column=2)

microstr_radio = tk.Radiobutton(win, text="Микроструктура", variable=var1, value=4, command = type_select)
microstr_radio.grid(row=5, column=3) 


params_combobox = ttk.Combobox(win)
params_combobox.grid(row = 6, column = 0, ipadx=55)
param_btn = tk.Button(win, text = 'get', command = param_select)
param_btn.grid(row = 6, column =1, stick = 'we')




    

def execute_sql_query():

    print(type(part_namesq))
    params_name_value = params_name.get()
    param_key_value = param_key.get()
    part_symbols_value = part_symbols.get()
    part_namesq_value = part_namesq.get()
    steel_value = steel.get()
  
    # Затем строим SQL-запрос с использованием собранных значений
    sql_query = f"""SELECT repair.operating, {params_name_value}.{param_key_value}
                    FROM repair
                    JOIN parts ON repair.id = parts.turbineid
                    JOIN {params_name_value} ON parts.partid = {params_name_value}.partid
                    WHERE LEFT(parts.partname, {part_symbols_value}) = '{part_namesq_value}' AND parts.steel = '{steel_value}'
                    GROUP BY repair.operating, {params_name_value}.{param_key_value}
                    ORDER BY repair.operating ASC;"""
    print (sql_query)
    
    # Затем выполняем SQL-запрос
    cur.execute(sql_query)
    result = cur.fetchall()
        
    
    tensstr_values = [row[0] for row in result]
    frequency = [row[1] for row in result]
    
    # Строим график
    plt.scatter(tensstr_values, frequency)
    plt.ylabel(f"{selected_param}")
    plt.xlabel("Время работы")
    plt.show()
    conn.close()
    print (    params_name_value, param_key_value, part_symbols_value, part_namesq_value, steel_value)
execute_button = tk.Button(win, text="Execute SQL Query", command=execute_sql_query)
execute_button.grid(row=7, column=0, columnspan=2)





    


win.mainloop()