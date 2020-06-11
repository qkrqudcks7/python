import tkinter as tk         # tkinter를 tk로 부른다
from tkinter.font import Font  # font 함수를 부른다

class Student():
    def __init__(self, idx=-1, name='', std_id=-1, kor_score=-1, math_score=-1, eng_score=-1):
        self.name = name       # 이름 값
        self.idx = idx         # 각 객체별로 구분하기 위한 id(객체별 구분자겸 순번)
        self.std_id = std_id   # 학번 값
        self.kor_score = kor_score     # 국어 값
        self.math_score = math_score   # 수학 값
        self.eng_score = eng_score     # 영어 값

        self.total_score = self.kor_score + self.math_score + self.eng_score  # 총점 값
        self.mean = float(self.total_score)/3.0    # 평균 값
        self.total_rank = -1     # 총점 랭크 초기화
        self.kor_rank = -1       # 국어점수 랭크 초기화
        self.math_rank = -1      # 수학점수 랭크 초기화
        self.eng_rank = -1       # 영어점수 랭크 초기화

class NotProcessedError(Exception):       # 예외 값 입력하기 위한 클래스 지정
    pass

class StdManager():      # Student 입력, 갱신 , 삭제 키 입력
    def __init__(self):
        self.num_student = 0 # 학생 수 0으로 초기화
        self.std_list = [] # 학생들의 리스트를 저장한다
        self.name_order = []  # 이름 순서
        self.stdid_order = [] # 학번 순서
        self.total_score_order = [] # 총점 순서
        self.kor_order = [] # 국어점수 순서
        self.math_order = [] # 수학점수 순서
        self.eng_order = [] # 영어점수 순서

        self.mean = -1 # 평균점수 초기화
        self.isProcessed = False # 프로그램 실행 과정을 초기화 한다

    def add(self, name, std_id, kor_score, math_score, eng_score):   # 입력 버튼을 출력하기 위한 함수
        res = self.find_by_id(std_id)           # 주어진 학번이 이미 존재하는지 확인
        if self.num_student >=1 and res != None: # 이미 있는 학생수가 1명이상이고 res에 값이 있다면 오류발생
            raise ValueError
        e = Student(self.num_student, name, std_id, kor_score, math_score, eng_score)
        self.std_list.append(e) # 학생 리스트에 e 추가
        self.num_student += 1 # 학생 수 1씩 추가
        self.isProcessed = False # 실행 상태 false

    def update(self, e, name, std_id, kor_score, math_score, eng_score): # 갱신 버튼 출력하는 함수
        if self.num_student < 1:     # 학생수가 1명도 없다면 오류발생
            raise ValueError
        isFound = False    # 갱신 값 초기설정
        for i,x in enumerate(self.std_list):
            if e.std_id == x.std_id:     # add에서 설정한 e값의 std_id랑 std_list내의 x의 std_id값이 같다면
                self.std_list[i].name = name       # 이름, 학번, 국어점수 수학점수 영어점수 총점 평균을 보여준다
                self.std_list[i].std_id = std_id
                self.std_list[i].kor_score = kor_score
                self.std_list[i].math_score = math_score
                self.std_list[i].eng_score = eng_score
                self.std_list[i].total_score = kor_score + math_score + eng_score
                self.std_list[i].mean = float(self.std_list[i].total_score)/3.0
                self.isProcessed = False
                isFound = True      # 갱신 완료를 true로 표현
                break                 # 빠져나간다
        if not isFound:           # 갱신에 실패하면 예외를 불러 일으킨다
            raise ValueError

    def delete(self, idx=-1, stdid = -1):     # 삭제 버튼 출력 함수 idx는 삭제하고자 하는 element의 리스트 인덱스. stdid는 학번
        if idx >=self.num_student: # 주어진 인덱스가 학생수보다 많을 경우 에러 호출
            raise ArithmeticError
        elif self.num_student == 0 or self.std_list[idx].std_id != stdid: # 학생 데이터가 없거나 주어진 학번이 불일치할 경우 에러 호출
            raise ArithmeticError
        else:
            del self.std_list[idx] # 주어진 학생 정보 삭제
            self.num_student -= 1 # 학생수 감소
            self.isProcessed = False # isProcessed flag 성적을 처리했는지 나타냄

            # reorder idx 
            for i,e in enumerate(self.std_list): # 원소 하나 지웠으니 id값이 하나 중간에 비니까 idx를 새로 부여한다.
                e.idx = i

    def find_by_name(self, name):    # 이름으로 찾기
        res = None
        for e in self.std_list:
            if e.name == name:
                res = e
                break
        return res

    def find_by_id(self, id):       # 학번으로 찾기
        res = None
        for e in self.std_list:
            if e.std_id == id:
                res = e
                break
        return res

    # 성적 처리
    def process_grade(self):
        if self.num_student < 1:      # 학생수가 1명도 없다면 오류 발생
            raise ArithmeticError

        # 정렬하기
        self.name_order = sorted(self.std_list, key=lambda e: e.name) # std_list에서 이름으로 정렬하기
        self.stdid_order = sorted(self.std_list, key=lambda e: e.std_id) # std_list에서 학번으로 정렬하기
        self.total_score_order = sorted(self.std_list, key=lambda e: e.total_score) # std_list에서 총점으로 정렬하기
        self.kor_order = sorted(self.std_list, key=lambda e: e.kor_score) # std_list에서 국어점수로 정렬하기
        self.math_order = sorted(self.std_list, key=lambda e: e.math_score) # std_list에서 수학점수로 정렬하기
        self.eng_order = sorted(self.std_list, key=lambda e: e.eng_score) # std_list에서 영어점수로 정렬하기

        # 순위 나타내기
        sum = 0.0 # 합계 0으로 초기화
        for i,e in enumerate(self.total_score_order): # 총점 값으로 반복
            self.std_list[i].total_rank = i  # 학생리스트의 i번째 학생의 토탈 랭크는 i번째
            sum += float(self.std_list[i].total_score) # 전체 총점: 학생 리스트 i의 총합을 sum에 추가
        self.mean = sum / (3.0 * float(self.num_student)) # 전체 평균: 총점/ 과목3개(3.0)*학생수

        for i,e in enumerate(self.kor_order):
            self.std_list[i].kor_rank = i  # i 학생의 국어 랭크는 i 번째

        for i,e in enumerate(self.math_order):
            self.std_list[i].math_rank = i # i 학생의 수학랭크는 i 번째

        for i,e in enumerate(self.eng_order):
            self.std_list[i].eng_rank = i # i 학생의 영어랭크는 i번째

        self.isProcessed = True # 연산처리 ok

    # 이름순, 총점 석차순, 과목별 석차순으로 출력
    def display_rank(self):
        if self.isProcessed == False:  # 연산 과정이 false면 오류발생
            raise NotProcessedError()

class TkManager(tk.Tk): # gui 구축
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("박병찬의 성적처리 프로그램") # 이름
        self.geometry("720x480+150+150") # 해상도 설정
        self.resizable(False, False) #창 크기 고정하기
        base_frame = tk.Frame(self)
        base_frame.pack(side="top", fill="both", expand = True)
        base_frame.grid_rowconfigure(0, weight=1)
        base_frame.grid_columnconfigure(0, weight=1)

        self.ft = Font(family="맑은 고딕", size=12) # 폰트 설정 글자크기 12

        self.std_manager = StdManager() # StdManager 불러오기

        self.frames = {} # 프레임 값 초기화
        for f in (MainFrame, AddFrame, UpdateFrame, DelFrame, DisplayFrame): # 메인, 입력, 갱신, 삭제 출력 프레임 지정
            self.frames[f] = f(base_frame, self, self.ft) # 여러 프레임에도 기본 프레임과 폰트 적용
            self.frames[f].grid(row=0, column=0, sticky="nsew") # 배치 설정

        self.display_frame(MainFrame)

    def display_frame(self, fname):  # 출력 프레임 설정
        if fname == DisplayFrame: # fname을 출력 프레임으로 지정
            df = self.frames[fname] # df로 지정
            df.num = self.std_manager.num_student # 학생 수 지정
            df.mean = self.std_manager.mean # 전체 평균 지정
            df.lname = self.std_manager.name_order # 이름 순서 지정
            df.num_label.config(text="학생수: " +str(self.std_manager.num_student)) # 학생수 라는 라벨을 입력
            df.total_mean_label.config(text="전체평균: " +str(self.std_manager.mean)) # 전체 평균이라는 라벨을 입력
            df.updateTable() # 테이블 업데이트
        self.frames[fname].tkraise() # 프레임이 두개 이상일 경우 다른 창을 맨 앞으로 가져오는 메소드

class MainFrame(tk.Frame): # 메인 화면 구축
    def __init__(self, parent_frame, master, font):
        tk.Frame.__init__(self, parent_frame)
        self.ft = font # 폰트 받아오기
        self.master = master # 이 클래스의 임의의 값 설정

        # 메인 프레임 ui 세팅
        main_label = tk.Label(self, text="성적처리 프로그램 메인화면", font=self.ft).grid(column=1, row=1, columnspan=3)
        #main_label.pack(pady=10, padx=10)

        add_button = tk.Button(self, text="입력", command=lambda: master.display_frame(AddFrame)).grid(column=2, row=3)
        #add_button.pack() 출력 프레임의 입력 프레임을 갖고온다

        update_button = tk.Button(self, text="갱신", command=lambda: master.display_frame(UpdateFrame)).grid(column=2, row=5)
        #update_button.pack() 출력 프레임의 업데이트 프레임을 갖고온다

        del_button = tk.Button(self, text="삭제", command=lambda: master.display_frame(DelFrame)).grid(column=2, row=7)
        #del_button.pack() 출력 프레임의 삭제 프레임을 갖고온다

        del_button = tk.Button(self, text="성적처리", command=lambda: self.send_process()).grid(column=2, row=9)
        #del_button.pack() 연산 과정을 가져온다

        del_button = tk.Button(self, text="출력", command=lambda: self.send_display()).grid(column=2, row=11)
        #del_button.pack() 출력 화면을 가져온다

        self.stat_label = tk.Label(self, text="상태: 정상", font=self.ft) # 상태를 나타내는 라벨
        self.stat_label.grid(column=1, row=12, columnspan=3) # 위치 설정

    def send_process(self): # 연산 과정 가져오는 함수
        try:
            self.master.std_manager.process_grade() # StdManager 클래스의 성적 처리 과정을 가져온다
        except ArithmeticError:
            self.stat_label.config(text="오류: 처리할 데이터가 없습니다") # 값이 없다면 이 라벨을 출력한다
        except KeyError:
            self.stat_label.config(text="오류: ") # 값에 오류가 생기면 이 라벨을 출력한다

    def send_display(self): # 출력 화면을 가져오는 함수
        if self.master.std_manager.isProcessed == False: #StdManager의 isProcessed(연산과정)의 값이 false 라면
            self.stat_label.config(text="오류: 성적처리를 하지 않았습니다") # 이 라벨을 출력한다
            return
        try:
            self.master.display_frame(DisplayFrame)  # display_frame 함수의 값을 가져온다
        except ArithmeticError:
            self.stat_label.config(text="오류: 처리할 데이터가 없습니다") # 값이 없다면 이 라벨을 출력한다
        except KeyError:
            self.stat_label.config(text="오류: ") # 값에 오류가 있다면 이 라벨을 출력한다

class AddFrame(tk.Frame): # 입력 화면 프레임 구축
    def __init__(self, parent_frame, master, font):
        tk.Frame.__init__(self, parent_frame)
        self.ft = font # 폰트 받아오기
        self.master = master # 마스터 객체

        # UI setting
        self.main_label = tk.Label(self, text="학생정보 입력", font=self.ft)  # 라벨 입력하기
        self.main_label.grid(column=1, row=1)  # 라벨 배치
        #self.main_label.pack(pady=10, padx=10)

        self.name = tk.StringVar()  # (이름)인수 설정 ※ String이 들어간다 해서 문자열 아님 주의. StringVar라는 타입의 변수를 대입한다는 의미
        self.stdid = tk.StringVar() # (학번)인수 설정
        self.kor_score = tk.StringVar() # (국어점수)인수 설정
        self.math_score = tk.StringVar() # (수학점수)인수 설정
        self.eng_score = tk.StringVar() # (영어점수)인수 설정

        name_e = tk.Entry(self, width=100, textvariable=self.name)  # 이름 입력칸 배치. textvariable로 변수 이름을 부를 수 있다.
        name_e.grid(column=2, row=2)

        stdid_e = tk.Entry(self, width=100, textvariable=self.stdid) # 학번 입력칸 배치
        stdid_e.grid(column=2, row=3)

        kor_score_e = tk.Entry(self, width=100, textvariable=self.kor_score) # 국어점수 입력칸 배치
        kor_score_e.grid(column=2, row=4)

        math_score_e = tk.Entry(self, width=100, textvariable=self.math_score) # 수학점수 입력칸 배치
        math_score_e.grid(column=2, row=5)

        eng_score_e = tk.Entry(self, width=100, textvariable=self.eng_score) # 영어점수 입력칸 배치
        eng_score_e.grid(column=2, row=6)

        name_l = tk.Label(self, text="이름", font=self.ft).grid(column=1, row=2) # "이름" 라벨 배치
        stdid_l = tk.Label(self, text="학번", font=self.ft).grid(column=1, row=3) # "학번" 라벨 배치
        kor_score_l = tk.Label(self, text="국어점수", font=self.ft).grid(column=1, row=4) # "국어점수" 라벨 배치
        math_score_l = tk.Label(self, text="수학점수", font=self.ft).grid(column=1, row=5) # "수학점수" 라벨 배치
        eng_score_l = tk.Label(self, text="영어점수", font=self.ft).grid(column=1, row=6) # "영어점수" 라벨 배치

        confirm_btn = tk.Button(self, text="입력", command=lambda: self.send()).grid(column=2, row=7, sticky='W') # "입력"키 배치 self.send() 함수를 대입
        back_btn = tk.Button(self, text="메인으로", command=lambda: master.display_frame(MainFrame)).grid(column=1, row=7, sticky='W') # "메인으로" 키 입력 메인프레임 대입

        self.stat_label = tk.Label(self, text="상태: 정상", font=self.ft) # 상태를 나타내는 라벨 입력
        self.stat_label.grid(column=1, row=8, columnspan=2) # 상태 라벨 배치 .columnspan 차지하는 열의 크기를 나타냄

    def send(self, *args):  # 입력 값을 대입하는 함수
        try:
            name = str(self.name.get()) # 이름 입력
            stdid = int(self.stdid.get()) # 학번 입력
            kor_score = float(self.kor_score.get()) # 국어점수 입력
            math_score = float(self.math_score.get()) # 수학점수 입력
            eng_score = float(self.eng_score.get()) # 영어점수 입력

            self.master.std_manager.add(name, stdid, kor_score, math_score, eng_score) # 받아온 값 입력
            self.stat_label.config(text="상태: 정상적으로 입력되었습니다") # 정상입력 되면 이 메세지가 출력된다
        except ValueError:
            self.stat_label.config(text='오류: 입력이 잘못되었습니다.') # 오류가 발생하면 이 메세지가 출력된다

class UpdateFrame(tk.Frame): # 갱신 버튼을 구현한다
    def __init__(self, parent_frame, master, font):
        tk.Frame.__init__(self, parent_frame)
        self.ft = font # 폰트 가져오기
        self.e = None # e 값 가져오기(Student()값)
        self.master = master # tk의 가장 상위값을 마스터로 설정

        # UI setting
        self.main_label = tk.Label(self, text="학생정보 갱신", font=self.ft) # 라벨을 입력한다
        self.main_label.grid(column=1, row=1, columnspan=2) # 라벨 배치
        # 라벨을 입력한다
        desc_label = tk.Label(self, text="입력된 학번 혹은 이름(첫번째 hit)으로 검색하여 정보를 갱신합니다", font=self.ft).grid(column=1, row=2, columnspan=2)
        # 이름으로 검색하는 버튼을 입력한다. search_by_name으로 설정했던 함수를 대입한다
        name_btn = tk.Button(self, text="이름으로 검색", command=lambda: self.search_by_name()).grid(column=1, row=3, sticky='W')
        # 학번으로 검색하는 버튼을 입력한다. search_by_id로 설정했던 함수를 대입한다.
        stdid_btn = tk.Button(self, text="학번으로 검색", command=lambda: self.search_by_id()).grid(column=2, row=3, sticky='W')
        self.name = tk.StringVar() # 이름  인수 설정
        self.stdid = tk.StringVar() # 학번  인수 설정
        self.kor_score = tk.StringVar() # 국어점수 인수 설정
        self.math_score = tk.StringVar() # 수학점수 인수 설정
        self.eng_score = tk.StringVar() # 영어점수 인수 설정

        self.name_e = tk.Entry(self, width=100, textvariable=self.name) # 이름 입력칸을 설정한다
        self.name_e.grid(column=2, row=4) # 이름 입력칸을 배치한다.

        self.stdid_e = tk.Entry(self, width=100, textvariable=self.stdid) # 학번 입력칸을 설정한다
        self.stdid_e.grid(column=2, row=5) # 학번 입력칸을 배치한다

        self.kor_score_e = tk.Entry(self, width=100, textvariable=self.kor_score) # 국어점수 입력칸을 설정한다
        self.kor_score_e.grid(column=2, row=6) # 국어점수 입력칸을 배치한다

        self.math_score_e = tk.Entry(self, width=100, textvariable=self.math_score) # 수학점수 입력칸을 설정한다
        self.math_score_e.grid(column=2, row=7) # 수학점수 입력칸을 배치한다

        self.eng_score_e = tk.Entry(self, width=100, textvariable=self.eng_score) # 영어점수 입력칸을 설정한다
        self.eng_score_e.grid(column=2, row=8) # 영어점수 입력칸을 배치한다

        name_l = tk.Label(self, text="이름", font=self.ft).grid(column=1, row=4) # "이름" 라벨을 입력한다
        stdid_l = tk.Label(self, text="학번", font=self.ft).grid(column=1, row=5) # "학번" 라벨을 입력한다
        kor_score_l = tk.Label(self, text="국어점수", font=self.ft).grid(column=1, row=6) # "국어점수" 라벨을 입력한다
        math_score_l = tk.Label(self, text="수학점수", font=self.ft).grid(column=1, row=7) # "수학점수" 라벨을 입력한다
        eng_score_l = tk.Label(self, text="영어점수", font=self.ft).grid(column=1, row=8) # "영어점수" 라벨을 입력한다

        # "갱신" 버튼 입력 self.send로 설정한 함수를 가져온다
        confirm_btn = tk.Button(self, text="갱신", command=lambda: self.send()).grid(column=2, row=9, sticky='W')
        # "메인으로 돌아가는 버튼 입력" 메인 프레임 화면을 가져온다
        back_btn = tk.Button(self, text="메인으로", command=lambda: master.display_frame(MainFrame)).grid(column=1, row=9, sticky='W')

        self.stat_label = tk.Label(self, text="상태: 정상", font=self.ft) # 상태를 나타내는 라벨을 입력
        self.stat_label.grid(column=1, row=10, columnspan=2) # 라벨 배치 columnspan 차지하는 열의 크기를 나타냄

    def search_by_name(self, *args): # 이름으로 갱신하는 함수 구현. 몇개의 인수를 받을지 모르니 *args를 입력
        name = str(self.name.get()) # self.name 이름 값을 name로 설정
        res = self.master.std_manager.find_by_name(name) # 이름값을 검색한 값을 res로 나타냄
        if res==None: # res에 아무것도 없다면 오류 출력
            self.stat_label.config(text='오류: 검색 결과가 없습니다')
        else: # 검색 값이 있다면
            self.stdid.set(res.std_id) # 검색된 학번 설정
            self.kor_score.set(res.kor_score) # 검색된 국어점수 설정
            self.math_score.set(res.math_score) # 검색된 수학점수 설정
            self.eng_score.set(res.eng_score) # 검색된 영어점수 설정

            self.e = res # e는 이름을 검색한 값
            self.stat_label.config(text="상태: 정상")  # 상태를 나타내는 라벨 출력

    def search_by_id(self, *args): # 학번으로 찾기. 몇개의 인수를 받을지 모르니 *args를 입력
        id = self.stdid.get() # 학번을 받아아 오는 값으로 id를 설정
        if id == '': # id에 아무것도 없다면
            self.stat_label.config(text='오류: 입력이 잘못되었습니다.') # 오류 출력
            return

        res = self.master.std_manager.find_by_id(int(id)) # 위 StdManager 클래스에서 받은 학번 값을 res로 설정
        if res==None: # res에 아무것도 없다면 당연히 검색 결과가 없다는 뜻
            self.stat_label.config(text='오류: 검색 결과가 없습니다')
        else: # res에 값이 있다면
            self.name.set(res.name) # 이름 값 설정
            self.kor_score.set(res.kor_score) # 국어점수 값 설정
            self.math_score.set(res.math_score) # 수학점수 값 설정
            self.eng_score.set(res.eng_score) # 영어점수 값 설정

            self.e = res # 검색결과인 res를 e에 저장
            self.stat_label.config(text="상태: 정상") # 상태 표시 라벨

    def send(self, *args): # 갱신 값 보내는 함수 구축. 인수를 얼마를 받을지 모르니 *args로 가져온다
        try:
            name = str(self.name.get()) # 이름 값 가져오기
            stdid = int(self.stdid.get()) # 학번 값 가져오기
            kor_score = float(self.kor_score.get()) # 국어점수 값 가져오기
            math_score = float(self.math_score.get()) # 수학점수 값 가져오기
            eng_score = float(self.eng_score.get()) # 영어점수 값 가져오기

            # StrManager 클래스의 업데이트 함수 값 가져오기
            self.master.std_manager.update(self.e, name, stdid, kor_score, math_score, eng_score)
            self.stat_label.config(text="상태: 정상적으로 갱신되었습니다") # 정상 출력 라벨 출력하기
        except ValueError:
            self.stat_label.config(text='오류: 입력이 잘못되었습니다.') # 오류가 나면 출력

class DelFrame(tk.Frame): # 삭제 프레임 구축
    def __init__(self, parent_frame, master, font):
        tk.Frame.__init__(self, parent_frame)
        self.ft = font # 폰트 가져오기
        self.e = None # e 값 초기화
        self.master = master # 임의의 마스터값 설정

        # UI setting
        self.main_label = tk.Label(self, text="학생정보 삭제", font=self.ft) # 학생 정보 삭제 라벨 입력
        self.main_label.grid(column=1, row=1, columnspan=2) # 라벨 배치
        # 밑의 라벨을 입력하고 배치한다
        desc_label = tk.Label(self, text="입력된 학번 혹은 이름(첫번째 hit)으로 검색하여 삭제합니다", font=self.ft).grid(column=1, row=2, columnspan=2)
        # "이름으로 검색" 하는 버튼을 출력하고 배치한다
        name_btn = tk.Button(self, text="이름으로 검색", command=lambda: self.search_by_name()).grid(column=1, row=3, sticky='W')
        # "학번으로 검색" 하는 버튼을 출력하고 배치한다
        stdid_btn = tk.Button(self, text="학번으로 검색", command=lambda: self.search_by_id()).grid(column=2, row=3, sticky='W')
        self.name = tk.StringVar() # 이름 입력 인수 입력
        self.stdid = tk.StringVar() # 학번 입력 인수 입력
        self.kor_score = tk.StringVar() # 국어점수 인수 입력
        self.math_score = tk.StringVar() # 수학점수 인수 입력
        self.eng_score = tk.StringVar() # 영어점수 인수 입력

        self.name_e = tk.Entry(self, width=100, textvariable=self.name) # 이름 입력칸 설정
        self.name_e.grid(column=2, row=4) # 이름 입력칸 배치

        self.stdid_e = tk.Entry(self, width=100, textvariable=self.stdid) # 학번 입력칸 설정
        self.stdid_e.grid(column=2, row=5) # 학번 입력칸 배치

        self.kor_score_e = tk.Entry(self, width=100, textvariable=self.kor_score) # 국어점수 입력칸 설정
        self.kor_score_e.grid(column=2, row=6) # 국어점수 입력칸 배치

        self.math_score_e = tk.Entry(self, width=100, textvariable=self.math_score) # 수학점수 입력칸 설정
        self.math_score_e.grid(column=2, row=7) # 수학점수 입력칸 배치

        self.eng_score_e = tk.Entry(self, width=100, textvariable=self.eng_score) # 영어점수 입력칸 설정
        self.eng_score_e.grid(column=2, row=8) # 영어점수 입력칸 배치

        name_l = tk.Label(self, text="이름", font=self.ft).grid(column=1, row=4) # "이름" 라벨 배치
        stdid_l = tk.Label(self, text="학번", font=self.ft).grid(column=1, row=5) # "학번" 라벨 배치
        kor_score_l = tk.Label(self, text="국어점수", font=self.ft).grid(column=1, row=6) # "국어점수" 라벨 배치
        math_score_l = tk.Label(self, text="수학점수", font=self.ft).grid(column=1, row=7) # "수학점수" 라벨 배치
        eng_score_l = tk.Label(self, text="영어점수", font=self.ft).grid(column=1, row=8) # "영어점수" 라벨 배치

        # "삭제" 버튼 추가 self.send 함수 대입
        confirm_btn = tk.Button(self, text="삭제", command=lambda: self.send()).grid(column=2, row=9, sticky='W')
        # "메인으로" 버튼 추가 메인 프레임 화면을 가져온다.
        back_btn = tk.Button(self, text="메인으로", command=lambda: master.display_frame(MainFrame)).grid(column=1, row=9, sticky='W')

        self.stat_label = tk.Label(self, text="상태: 정상", font=self.ft) # 상태를 출력하는 라벨을 추가
        self.stat_label.grid(column=1, row=10, columnspan=2) # 라벨 배치

    def search_by_name(self, *args): # 이름으로 찾는 버튼을 구현하기 위한 함수. 얼마나 인수를 추가할지 몰라 *args로 입력
        name = str(self.name.get()) # 이름 값 가져오기 name으로 설정
        res = self.master.std_manager.find_by_name(name) # 이름 값을 검색한 값을 res로 나타냄
        if res==None: # res에 아무것도 없다면 오류 출력
            self.stat_label.config(text='오류: 검색 결과가 없습니다')
        else: # res에 값이 있다면
            self.stdid.set(res.std_id) # 학번 값 가져오기
            self.kor_score.set(res.kor_score) # 국어점수 값 가져오기
            self.math_score.set(res.math_score) # 수학점수 값 가져오기
            self.eng_score.set(res.eng_score) # 영어점수 값 가져오기

            self.e = res # res를 e값으로 대입
            self.stat_label.config(text="상태: 정상") # 상태를 출력하는 라벨 추가

    def search_by_id(self, *args): # 학번으로 찾는 버튼을 구현하기 위한 함수. 얼마나 인수를 추가할지 몰라 *args로 입력
        id = self.stdid.get() # 학번값 가져오기 id로 설정
        if id == '': # 만약 id에 값이 없다면
            self.stat_label.config(text='오류: 입력이 잘못되었습니다.') # 오류 발생
            return

        res = self.master.std_manager.find_by_id(int(id)) # id값을 검색한 값을 res로 설정
        if res==None: # res값에 아무것도 없다면
            self.stat_label.config(text='오류: 검색 결과가 없습니다') # 오류 발생
        else: # res 값이 있다면
            self.name.set(res.name) # 이름 값 가져오가
            self.kor_score.set(res.kor_score) # 국어점수 값 가져오기
            self.math_score.set(res.math_score) # 수학점수 값 가져오기
            self.eng_score.set(res.eng_score) # 영어점수 값 가져오기

            self.e = res # res를 e에 대입
            self.stat_label.config(text="상태: 정상") # 상태 출력 라벨 추가하기

    def send(self, *args): # 삭제키를 위한 함수 구축
        if self.e == None: # e에 아무것도 없다면
            self.stat_label.config(text='오류: 입력이 잘못되었습니다.') # 오류 발생
            return
        try: # 학번 값을 저장
            stdid = int(self.stdid.get())
            self.master.std_manager.delete(self.e.idx, stdid) # StdManager 클래스의 삭제 함수를 가동
            self.stat_label.config(text="상태: 정상적으로 삭제되었습니다") # 삭제 성공시 출력
        except ValueError: # 삭제 값을 잘못 입력시 출력
            self.stat_label.config(text='오류: 입력이 잘못되었습니다.')
        except ArithmeticError: # 학생 정보가 없을 시 출력
            self.stat_label.config(text='오류: 학생정보가 존재하지 않습니다')

class DisplayFrame(tk.Frame): # 출력 프레임 구축
    def __init__(self, parent_frame, master, font):
        tk.Frame.__init__(self, parent_frame)
        self.ft = font # 폰트 받아오기
        self.e = None # e값 초기화
        self.master = master # 마스터 값 설정
        self.order = 0 # 0: ascending order, 1: descending order

        # UI setting
        # 메인으로 돌아가는 버튼 설정, 배치 , 메인프레임을 보여줌으로써 화면으로 돌아간다
        back_btn = tk.Button(self, text="메인으로", command=lambda: master.display_frame(MainFrame)).grid(column=1, row=1, sticky='W')
        self.main_label = tk.Label(self, text="학생정보출력", font=self.ft) # 학생 정보 출력이라는 라벨을 출력
        self.main_label.grid(column=3, row=2, columnspan=3) # 라벨 배치

        self.stat_label = tk.Label(self, text="상태: 정상", font=self.ft) # 상태를 나타내는 라벨을 출력
        self.stat_label.grid(column=1, row=3, columnspan=7) # 라벨 배치

        self.num = master.std_manager.num_student # 전체 학생 수를 나타낸다
        self.mean = master.std_manager.mean # 전체 평균을 나타낸다

        self.num_label = tk.Label(self, text="학생수: " +str(self.num), font=self.ft) # (학생수: 전체학생수 값) 이렇게 나타낸다 위에 설정한 num값을 대입
        self.num_label.grid(column=1, row=4, columnspan=2) # 학생수 라벨 배치
        self.total_mean_label = tk.Label(self, text="전체평균: " +str(self.mean), font=self.ft) # (전체평균: 전체평균 값) 이렇게 나타낸다 위에 설정한 mean 값을 대입함
        self.total_mean_label.grid(column=4, row=4, columnspan=2) # 전체 평균 라벨 배치

        self.lname = self.master.std_manager.name_order # StdManager의 name_order 값을 가져와 대입한다.
        # "이름 순서" 버튼을 추가한다. StrManager의 name_order 값을 가지고 업데이트 한다. 즉 이름 순서대로 출려한다
        name_btn = tk.Button(self, text="이름순서", command=lambda: self.updateTable(lname=self.master.std_manager.name_order)).grid(column=1, row=5, sticky='W')
        # "학번 순서" 버튼을 추가한다. StrManager의 stdid_order 값을 가지고 업데이트 한다. 즉 학번 순서대로 출려한다
        id_btn = tk.Button(self, text="학번순서", command=lambda: self.updateTable(lname=self.master.std_manager.stdid_order)).grid(column=2, row=5, sticky='W')
        # "총점 순서" 버튼을 추가한다. StrManager의 total_score_order 값을 가지고 업데이트 한다. 즉 총점 순서대로 출려한다
        total_btn = tk.Button(self, text="총점순서", command=lambda: self.updateTable(lname=self.master.std_manager.total_score_order)).grid(column=3, row=5, sticky='W')
        # "국어점수 순서" 버튼을 추가한다. StrManager의 kor_order 값을 가지고 업데이트 한다. 즉 국어점수 순서대로 출려한다
        kor_btn = tk.Button(self, text="국어점수", command=lambda: self.updateTable(lname=self.master.std_manager.kor_order)).grid(column=4, row=5, sticky='W')
        # "수학점수 순서" 버튼을 추가한다. StrManager의 math_order 값을 가지고 업데이트 한다. 즉 수학점수 순서대로 출려한다
        math_btn = tk.Button(self, text="수학점수", command=lambda: self.updateTable(lname=self.master.std_manager.math_order)).grid(column=5, row=5, sticky='W')
        # "영어점수 순서" 버튼을 추가한다. StrManager의 eng_order 값을 가지고 업데이트 한다. 즉 영어점수 순서대로 출려한다
        eng_btn = tk.Button(self, text="영어점수", command=lambda: self.updateTable(lname=self.master.std_manager.eng_order)).grid(column=6, row=5, sticky='W')

        self.max = tk.StringVar() # 최대 출력할 수 있는 값을 설정한다
        # "최대 출력수" 라벨을 추가한다.
        max_label = tk.Label(self, text="최대 출력수:", font=self.ft).grid(column=2, row=6, columnspan=2)
        max_e = tk.Entry(self, width=6, textvariable=self.max) # 출력값을 보여주는 창을 표시한다
        max_e.grid(column=4, row=6) # 창을 배치한다
        self.max.set(10) # 최대치를 10으로 설정
        # 오름차순 버튼을 배치한다. 오름차 값=0 으로 줘서 업데이트 시킨다.
        asc_btn = tk.Button(self, text="오름차", command=lambda: self.updateTable(order=0)).grid(column=6, row=6, sticky='W')
        # 내림차순 버튼을 배친한다. 내림차 값=1로 줘서 업데이트 시킨다.
        dsc_btn = tk.Button(self, text="내림차", command=lambda: self.updateTable(order=1)).grid(column=7, row=6, sticky='W')

        # 헤더 부분 출력
        self.name_label = tk.Label(self, text="이름", font=self.ft).grid(column=1, row=7) # 이름 라벨 출력
        self.id_label = tk.Label(self, text="학번", font=self.ft).grid(column=2, row=7) # 학번 라벨 출력
        self.total_label = tk.Label(self, text="총점", font=self.ft).grid(column=3, row=7) # 총점 라벨 출력
        self.mean_label = tk.Label(self, text="평균", font=self.ft).grid(column=4, row=7) # 평균 라벨 출력
        self.kor_label = tk.Label(self, text="국어", font=self.ft).grid(column=5, row=7) # 국어점수 라벨 출력
        self.math_label = tk.Label(self, text="수학", font=self.ft).grid(column=6, row=7) # 수학점수 라벨 출력
        self.eng_label = tk.Label(self, text="영어", font=self.ft).grid(column=7, row=7) # 영어점수 라벨 출력

        self.nlist = [] # 이름 리스트 생성
        self.ilist = [] # 학번 리스트 생성
        self.tlist = [] # 총점 리스트 생성
        self.mlist = [] # 평균 리스트 생성
        self.klist = [] # 국어점수 리스트 생성
        self.malist = [] # 수학점수 리스트 생성
        self.elist = [] # 영어점수 리스트 생성

        self.updateTable() # updateTable 가동

    # 순서 재정렬하여 GUI에 출력
    # lname: 정렬기준이 되는 객체 리스트
    # order: 정렬방식 (0: 오름차, 1: 내림차)
    def updateTable(self, lname=None, order=-1):
        # update properties
        max_i = -1 # 최대 인덱스값 -1로 초기화
        try:
            max_i = int(self.max.get()) # 출력 max값 가져오기
        except ValueError: # max값에 문제가 있는 경우 오류 문구 출력
            self.stat_label.config(text='오류: 입력이 잘못되었습니다.')

        if lname != None:
            self.lname = lname # self.lname값 업데이트
        if order != -1: # 올바른 order값인지 체크
            self.order = order
        order = self.order

        # remove previous widgets
        for i in range(len(self.nlist)):
            self.nlist[i].destroy() # 이름 리스트 객체 삭제
            self.ilist[i].destroy() # 학번 리스트 객체 삭제
            self.tlist[i].destroy() # 총점 리스트 객체 삭제
            self.mlist[i].destroy() # 평균 리스트 객체 삭제
            self.klist[i].destroy() #  국어점수 리스트 객체 삭제
            self.malist[i].destroy() # 수학점수 리스트 객체 삭제
            self.elist[i].destroy() # 영어점수 리스트 객체 삭제

        # table contents
        idx = 0 # idx 변수 0으로 초기화
        max_i = min(max_i, self.num) # 최대 i값 구하기
        for i in range(max_i): # max_i까지 반복문

            if order == 0: # ascending order로 처리
                idx = i
            elif order == 1: # descending order로 처리
                idx = max_i-1-i # idx 값이 루프 진행하면서 max_i-1 에서 0 으로 감소하도록
            e = self.lname[idx] # 주어진 인덱스의 객체 가져오기
            rowi = 8+i # 행 인덱스

            # 갱신된 이름 위젯 리스트 생성
            l = tk.Label(self, text=e.name, font=self.ft) # 새로운 Label 위젯 생성
            l.grid(column=1, row=rowi) # grid 포맷으로 설정
            self.nlist.append(l) # 새로 생성된 Label 위젯을 nlist에 추가

            # 갱신된 학번 위젯 리스트 생성
            l = tk.Label(self, text=e.std_id, font=self.ft) # 새로운 Label 위젯 생성
            l.grid(column=2, row=rowi) # grid 포맷으로 설정
            self.ilist.append(l) # 새로 생성된 Label 위젯을 ilist에 추가

            # 갱신된 총점 위젯 리스트 생성
            l = tk.Label(self, text=e.total_score, font=self.ft) # 새로운 Label 위젯 생성
            l.grid(column=3, row=rowi) # grid 포맷으로 설정
            self.tlist.append(l) # 새로 생성된 Label 위젯을 tlist에 추가

            # 갱신된 평균 위젯 리스트 생성
            l = tk.Label(self, text=e.mean, font=self.ft) # 새로운 Label 위젯 생성
            l.grid(column=4, row=rowi) # grid 포맷으로 설정
            self.mlist.append(l) # 새로 생성된 Label 위젯을 mlist에 추가

            # 갱신된 국어점수 위젯 리스트 생성
            l = tk.Label(self, text=e.kor_score, font=self.ft) # 새로운 Label 위젯 생성
            l.grid(column=5, row=rowi) # grid 포맷으로 설정
            self.klist.append(l) # 새로 생성된 Label 위젯을 klist에 추가

            # 갱신된 수학점수 위젯 리스트 생성
            l = tk.Label(self, text=e.math_score, font=self.ft) # 새로운 Label 위젯 생성
            l.grid(column=6, row=rowi) # grid 포맷으로 설정
            self.malist.append(l) # 새로 생성된 Label 위젯을 malist에 추가

            # 갱신된 영어점수 위젯 리스트 생성
            l = tk.Label(self, text=e.eng_score, font=self.ft) # 새로운 Label 위젯 생성
            l.grid(column=7, row=rowi) # grid 포맷으로 설정
            self.elist.append(l) # 새로 생성된 Label 위젯을 elist에 추가

        self.stat_label.config(text="상태: 정상적으로 입력되었습니다")



if __name__ == '__main__': # 해당 스크립트를 메인 프로그램으로 돌리는지 체크하는 내용입니다
    app = TkManager()
    app.mainloop()
