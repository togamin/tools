from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import csv

#過去ログの読み込み
def get_past_logs():
    with open('pomodoro.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

#データの追加
def log_activity(status, group, activity, note):
    new_data = [datetime.now().strftime("%m/%d"),datetime.now().strftime("%H:%M"), status, group, activity, note]
    with open('pomodoro.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_data)

#ポップアップ表示関数
def popup(status,callback):
    #メインウィンドウを作成
    popup_root = tk.Tk()
    popup_root.title("Pomodoro App：" + status)
    screen_width = popup_root.winfo_screenwidth()
    screen_height = popup_root.winfo_screenheight()
    window_width = 700
    window_height = 300
    position_right = int(screen_width/2 - window_width/2)
    position_top= int(screen_height/2 - window_height/2)
    popup_root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # 画面上部のフレームの作成
    frame_top = ttk.Frame(popup_root)
    frame_top.pack(padx=3,pady=3,fill=tk.BOTH, expand=True)
    
    # グリッドの列幅を調整
    frame_top.grid_columnconfigure(0, weight=1)
    frame_top.grid_columnconfigure(1, weight=1)
    frame_top.grid_columnconfigure(2, weight=1)
    frame_top.grid_columnconfigure(3, weight=1)

    # グループ
    label_group = ttk.Label(frame_top, text="グループ：")
    label_group.grid(row = 0, column = 0, sticky=tk.W, padx=1, pady=1)
    #グループプルダウン
    options = ["AWS", "作業効率", "暮らし", "組織"]
    selected_option = tk.StringVar()
    dropdown = ttk.Combobox(frame_top, textvariable=selected_option, values=options)
    dropdown.grid(row = 0, column = 1, columnspan=1, sticky=tk.W, padx=1, pady=1)
    
    # 内容
    label_activity = ttk.Label(frame_top, text="内容：")
    entry_activity = ttk.Entry(frame_top)
    label_activity.grid(row = 1, column = 0, sticky=tk.W, padx=1, pady=1)
    entry_activity.grid(row=1, column=1, columnspan=2, sticky=tk.W + tk.E, padx=1, pady=1)

    # note欄作成
    label_note = ttk.Label(frame_top, text="note：")
    entry_note = ttk.Entry(frame_top)
    label_note.grid(row=2, column=0, sticky=tk.W, padx=1, pady=1)
    entry_note.grid(row=2, column=1, columnspan=2, sticky=tk.W + tk.E, padx=1, pady=1)
    
    # ボタンを追加
    button = ttk.Button(frame_top, text="OK", command=lambda: on_ok())
    button.grid(row=2, column=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=1)

    def on_ok():
        group = dropdown.get()
        activity = entry_activity.get()
        note = entry_note.get()
        if activity:
            log_activity(status, group, activity, note)
            messagebox.showinfo("ポモドーロタイマー", "ログが保存されました")
            popup_root.quit()
            popup_root.destroy()
            callback()
        else:
            messagebox.showinfo("ポモドーロタイマー", "作業内容が入力されていません")

    #過去ログ取得
    past_logs = get_past_logs()

    # Treeviewのスタイルを設定
    style = ttk.Style()
    style.theme_use("alt")
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("Treeview", font=("Helvetica", 10), rowheight=25)

    # Treeviewウィジェットの作成
    columns = ["Date", "Time", "Statue", "Group", "Contents", "note"]
    tree = ttk.Treeview(popup_root, columns=columns, show='headings')

    # ヘッダーの設定とカラム幅の設定
    
    for idx, col in enumerate(columns):
        tree.heading(columns[idx], text=col)
        column_widths = [50, 50, 50, 100, 300, 300]
        tree.column(columns[idx], width=column_widths[idx])

    # データの挿入
    for row in past_logs[1:]:
        tree.insert("", tk.END, values=row)

    tree.pack(expand=True, fill='both')

    #イベントループの開始
    popup_root.mainloop()

#ポモドーロサイクル
def pomodoro_cycle(work_time,break_time):
    root = tk.Tk()
    root.withdraw()  # メインウィンドウを隠す
    
    #作業開始のポップアップを表示し、作業時間の計測を開始する関数を呼び出す
    def show_work_popup():
        popup("Goal",start_work)
    #作業時間の計測を開始し、経過後休息開始のポップアップを表示関数を呼び出す
    def start_work():
        print(datetime.now().strftime("%m/%d-%H:%M")+"作業開始")
        root.after(work_time, show_break_popup)  # 作業時間後に休息時間を開始
    #休息開始のポップアップを表示し、休息時間の計測を開始する関数を呼び出す
    def show_break_popup():
        popup("Done",start_break)
    #休息時間の計測を開始し、経過後作業開始のポップアップを表示関数を呼び出す
    def start_break():
        print(datetime.now().strftime("%m/%d-%H:%M")+"休息開始")
        root.after(break_time, show_work_popup)
    show_work_popup()
    root.mainloop()

if __name__ == "__main__":
    work_time = 25
    break_time = 5
    pomodoro_cycle(work_time*1000*60,break_time*1000*60)