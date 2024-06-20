import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
print("pomodoro_timer")

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

if __name__ == "__main__":
    print(get_past_logs())
    log_activity("Done", "作業効率", "GitのIssueテンプレートの作成")