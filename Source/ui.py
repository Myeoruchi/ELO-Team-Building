import base64
import random
import threading
import tkinter as tk
from tkinter import simpledialog, PhotoImage, ttk, scrolledtext
from itertools import combinations

import excel
import image

VERSION = 'v0.1'
icon_base64 = image.get_image()
icon_data = base64.b64decode(icon_base64)

class App:
    def __init__(self, root):
        self.root = root
        self.sum = [0] * 10
        self.cnt = [0] * 10

        # 타이틀
        root.title(f"Test {VERSION}")

        # 창 크기 고정
        root.geometry("400x400")
        root.resizable(False, False)

        # Team Frame 생성
        team1_frame = tk.Frame(root)
        team1_frame.grid(row=0, column=0)
        team2_frame = tk.Frame(root)
        team2_frame.grid(row=0, column=1)
        
        # Team 텍스트
        team1_title = tk.Label(team1_frame, text="Attack", font=("Arial", 14, "bold"), fg="red")
        team1_title.grid(row=0, column=0, columnspan=2, pady=10)
        team2_title = tk.Label(team2_frame, text="Defense", font=("Arial", 14, "bold"), fg="blue")
        team2_title.grid(row=0, column=0, columnspan=2, pady=10)

        # 플레이어 리스트 및 ELO 레이팅 표시
        self.player_box = []
        self.elo_label = []
        self.elo_average = []
        for j in range(2):
            for i in range(5):
                if j == 0:
                    combo = ttk.Combobox(team1_frame, state="readonly", justify="right", width=10)
                    combo.bind("<<ComboboxSelected>>", self.combobox_select_event)
                    combo.grid(row=i+1, column=j)
                    elo = tk.Label(team1_frame, text="       ")
                    elo.grid(row=i+1, column=j+1, padx=10)
                else:
                    combo = ttk.Combobox(team2_frame, state="readonly", width=10)
                    combo.bind("<<ComboboxSelected>>", self.combobox_select_event)
                    combo.grid(row=i+1, column=j)
                    elo = tk.Label(team2_frame, text="       ")
                    elo.grid(row=i+1, column=j-1, padx=10)
                self.player_box.append(combo)
                self.elo_label.append(elo)
            
            if j == 0:
                elo_aver = tk.Label(team1_frame, font=("Arial", 12, "bold"), fg="red")
                elo_aver.grid(row=6, column=1)
            else:
                elo_aver = tk.Label(team2_frame, font=("Arial", 12, "bold"), fg="blue")
                elo_aver.grid(row=6, column=0)
            self.elo_average.append(elo_aver)

        # Button Frame 생성
        button_frame = tk.Frame(root)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # 신규 등록 버튼
        new_player_button = ttk.Button(button_frame, text="신규 등록", command=self.add_new_player)
        new_player_button.grid(row=0, column=0, padx=20)

        # 팀 섞기 버튼
        team_button = ttk.Button(button_frame, text="팀 섞기", command=self.team_shuffle)
        team_button.grid(row=0, column=1, padx=20)

        # 결과 입력 버튼
        update_button = ttk.Button(button_frame, text="결과 입력")
        update_button.grid(row=0, column=2, padx=20)

        # 로그창
        self.log_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD, state="disabled")
        self.log_text.grid(row=2, column=0, columnspan=2, pady=10)

        # weight 설정
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.update_combobox()

    def combobox_select_event(self, event):
        self.update_elo_ui(event)

    def update_elo_ui(self, event):
        def func():
            elo = excel.get_elo(event.widget.get())
            idx = self.player_box.index(event.widget)
            
            self.elo_label[idx].config(text=str(elo))
            self.sum[idx] = elo
            self.cnt[idx] = 1

            group_idx = idx // 5
            total_sum = 0
            total_cnt = 0
            for i in range(group_idx * 5, (group_idx + 1) * 5):
                total_sum += self.sum[i]
                total_cnt += self.cnt[i]

            self.elo_average[group_idx].config(text=str(int(total_sum / total_cnt)))

        threading.Thread(target=func, daemon=True).start()

    def update_ui(self, team):
        self.sum = [0] * 10
        self.cnt = [0] * 10

        for player_box in self.player_box:
            player_box.set('')
        for elo_label in self.elo_label:
            elo_label.config(text='')
        for elo_average in self.elo_average:
            elo_average.config(text="       ")

        for team_idx, players in enumerate(team):
            start_idx = team_idx * 5
            for idx, player in enumerate(players):
                player_idx = start_idx + idx
                self.player_box[player_idx].set(player)
                elo = excel.get_elo(player)
                self.elo_label[player_idx].config(text=str(elo))
                self.sum[player_idx] = elo
                self.cnt[player_idx] = 1

        for idx in range(2):
            total_sum = 0
            total_cnt = 0
            for i in range(idx * 5, (idx + 1) * 5):
                total_sum += self.sum[i]
                total_cnt += self.cnt[i]
            self.elo_average[idx].config(text=str(int(total_sum / total_cnt)))

    def update_combobox(self):
        data = sorted(excel.get_player_list())
        for combobox in self.player_box:
            combobox.config(values=data)

    def add_new_player(self):
        info = simpledialog.askstring("신규 등록", "닉네임과 ELO를 다음과 같은 형식으로 입력하세요.\nex. 가나다, 1500")
        if info == None:
            self.log("신규 등록 취소")
            return
        try:
                name, elo = info.split(',')
        except:
            self.log("입력 형식이 잘못되었습니다.")

        def func():
            if excel.add_new_player(name, elo) is True:
                self.log(f"[{name}, {elo}] - 신규 등록이 완료되었습니다.")
                self.update_combobox()
            else:
                self.log("이미 존재하는 닉네임입니다.")
                return
            
        threading.Thread(target=func, daemon=True).start()
        
    def team_shuffle(self):
        scope = simpledialog.askfloat("팀 섞기", "ELO 평균 차이의 최댓값을 입력해주세요.")
        if scope == None:
            self.log("팀 섞기 취소")
            return
        
        players = list(set(player.get() for player in self.player_box if player.get() != ''))
        if len(players) % 2 == 1:
            self.log("인원수가 짝수가 아닙니다.")
            return

        def func():
            all_combinations = list(combinations(players, len(players) // 2))
            valid_combinations = []

            for team1 in all_combinations:
                team2 = [player for player in players if player not in team1]

                team1_avg = sum(excel.get_elo(player) for player in team1) / len(team1)
                team2_avg = sum(excel.get_elo(player) for player in team2) / len(team2)

                diff = abs(team1_avg - team2_avg)
                if diff <= scope:
                    valid_combinations.append((team1, team2, diff))
                    valid_combinations.append((team2, team1, diff))

            if not valid_combinations:
                self.log("조건에 맞는 팀 조합이 없습니다.")
                return
            
            best_combination = random.choice(valid_combinations)
            team1, team2, min_diff = best_combination

            self.update_ui((team1, team2))
            self.log(f"팀 섞기 완료.\n평균 ELO 차이 : {min_diff:.2f}")
        
        threading.Thread(target=func, daemon=True).start()
    
    def log(self, message):
        """로그 메시지를 출력하는 함수"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    icon_image = PhotoImage(data=icon_data)
    root.iconphoto(True, icon_image)
    app = App(root)
    root.mainloop()