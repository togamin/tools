import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

#スプレッドシートへの認証情報の設定
CREDENTIALS_FILE = 'config/credentials.json'
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(credentials)

# スプレッドシートを開きワークシートを選択する
spreadsheet = client.open("目標管理シート_togamin")
worksheet = spreadsheet.worksheet("pomodoro")

#スプレッドシートから過去ログを読み込む
def get_past_logs():
    last_row = len(worksheet.col_values(1))
    start_row = max(last_row - 9, 1)
    last_10_rows = worksheet.get_all_values()[start_row-1:last_row]
    return last_10_rows

#スプレッドシートにログを書き込む
def log_activity(status, group, activity):
    worksheet.append_row([datetime.now().strftime("%m/%d"),datetime.now().strftime("%H:%M"), status, group ,activity])

#ポップアップ表示関数
def popup(status,callback):
    #メインウィンドウを作成
    popup_root = tk.Tk()
    popup_root.title("Pomodoro App")
    screen_width = popup_root.winfo_screenwidth()
    screen_height = popup_root.winfo_screenheight()
    window_width = 700
    window_height = 300
    position_right = int(screen_width/2 - window_width/2)
    position_top= int(screen_height/2 - window_height/2)
    popup_root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # 横並びのフレームを作成
    frame = ttk.Frame(popup_root)
    frame.pack(padx=10, pady=10)
    
    # ラベルと入力欄を横並びで作成
    labels = ["グループ:", "内容:"]
    entry_widths = [7, 40]
    entries = []
    for label, width in zip(labels, entry_widths):
        lbl = ttk.Label(frame, text=label)
        lbl.pack(side=tk.LEFT, padx=5)
        
        entry = ttk.Entry(frame, width=width)
        entry.pack(side=tk.LEFT, padx=5)
        entries.append(entry)
    
    # ボタンを追加
    button = ttk.Button(frame, text="OK", command=lambda: on_ok(entries))
    button.pack(pady=10)

    def on_ok(entries):
        group = entries[0].get()
        activity = entries[1].get()
        if activity:
            log_activity(status, group, activity)
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
    columns = [f"#{i+1}" for i in range(len(past_logs[0]))]
    tree = ttk.Treeview(popup_root, columns=columns, show='headings')

    # ヘッダーの設定とカラム幅の設定
    for idx, col in enumerate(worksheet.row_values(1)):
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
    pomodoro_cycle(10000,10000)