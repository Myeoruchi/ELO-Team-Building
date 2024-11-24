import os
import time
import json
import base64
import subprocess
import threading
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, PhotoImage, ttk, scrolledtext
import pandas as pd
from urllib.parse import urlparse, parse_qs

SEGMENT_DURATION = 2.28
VERSION = 'v2.3'
settings_file = 'settings.json'

class App:
    def __init__(self, root):
        self.root = root

        # 타이틀
        root.title(f"Test {VERSION}")

        # 창 크기 고정
        root.geometry("600x400")
        root.resizable(False, False)
        
        # weight 설정
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Team Frame 생성
        team1_frame = tk.Frame(root)
        team1_frame.grid(row=0, column=0)
        team2_frame = tk.Frame(root)
        team2_frame.grid(row=0, column=1)
        
        # Team 텍스트
        team1_title = tk.Label(team1_frame, text="Team 1")
        team1_title.grid(row=0, column=0, columnspan=2, pady=10)
        team2_title = tk.Label(team2_frame, text="Team 2")
        team2_title.grid(row=0, column=0, columnspan=2, pady=10)

        # 플레이어 리스트 및 ELO 레이팅 표시
        data = ["Apple", "Banana", "Cherry", "Date"]
        self.player_box = []
        self.elo_label = []
        self.elo_average = []
        for j in range(2):
            for i in range(5):
                if j == 0:
                    combo = ttk.Combobox(team1_frame, values=data, state="readonly")
                    combo.grid(row=i+1, column=j, padx=25)
                    elo = tk.Label(team1_frame)
                    elo.grid(row=i+1, column=j+1)
                else:
                    combo = ttk.Combobox(team2_frame, values=data, state="readonly")
                    combo.grid(row=i+1, column=j, padx=25)
                    elo = tk.Label(team2_frame)
                    elo.grid(row=i+1, column=j-1)
                self.player_box.append(combo)
                self.elo_label.append(elo)
            
            if j == 0:
                elo_aver = tk.Label(team1_frame)
                elo_aver.grid(row=6, column=1)
            else:
                elo_aver = tk.Label(team2_frame)
                elo_aver.grid(row=6, column=0)
            self.elo_average.append(elo_aver)

        # Button Frame 생성
        button_frame = tk.Frame(root)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        #신규 플레이어 버튼
        new_player_button = ttk.Button(button_frame, text="신규 등록")
        new_player_button.grid(row=0, column=0, padx=30)

        #팀 섞기 버튼
        team_button = ttk.Button(button_frame, text="팀 섞기")
        team_button.grid(row=0, column=1, padx=30)

        #결과 입력 버튼
        update_button = ttk.Button(button_frame, text="결과 입력")
        update_button.grid(row=0, column=2, padx=30)

        # 로그창
        self.log_text = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD, state="disabled")
        self.log_text.grid(row=2, column=0, columnspan=2, pady=10)

        # # 경로 앞 텍스트
        # self.text_filepath = tk.Label(self.path_frame, text="엑셀 파일 경로")
        # self.text_filepath.grid(row=0, column=0, padx=10, pady=10)

        # # 엑셀 경로를 표시할 Entry 위젯
        # self.excel_path = tk.Entry(self.path_frame, width=50,relief="solid")
        # self.excel_path.grid(row=0, column=1, padx=10, pady=10)

        # # 파일 경로 지정 버튼
        # self.button_browse = tk.Button(self.path_frame, text="파일 선택", command=lambda: self.browse_path(0, self.excel_path))
        # self.button_browse.grid(row=0, column=2, padx=10, pady=10)

        # # 경로 앞 텍스트
        # self.text_filepath = tk.Label(self.path_frame, text="원본 음원 저장 경로")
        # self.text_filepath.grid(row=1, column=0, padx=10, pady=10)

        # # 엑셀 경로를 표시할 Entry 위젯
        # self.download_path = tk.Entry(self.path_frame, width=50, relief="solid")
        # self.download_path.grid(row=1, column=1, padx=10, pady=10)

        # # 파일 경로 지정 버튼
        # self.button_browse = tk.Button(self.path_frame, text="폴더 선택", command=lambda: self.browse_path(1, self.download_path))
        # self.button_browse.grid(row=1, column=2, padx=10, pady=10)

        # # 경로 앞 텍스트
        # self.text_filepath = tk.Label(self.path_frame, text="자른 음원 저장 경로")
        # self.text_filepath.grid(row=2, column=0, padx=10, pady=10)

        # # 엑셀 경로를 표시할 Entry 위젯
        # self.cut_path = tk.Entry(self.path_frame, width=50, relief="solid")
        # self.cut_path.grid(row=2, column=1, padx=10, pady=10)

        # # 파일 경로 지정 버튼
        # self.button_browse = tk.Button(self.path_frame, text="폴더 선택", command=lambda: self.browse_path(2, self.cut_path))
        # self.button_browse.grid(row=2, column=2, padx=10, pady=10)

        # # 버튼을 넣을 Frame을 생성
        # self.button_frame = tk.Frame(root)
        # self.button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # # 음원 다운로드 버튼
        # self.button_download = tk.Button(self.button_frame, text="음원 다운로드", width=15, command=self.music_download)
        # self.button_download.grid(row=3, column=0, padx=10, pady=10)

        # # 음원 자르기
        # self.button_cut = tk.Button(self.button_frame, text="음원 볼륨 조절 및 자르기", width=20, command=self.music_cut)
        # self.button_cut.grid(row=3, column=1, padx=10, pady=10)

        # # 정보 추출 버튼
        # self.button_extract = tk.Button(self.button_frame, text="정보 추출", width=15, command=self.extract_info)
        # self.button_extract.grid(row=3, column=2, padx=10, pady=10)

        # # 로그창
        # self.log_text = tk.Text(root, height=10, wrap=tk.WORD, state="disabled")
        # self.log_text.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # # 스크롤바 생성
        # self.yscrollbar = tk.Scrollbar(root, orient="vertical", command=self.log_text.yview)
        # self.yscrollbar.grid(row=4, column=4, sticky='ns')

        # # 스크롤바 연결
        # self.log_text.config(yscrollcommand=self.yscrollbar.set)

        # # 행과 열의 가중치 설정 (상대적 크기 조정을 위해 필요)
        # root.grid_rowconfigure(4, weight=1)
        # root.grid_columnconfigure(0, weight=1)

        # 경로 불러오기
        if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    path = json.load(f)
                    try:
                        self.excel_path.insert(0, path['0'])
                        self.excel_path.xview(tk.END)
                    except:
                        pass

                    try:
                        self.download_path.insert(0, path['1'])
                        self.download_path.xview(tk.END)
                    except:
                        pass
                    
                    try:
                        self.cut_path.insert(0, path['2'])
                        self.cut_path.xview(tk.END)
                    except:
                        pass
    
    def extract_video_id(self, url):
            if 'youtu.be' in url:
                parsed_url = urlparse(url)
                video_id = parsed_url.path.strip('/')
                return video_id if len(video_id) == 11 else None
            
            elif 'youtube.com' in url:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                video_id = query_params.get('v', [None])[0]
                return video_id if len(video_id) == 11 else None
            
            return None

    def browse_path(self, folder, path):
        if folder:
            selectpath = filedialog.askdirectory()
        else:
            selectpath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

        if selectpath:
            path.delete(0, tk.END)  # 기존 경로 삭제
            path.insert(0, selectpath)  # 경로 삽입
            path.xview(tk.END) # 끝으로 스크롤

            settings = {}
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
            settings[f'{folder}'] = selectpath
            with open(settings_file, 'w') as f:
                json.dump(settings, f)

    def music_download(self):
        """음원을 다운로드 하는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return
        if not self.download_path.get():
            messagebox.showerror("에러", "원본 음원 저장 경로를 선택해주세요.")
            return
        os.makedirs(self.download_path.get(), exist_ok=True)

        sleep = simpledialog.askfloat("간격 설정기", "차단을 막기 위한 다운로드 간격 설정입니다.\n초 단위이므로 적당히 경험에 따라 조절해주세요.", parent=root)
        if sleep == None:
            self.log("다운로드 작업 취소")
            return
        
        def download():
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. ({e})")
                return

            musicNum = len(df)
            success = 0
            fail = 0
            skip = 0
            unused = 0
        
        thread = threading.Thread(target=download)
        thread.start()

    def music_cut(self):
        """음원을 자르는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return
        if not self.download_path.get():
            messagebox.showerror("에러", "원본 음원 저장 경로를 선택해주세요.")
            return
        if not self.cut_path.get():
            messagebox.showerror("에러", "자른 음원 저장 경로를 선택해주세요.")
            return
        os.makedirs(self.download_path.get(), exist_ok=True)
        os.makedirs(self.cut_path.get(), exist_ok=True)

        vol = simpledialog.askfloat("볼륨 설정기", "설정할 볼륨을 입력하세요.\n추천값 : 93.0±", parent=root)
        if not vol:
            self.log("볼륨 조절 / 자르기 작업 취소")
            return
        vol -= 89.0

        quality = simpledialog.askfloat("음질 설정기", "설정할 음질을 입력하세요. (1~10, 추천 값 : 4)\n클수록 음질이 높아집니다.", parent=root)
        if not quality:
            self.log("볼륨 조절 / 자르기 작업 취소")
            return

        def cut():
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. ({e})")
                return

            subprocess.run(f'del /s /f /q "{self.cut_path.get()}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW, check=True)

            musicNum = len(df)
            success = 0
            fail = 0
            unused = 0
            op = 0
            end = 0
            for idx, row in df.iterrows():
                if pd.notna(row['미사용']):
                    self.log(f'볼륨 조절 / 자르기 스킵 : {idx+1:03}행 (미사용)')
                    unused += 1
                    continue

                empty = []
                if pd.isna(row['Addr']):
                    empty.append('Addr')
                if pd.isna(row['Start']):
                    empty.append('Start')
                if pd.isna(row['End']):
                    empty.append('End')

                if empty:
                    empty_list = ', '.join(empty)
                    self.log(f'볼륨 조절 / 자르기 실패 : {idx+1:03}행 (공백 : {empty_list})')
                    fail += 1
                    continue

                try:
                    video_id = self.extract_video_id(row['Addr'])
                    if video_id:
                        downloaded_file = os.path.join(self.download_path.get(), f'{video_id}.mp3')
                    else:
                        downloaded_file = row['Addr']

                    if os.path.exists(downloaded_file):
                        if pd.notna(row['오프닝/엔딩']):
                            if row['오프닝/엔딩'] == '오프닝':
                                path = self.cut_path.get() + '/OP'
                                op += 1
                            else:
                                path = self.cut_path.get() + '/ED'
                                end += 1
                        else:
                            path = self.cut_path.get() + f'/{idx+1-unused-op-end:03}'
                        os.makedirs(path, exist_ok=True)
                        output_file = path + '/cut.mp3'

                        command = [
                            'ffmpeg',
                            '-ss', str(row['Start']),
                            '-to', str(row['End']),
                            '-i', downloaded_file,
                            '-reset_timestamps', '1',
                            '-c:a', 'libmp3lame',
                            '-q:a', '0',
                            '-ar', '44100',
                            '-ac', '2',
                            '-b:a', '320k',
                            output_file
                        ]
                        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True)

                        command = ['mp3gain', '-c', '-r', '-d', str(vol), output_file]
                        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True)
                        
                        command = [
                            'ffmpeg',
                            '-i', output_file,
                            '-f', 'segment',
                            '-segment_time', str(SEGMENT_DURATION),
                            '-reset_timestamps', '1',
                            '-c:a', 'libvorbis',
                            '-q:a', str(quality),
                            path + '/%03d.ogg'
                        ]
                        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True)

                        self.log(f'볼륨 조절 / 자르기 성공 : {idx+1:03}행')
                        success += 1
                    else:
                        self.log(f'볼륨 조절 / 자르기 실패 : {idx+1:03}행 (파일 없음)')
                        fail += 1
                        continue

                except Exception as e:
                    self.log(f'볼륨 조절 / 자르기 실패 : {idx+1:03}행 ({e})')
                    fail += 1

            subprocess.run(f'del /s /f /q "{self.cut_path.get()}\\*.mp3"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW, check=True)

            with open(f'{self.cut_path.get()}/info.txt', 'w', encoding='utf-8') as f:
                if fail:
                    f.write('fail')
                else:
                    f.write(f'{musicNum-unused-op-end}\n{op}\n{end}')
            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {unused}개 미사용 했습니다.')
            self.log(f'{op+end}개의 곡이 오프닝/엔딩 곡으로 사용됐습니다.')
        
        thread = threading.Thread(target=cut)
        thread.start()

    def extract_info(self):
        """맵에 들어갈 정보를 파일로 출력하는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return

        def extract():            
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. : ({e})")
                return

            CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
            musicNum = len(df)
            categoryNum = 0
            categoryInclude = []
            categoryName = []
            categoryIndex = []
            hint = 'const hintArr1 = ['
            chosung = 'const hintArr2 = ['
            artist = 'const artArr = ['
            answer_list = 'const ansArr = ['
            answer_count = 'const indexArr = ['
            music_length = 'const lenArr = ['

            def extract_chosung(text):
                result = []
                for char in text:
                    if '가' <= char <= '힣':  # 한글 유니코드 범위 안에 있는 경우
                        char_code = ord(char) - 0xAC00
                        chosung_index = char_code // (21 * 28)
                        result.append(CHOSUNG_LIST[chosung_index])
                    else:
                        result.append(char)  # 한글이 아닌 경우 그대로 추가
                return ''.join(result)

            musicNum = len(df)
            success = 0
            fail = 0
            unused = 0
            opend = 0
            for idx, row in df.iterrows():
                try:
                    if pd.notna(row['미사용']):
                        self.log(f'추출 스킵 : {idx+1:03}행 (미사용)')
                        unused += 1
                        continue
                    
                    if pd.notna(row['오프닝/엔딩']):
                        self.log(f'추출 스킵 : {idx+1:03}행 (오프닝/엔딩)')
                        opend += 1
                        continue
                    
                    empty = []
                    if pd.isna(row['범주']):
                        empty.append('범주')
                    if pd.isna(row['힌트1']):
                        empty.append('힌트1')
                    if pd.isna(row['가수']):
                        empty.append('가수')
                    if pd.isna(row['제목']):
                        empty.append('제목')
                    if pd.isna(row['Start']):
                        empty.append('Start')
                    if pd.isna(row['End']):
                        empty.append('End')
                    if pd.isna(row['정답 리스트1']):
                        empty.append('정답 리스트1')
                    
                    if empty:
                        empty_list = ', '.join(empty)
                        self.log(f'추출 실패 : {idx+1:03}행 (공백 : {empty_list})')
                        
                    if row['범주'] in categoryName:
                        index = categoryName.index(row['범주'])
                        categoryIndex.append(index)
                        categoryInclude[index] += 1
                    else:
                        categoryName.append(row['범주'])
                        categoryIndex.append(categoryNum)
                        categoryInclude.append(1)
                        categoryNum += 1

                    hint += f'EPD(Db("{row["힌트1"]}")), '
                    artist += f'EPD(Db("{row["가수"]} - {row["제목"]}")), '

                    count = 0
                    answers = row['정답 리스트1'].split(',')  # ,로 구분된 정답 분리
                    count += len(answers)

                    if pd.notna(row['정답 리스트2']):
                        answers += row['정답 리스트2'].split(',')
                    count += len(answers) << 0x8
                        
                    answer_db_format = ', '.join([f'Db("{answer.strip()}")' for answer in answers])
                    answer_list += f'[{answer_db_format}], '

                    first_answer = answers[0].strip()
                    cho = extract_chosung(first_answer)
                    chosung += f'EPD(Db("{cho}")), '

                    answer_count += f'{count}, '
                    music_length += f'{int(row["End"] - row["Start"])}, '

                    self.log(f'추출 성공 : {idx+1:03}행')
                    success += 1

                except Exception as e:
                    self.log(f'추출 실패 : {idx+1:03}행 ({e})')
                    fail += 1
                    return

            with open(f'{os.path.dirname(self.excel_path.get())}/src/musicInfo.eps', 'w', encoding='utf-8') as outfile:
                outfile.write(f'const musicNumMax = {musicNum-unused-opend};\n')
                outfile.write(f'const categoryNum = {categoryNum};\n')

                outfile.write('const categoryActive = EUDArray(categoryNum);\n') 

                outfile.write('const categoryInclude = [')
                for i in range(len(categoryInclude)-1):
                    outfile.write(f'{categoryInclude[i]}, ')
                outfile.write(f'{categoryInclude[-1]}];\n')

                outfile.write('const categoryName = [')
                for i in range(len(categoryName)-1):
                    outfile.write(f'EPD(Db("{categoryName[i]}")), ')
                outfile.write(f'EPD(Db("{categoryName[-1]}"))];\n')

                outfile.write('const categoryIndex = [')
                for i in range(len(categoryIndex)-1):
                    outfile.write(f'{categoryIndex[i]}, ')
                outfile.write(f'{categoryIndex[-1]}];\n')
                
                outfile.write(f'{music_length[:-2]}];\n')
                outfile.write(f'{answer_count[:-2]}];\n')
                outfile.write(f'{answer_list[:-2]}];\n')
                outfile.write(f'{artist[:-2]}];\n')
                outfile.write(f'{hint[:-2]}];\n')
                outfile.write(f'{chosung[:-2]}];\n')

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, 미사용 {unused}개, 오프닝/엔딩 {opend}개를 스킵했습니다.')
        
        thread = threading.Thread(target=extract)
        thread.start()
    
    def log(self, message):
        """로그 메시지를 출력하는 함수"""
        self.log_text.config(state="normal")  # Text 위젯을 수정 가능 상태로 변경
        self.log_text.insert(tk.END, message + "\n")  # 메시지 삽입
        self.log_text.yview(tk.END)  # 자동으로 최신 로그로 스크롤
        self.log_text.config(state="disabled")  # 수정 불가능 상태로 설정

# Tkinter 윈도우 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

# # 메인 윈도우 생성
# root = tk.Tk()
# root.title("Dropdown List UI")
# root.geometry("300x400")  # 창 크기 설1

# # 메인 프레임 생성
# frame = tk.Frame(root, bd=2, relief="solid")
# frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# # 드롭다운 리스트 옵션 (예제 리스트)
# options = ["Option 1", "Option 2", "Option 3"]

# # 드롭다운 리스트 생성
# dropdowns = []
# for row in range(5):  # 5행
#     for col in range(2):  # 2열
#         selected_option = tk.StringVar()  # 선택된 값 저장용 변수
#         selected_option.set("Select")  # 초기값 설정

#         # Combobox 생성
#         dropdown = ttk.Combobox(frame, textvariable=selected_option, values=options, state="readonly", width = 10)
#         dropdown.grid(row=row, column=col, padx=5, pady=5, ipadx=5, ipady=5)
#         dropdowns.append(selected_option)

# # Tkinter 이벤트 루프 실행
# root.mainloop()
