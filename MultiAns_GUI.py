import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
import os
import json
from turtle import bgcolor

# loadData
def load_R1_file(input_dir):
    with open(input_dir, 'r', encoding='utf-8') as f:
        dataList_R1=json.load(f)
    return dataList_R1

def load_file(input_dir):
    with open(input_dir, 'r', encoding='utf-8') as f:
        dataList_R2=json.load(f)
        new_dataList=list()
        for dataList_R1 in dataList_R2:
            for data in dataList_R1:
                new_dataList.append(data)
    return new_dataList
    
def getData(num, dataList):
    Original_ques_id = dataList[num]["Original_ques_id"]
    query = dataList[num]["query"]
    Retrieved_article_id = dataList[num]["Retrieved_article_id"]
    Retrieved_answer = dataList[num]["Retrieved_answer"]
    summary = dataList[num]["summary"]
    summary_span = dataList[num]["summary_span"]
    del dataList
    return Original_ques_id, query, Retrieved_article_id, Retrieved_answer, summary, summary_span

def checkFileRepeat(mark_dataList):
    global number
    try:
        mark_dataList[number]
        return True
    except IndexError:
        return False

# Textframe
def setQueryInput(text):
    Query_text.configure(state='normal')
    Query_text.delete(1.0, 'end')
    Query_text.insert(1.0, text)
    Query_text.configure(state='disabled')
    
def setAnswerInput(text):
    Retrieved_answer_text.configure(state='normal')
    Retrieved_answer_text.delete(1.0, 'end')
    Retrieved_answer_text.insert(1.0, text)
    Retrieved_answer_text.configure(state='disabled')

def setSummaryInput(text):
    Summary_text.configure(state='normal')
    Summary_text.delete(1.0, 'end')
    Summary_text.insert(1.0, text)
    Summary_text.configure(state='disabled')
    
def setAnswerhighlight(summary_span):
    for range in summary_span:
        Retrieved_answer_text.tag_add("highlighted", range[0], range[1])
    highlight_font = font.Font(Retrieved_answer_text, Retrieved_answer_text.cget("font"))
    Retrieved_answer_text.tag_configure("highlighted", font = highlight_font, background="yellow")

def setNoteInput(text):
    Note_text.configure(state='normal')
    Note_text.delete(1.0, 'end')
    Note_text.insert(1.0, text)

def getNoteInput():
    result = Note_text.get(1.0, tk.END+"-1c")
    return result

# Botton commad

def highlight():
    highlight_font = font.Font(Retrieved_answer_text, Retrieved_answer_text.cget("font"))
    Retrieved_answer_text.tag_configure("highlight", font = highlight_font, background='cyan')

    try:
        current_tags = Retrieved_answer_text.tag_names("sel.first")
        if "highlight" in current_tags:
            Retrieved_answer_text.tag_remove("highlight", "sel.first", "sel.last")
        else:
            Retrieved_answer_text.tag_add("highlight", "sel.first", "sel.last")
    except tk.TclError:
        print("未選取文字")

def submit():
    summary = ''
    ranges = Retrieved_answer_text.tag_ranges("highlight")
    for i in range(len(ranges)//2) :
        selected = Retrieved_answer_text.get(ranges[i*2],ranges[i*2+1])
        summary = summary+selected
    setNoteInput(summary)

def reset():
    for tag in Retrieved_answer_text.tag_names():
        Retrieved_answer_text.tag_delete(tag)

def Next_Data(NorP):
    global input_file_dir, number, Original_ques_id, query, Retrieved_article_id, Retrieved_answer, summary, summary_span
    NP = {'N':1, 'P':-1}
    number += NP[NorP]
    if number == total_num.get():
        number = number-1
        messagebox.showinfo(title='恭喜',message="恭喜!標完了!")
    else:
        Original_ques_id, query, Retrieved_article_id, Retrieved_answer, summary, summary_span = getData(number,load_file(input_file_dir))
        
        Number_text.set(str(number+1))
        Original_ques_id_text.set(Original_ques_id)
        setQueryInput(query)
        Retrieved_article_id_text.set(Retrieved_article_id)
        setAnswerInput(Retrieved_answer)
        setAnswerhighlight(summary_span)
        setSummaryInput(summary)
        Note_text.delete(1.0, 'end')
        Informativeness.set('')
        Readability.set('')

        count_data()
        with open(output_file_dir, 'r', encoding='utf-8')as r:
            mark_dataList = json.load(r)
            try:
                setNoteInput(mark_dataList[number]['Note'])
                Informativeness.set(mark_dataList[number]['Informativeness'])
                Readability.set(mark_dataList[number]['Readability'])
                print('已評分')
            except IndexError:
                print('尚未評分')




def pressSaveButton(Info,Read):
    if (Info!='' and Read!='') or (len(getNoteInput())>0):
        with open(output_file_dir, 'r', encoding='utf-8') as r:
            mark_dataList = json.load(r)
            buf={}
            buf['Original_ques_id']= Original_ques_id
            buf['query'] = query
            buf['Retrieved_article_id'] = Retrieved_article_id
            buf['Retrieved_answer'] = Retrieved_answer
            buf['summary'] = summary
            buf['summary_span'] = summary_span
            buf['Informativeness'] = Info
            buf['Readability'] = Read
            buf['Note'] = getNoteInput()

            if checkFileRepeat(mark_dataList):
                mark_dataList[number] = buf
            else:
                mark_dataList.append(buf)
            r.close
        json.dump(mark_dataList, open(output_file_dir, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        del mark_dataList

        # if number+1 == total_num.get():
        #     messagebox.showinfo(title='恭喜',message="標完了")
        # else:
        Next_Data('N')
    else:
        messagebox.showerror(title="有錯喔!!",message="兄弟標一下吧！")
def pressNextButton():
    global number, marked_num #判別是否超過
    marked = marked_num.get()
    if number >= marked:
        messagebox.showerror(title="有錯喔!!",message="別再按下去了:)")
    else:
        Next_Data('N')

def pressPrevButton():
    global number
    if number > 0:
        Next_Data('P')
    else:
        messagebox.showerror(title="有錯喔!!",message="最頂了！")

def count_data():
    with open(output_file_dir, 'r', encoding='utf-8') as r:
        mark_dataList = json.load(r)
        marked_count=0
        for mark_data in mark_dataList:
            marked_count += 1
        
        marked_num.set(marked_count)
        del marked_count
        r.close()


Title_size = 16
Text_size =16

root = tk.Tk()
root.title("摘要評分系統")
app_width = 1100
app_height = 800
# ==============================================================================
if 'Input' not in os.listdir('./'):
    os.mkdir('Input')
if 'Output' not in os.listdir('./'):
    os.mkdir('Output')

input_file_dir = filedialog.askopenfilename(initialdir="./Input")
file_name = input_file_dir.split('/')[-1]
output_file_dir = os.path.join('./Output', file_name.replace('.json', '_name.json'))

# 檢查檔案是否存在
if os.path.isfile(output_file_dir)==False:
    with open(output_file_dir, mode="w",encoding="utf-8")as f:
        json.dump([],f)

with open(output_file_dir, 'r', encoding='utf-8') as r:
    number = len(json.load(r))
    r.close()

total = len(load_file(input_file_dir))
try:
    Original_ques_id, query, Retrieved_article_id, Retrieved_answer, summary, summary_span = getData(number,load_file(input_file_dir))
except:
    if number==total:
        number=0
        Original_ques_id, query, Retrieved_article_id, Retrieved_answer, summary, summary_span = getData(number,load_R1_file(output_file_dir))

# 初始設定值===================
Number_text = tk.StringVar()
Number_text.set(str(number+1))

Original_ques_id_text = tk.StringVar()
Original_ques_id_text.set(Original_ques_id)

Retrieved_article_id_text = tk.StringVar()
Retrieved_article_id_text.set(Retrieved_article_id)

summary_text = tk.StringVar()
summary_text.set(summary)

Informativeness = tk.StringVar()
Readability = tk.StringVar()


# Window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)

root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

# Create Main Frame
content = tk.Frame(root)

# null frame========================
Null_frame = tk.Frame(content, width=50)
Null_frame.grid(column=0, row=0, rowspan=9, sticky='WENS')

# number frame==========
Number_frame = tk.Frame(content)

Number_label = ttk.Label(Number_frame, text = 'Number :', font=('Arial', 20))
Number_label.grid(column=0, row=0)

Number_figure_label = ttk.Label(Number_frame, textvariable=Number_text, font=('Arial', 20))
Number_figure_label.grid(column=1, row=0)

Number_frame.grid(column=1, row=0, sticky='W')

# Original_ques_id frame=================
Original_ques_id_frame = tk.Frame(content)

Original_ques_id_label = ttk.Label(Original_ques_id_frame, text = 'Original_ques_id:', font=('Arial', Title_size))
Original_ques_id_label.grid(column=0, row=0)

Original_ques_id_figure_label = ttk.Label(Original_ques_id_frame,textvariable = Original_ques_id_text , font=('Arial', Title_size))
Original_ques_id_figure_label.grid(column=1, row=0)

Original_ques_id_frame.grid(column=1, row=1, sticky='W')


# Query frame==========
Query_frame = tk.Frame(content, borderwidth=1, relief ='groove', width=200, height=100)

Query_label = ttk.Label(Query_frame, text = 'Query : ', font=('Arial', Title_size))
Query_label.grid(column=0, row=0, sticky='W')

Query_text = tk.Text(Query_frame, 
                    font=('Microsoft JhengHei', Text_size),
                    borderwidth=3,
                    relief='groove',
                    width=80,
                    height=3,
                    state='disabled',
                    spacing2=5
                    )
setQueryInput(query)
Query_text.grid(column=0, row=1)

Query_frame.grid(column=1, row=2)


# Retrieved_article_id frame=================
Retrieved_article_id_frame = tk.Frame(content)

Retrieved_article_id_label = ttk.Label(Retrieved_article_id_frame, text = 'Retrieved_article_id:', font=('Arial', Title_size))
Retrieved_article_id_label.grid(column=0, row=0)

Retrieved_article_id_label = ttk.Label(Retrieved_article_id_frame,textvariable = Retrieved_article_id_text , font=('Arial', Title_size))
Retrieved_article_id_label.grid(column=1, row=0)

Retrieved_article_id_frame.grid(column=1, row=3, sticky='W')


# Retrieved_answer frame==================
Retrieved_answer_frame = ttk.Frame(content, borderwidth=1, relief ='groove')

Retrieved_answer_label = ttk.Label(Retrieved_answer_frame, text = 'Retrieved_answer : ', font=('Arial', Title_size))
Retrieved_answer_label.grid(column=0, row=0, sticky='W')

Retrieved_answer_text= tk.Text(Retrieved_answer_frame,
                    font=('Microsoft JhengHei', Text_size),
                    borderwidth=3,
                    relief='groove',
                    width=80,
                    height=15,
                    undo=True,
                    state='disabled',
                    spacing2=5
                    )
setAnswerInput(Retrieved_answer)
setAnswerhighlight(summary_span)

Retrieved_answer_text.grid(column=0, row=1)

Retrieved_answer_frame.grid(column=1, row=4)

# Summarize buttons frame==============
# Sum_Btn_frame = tk.Frame(Retrieved_answer_frame)

# select_btn = ttk.Button(Sum_Btn_frame, text = "Select", command=highlight)
# select_btn.grid(column=0, row=0)

# submit_btn = ttk.Button(Sum_Btn_frame, text = "Submit", command=submit)
# submit_btn.grid(column=1, row=0)

# reset_btn = ttk.Button(Sum_Btn_frame, text = "Reset", command=reset)
# reset_btn.grid(column=2, row=0)

# Sum_Btn_frame.grid(column=0, row=2)

#Summary frame==================
Summary_frame = ttk.Frame(content, borderwidth=1, relief ='groove')

Summary_label = ttk.Label(Summary_frame, text = 'Summary : ', font=('Arial', Title_size))
Summary_label.grid(column=0, row=0, sticky='W')

Summary_text= tk.Text(Summary_frame,
                    font=('Microsoft JhengHei', Text_size),
                    borderwidth=3,
                    relief='groove',
                    width=80,
                    height=5,
                    undo=True,
                    spacing2=5,
                    state="disabled"
                    )
setSummaryInput(summary)

Summary_text.grid(column=0, row=1)

Summary_frame.grid(column=1, row=5)


# Note frame==================
Note_frame = ttk.Frame(content, borderwidth=1, relief ='groove')

Note_label = ttk.Label(Note_frame, text = 'Note : ', font=('Arial', Title_size))
Note_label.grid(column=0, row=0, sticky='W')

Note_text= tk.Text(Note_frame,
                    font=('Microsoft JhengHei', Text_size),
                    borderwidth=3,
                    relief='groove',
                    width=80,
                    height=2,
                    undo=True,
                    spacing2=5
                    )

Note_text.grid(column=0, row=1)

Note_frame.grid(column=1, row=6, pady=10)

# Buttons frame==============
Buttons_frame = tk.Frame(content)
btn_space_frame = tk.Frame(Buttons_frame, height=20, width=25)
btn_space_frame.grid(column=0, row=0)

Informativeness_lable = ttk.Label(Buttons_frame, text = "Informativeness")
Informativeness_lable.grid(column=1, row=1, sticky="E")

Informativeness_spin = tk.Spinbox(Buttons_frame, from_=0, to=2, width=2, wrap=True, textvariable=Informativeness)
Informativeness_spin.grid(column=2, row=1, sticky='W')
Informativeness.set('')

Readability_lable = ttk.Label(Buttons_frame, text = "Readability")
Readability_lable.grid(column=1, row=2, sticky="E")

Readability_spin = tk.Spinbox(Buttons_frame, from_=0, to=1, width=2, wrap=True, textvariable=Readability)
Readability_spin.grid(column=2, row=2, sticky='W')
Readability.set('')
# Readability_check = ttk.Checkbutton(Buttons_frame, text='Readability', variable=Readability)
# Readability_check.grid(column=0, row=3, padx=20, pady=3,sticky='W')

btn_space2_frame = tk.Frame(Buttons_frame, height=20)
btn_space2_frame.grid(column=0, row=4)

Save_button = ttk.Button(Buttons_frame, text='Save', width=8, command=lambda: pressSaveButton(Informativeness.get(), Readability.get()))
Save_button.grid(column=1, columnspan=2, row=5)

Buttons_frame.grid(column=2, row=5, sticky='WENS')

#next prev 按鈕==============
page_frame = tk.Frame(content)

Next_button = ttk.Button(page_frame, text='Next', command= lambda: pressNextButton())
Next_button.grid(column=1, row=0, padx=3)

Prev_button = ttk.Button(page_frame, text='Prev', command= lambda: pressPrevButton())
Prev_button.grid(column=0, row=0, padx=3)
page_frame.grid(column=2, row=7)

# 資料量統整==================
Data_number_frame = ttk.Frame(content, borderwidth=5, relief='ridge', width=200, height=300)
Data_number_frame.grid(column=2, row=4)
Data_number_frame.columnconfigure(0, weight=2)
Data_number_frame.rowconfigure(0, weight=5)
Data_number_label = ttk.Label(Data_number_frame, text='資料統計',font=('Microsoft JhengHei', 15))
Data_number_label.grid(column=0, columnspan=2, row=0)

total_num = tk.IntVar()
total = len(load_file(input_file_dir))
total_num.set(total)
marked_num = tk.IntVar()

count_data()
Total_label = ttk.Label(Data_number_frame, text='總共 : ')
Total_label.grid(column=0, row=1, sticky='E')
Total_number_label = ttk.Label(Data_number_frame, textvariable=total_num)
Total_number_label.grid(column=1, row=1, sticky='E')

Marked_label = ttk.Label(Data_number_frame, text='已評分 : ')
Marked_label.grid(column=0, row=2, sticky='E')
marked_number_label = ttk.Label(Data_number_frame, textvariable=marked_num)
marked_number_label.grid(column=1, row=2, sticky='E')


content.grid(column=0, row=0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.mainloop()