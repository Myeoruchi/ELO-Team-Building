import tkinter as tk
from tkinter import messagebox
from itertools import combinations

# 팀 간 Elo 점수 차이를 최소화하는 함수
def balance_teams(players):
    # 가능한 모든 조합 중 절반만 고려 (Team 1)
    all_combinations = list(combinations(players, len(players) // 2))
    min_diff = float('inf')
    best_combination = None

    for team1 in all_combinations:
        team2 = [player for player in players if player not in team1]

        # Elo 평균 계산
        team1_avg = sum(player["rating"] for player in team1) / len(team1)
        team2_avg = sum(player["rating"] for player in team2) / len(team2)

        # 평균 차이 계산
        diff = abs(team1_avg - team2_avg)

        # 최소 차이를 기록
        if diff < min_diff:
            min_diff = diff
            best_combination = (team1, team2)

    return best_combination, min_diff

def process_input():
    players = []
    for i in range(10):
        name = name_entries[i].get().strip()
        rating = rating_entries[i].get().strip()

        if name and rating.isdigit():
            players.append({"name": name, "rating": int(rating)})
        else:
            messagebox.showerror("입력 오류", f"올바르지 않은 데이터: {name}, {rating}")
            return

    # Elo 점수 기준으로 팀 간 차이를 최소화하면서 팀 구성
    best_combination, elo_difference = balance_teams(players)

    # 결과 텍스트 구성
    result = "1팀:\n"
    for player in best_combination[0]:
        result += f"{player['name']} - ELO: {player['rating']}\n"
    
    result += "\n2팀:\n"
    for player in best_combination[1]:
        result += f"{player['name']} - ELO: {player['rating']}\n"
    
    result += f"\nElo 차이: {elo_difference:.2f}"

    # 결과 창 생성
    result_window = tk.Toplevel(root)
    result_window.title("팀 구성 결과")
    result_window.geometry("400x400")  # 창 크기 설정
    result_window.resizable(False, False)

    # 결과 텍스트 라벨 추가
    result_label = tk.Label(result_window, text=result, font=("Arial", 14), justify="left")
    result_label.pack(padx=20, pady=20)

# GUI 창 생성
root = tk.Tk()
root.title("내전 팀 짜기")

# 창 크기 설정
root.geometry("440x320")

root.resizable(False, False)

# 창 크기에 맞게 행과 열 크기 비율 설정
root.grid_rowconfigure(0, weight=1)  # 첫 번째 행(타이틀)에 비율을 1로 설정
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)
root.grid_rowconfigure(8, weight=1)
root.grid_rowconfigure(9, weight=1)
root.grid_rowconfigure(10, weight=1)
root.grid_rowconfigure(11, weight=1)  # 마지막 행(버튼)에 비율을 1로 설정

name_entries = []
rating_entries = []

# 이름과 ELO 입력 필드 10개 생성
for i in range(10):
    # 이름 입력 필드
    name_label = tk.Label(root, text=f"Player {i+1} 이름:")
    name_label.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
    name_entry = tk.Entry(root, width=20)
    name_entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
    name_entries.append(name_entry)

    # ELO 입력 필드
    rating_label = tk.Label(root, text=f"Player {i+1} ELO:")
    rating_label.grid(row=i, column=2, sticky="ew", padx=5, pady=5)
    rating_entry = tk.Entry(root, width=10)
    rating_entry.grid(row=i, column=3, sticky="ew", padx=5, pady=5)
    rating_entries.append(rating_entry)

# 결과 보기 버튼
process_button = tk.Button(root, text="결과 보기", command=process_input)
process_button.grid(row=10, column=0, columnspan=4, pady=10)

# 프로그램 실행
root.mainloop()
