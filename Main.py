# -*- coding: utf-8 -*-
import random
from tkinter import *
import tkinter.messagebox

from SudokuUtil import CheckSudoku


class SudokuGUI:
    level = 1
    count = 0
    def __init__(self):
        # 프레임 생성
        self.window = Tk()
        self.window.title("SUDOKU")
        # 스도쿠 판 생성
        self.numberMap = CheckSudoku().grid
        
        # 모니터 사이즈
        ScreenSizeX = self.window.winfo_screenwidth() 
        ScreenSizeY = self.window.winfo_screenheight() 
        # 프레임 사이즈
        FrameSizeX = 210
        FrameSizeY = 300
        # 프레임 위치
        FramePosX = (ScreenSizeX - FrameSizeX) / 2
        FramePosY = (ScreenSizeY - FrameSizeY) / 2
        # 프레임 위치 설정
        self.window.geometry("%sx%s+%s+%s" % (FrameSizeX, FrameSizeY, int(FramePosX), int(FramePosY)))
        self.window.minsize(FrameSizeX, FrameSizeY)
        self.window.maxsize(FrameSizeX, FrameSizeY)
       
        # 메뉴바 생성
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        configMenu = Menu(menubar, tearoff=0)
        helpMenu = Menu(menubar, tearoff=0)
        
        menubar.add_cascade(label="난이도", menu=configMenu)
        menubar.add_cascade(label="도움말", menu=helpMenu)
        menubar.add_command(label="모범답안",command=self.printAnswer)
        menubar.add_command(label="종료", command=self.window.destroy)
        
        configMenu.add_command(label="초보", command=self.setLevelEasy)
        configMenu.add_command(label="보통", command=self.setLevelNormal)
        configMenu.add_command(label="지옥", command=self.setLevelHard)
        
        helpMenu.add_command(label="힌트", command=self.printHint)
        helpMenu.add_command(label="도움말", command=self.helpMessage)
        
        
        self.frame = Frame(self.window)
        self.frame.pack()
        
        self.stringLevel = StringVar()
        self.label = Label(self.window, textvariable=self.stringLevel).pack()
        

        # 배열과 Entry들 생성
        self.cells = []
        self.entrys = []
        for i in range(9):
            self.cells.append([])
            for j in range(9):
                self.cells[i].append(StringVar())
        # Entry 생성 및 배열과 연결
        for i in range(9):
            self.entrys.append([])
            for j in range(9):  # DISABLED, NORMAL
                t = Entry(self.frame, cursor="top_left_arrow", state=DISABLED, bd=3, width=2, textvariable=self.cells[i][j], \
                        justify=RIGHT)
                t.grid(row=i, column=j)
                self.entrys[i].append(t)
                self.cells[i][j].set(self.numberMap[i][j])  # 초기값 지정
                
        # 버튼과 메모장
        self.memoString = StringVar()
        
        self.btn1 = Button(self.window, text="검사", command=self.validate).pack(side=BOTTOM)
        self.btnframe = Frame(self.window).pack(side=BOTTOM)
        Label(self.btnframe, text=" ").pack(side=LEFT)
        Label(self.btnframe, text=" ").pack(side=RIGHT)
        
        self.memo = Entry(self.btnframe, bg="light cyan", cursor="right_side", justify=CENTER, textvariable=self.memoString).pack(side=LEFT)
        self.btn2 = Button(self.btnframe, text="  C  ", bd=4, command=self.memoClear).pack(side=RIGHT)
        
        self.memoString.set("메모장")

        # 초기 난이도 설정
        self.setLevelEasy()
        
        
        self.window.mainloop()
      
    # 스도쿠 단계별 맵 설정 메서드
    def setLevelMapping(self, level=1):
        self.count=0
        for i in range(9):
            for j in range(9):
                self.cells[i][j].set(self.numberMap[i][j])  # 스도쿠 맵 전체 재생성
                self.entrys[i][j].config(state=DISABLED)  # 스도쿠 맵 전체 비활성화
                randomNumber = random.randint(0, level)  # 확률용 숫자 생성
                if(level == 1):
                    if(j % 2 == 0 and randomNumber != 0):
                        self.count+=1
                        self.cells[i][j].set("")
                        self.entrys[i][j].config(state=NORMAL)
                elif(level == 2):
                    if(i % 2 == 0 and randomNumber != 0):
                        self.count+=1
                        self.cells[i][j].set("")
                        self.entrys[i][j].config(state=NORMAL)
                else:
                    if(randomNumber != 0):
                        self.count+=1
                        self.cells[i][j].set("")
                        self.entrys[i][j].config(state=NORMAL)
                                
    def setLevelEasy(self):
        self.level = 1
        self.setLevelMapping(self.level)
        self.stringLevel.set("난이도 : 초보 [빈칸 : "+str(self.count)+"개]")
        
        
    def setLevelNormal(self):
        self.level = 2
        self.setLevelMapping(self.level)
        self.stringLevel.set("난이도 : 보통 [빈칸 : "+str(self.count)+"개]")
        
    def setLevelHard(self):
        self.level = 3
        self.setLevelMapping(self.level)
        self.stringLevel.set("난이도 : 지옥 [빈칸 : "+str(self.count)+"개]")
        
    def printHint(self):
        line = random.randint(0, 8)
        lineString = " "
        for j in range(9):
            lineString= str(lineString) + str(self.numberMap[line][j])+" "
        tkinter.messagebox.showinfo("랜덤 힌트!", str(line+1) + "번째 줄\n[" + str(lineString) + "]")
    
    def memoClear(self):
        self.memoString.set("")
    # 콘솔창에 답지를 출력하는 메서드
    def printAnswer(self):    
        answerString="          "
        for i in range(9):  # 답지
            for j in range(9):
                answerString = answerString + str(self.numberMap[i][j]) + " "
                print(self.numberMap[i][j], end=" ")
            answerString = answerString + "\n          "
            print()
        print("------------------") 
        
        
        tkinter.messagebox.showinfo("모범답안","*답은 여러개가 존재 할 수 있습니다*\n\n"+answerString)
   
    
    def helpMessage(self):
        helpString = """
        스도쿠란 3x3, 가로, 세로에 각각 1~9까지의 
        숫자만 쓰여있는 판에 빈칸을 만들어서
        그 빈칸을 채우는 게임입니다.
        
        난이도는 초보, 보통, 지옥이 제공되며
        어려우시다면 힌트를 보시는 것을 추천드립니다.
        
                                    Made by Jiwon_Kim
        """
        tkinter.messagebox.showinfo("도움말", helpString) 
        
          
    def validate(self):
        try:
            values = [[eval(x.get()) for x in self.cells[i] if x != []] for i in range(9)]            
            self.numberMap = values;
            print(values)
            check = CheckSudoku()
            if check.isValid(values):
                self.memoString.set("")
                tkinter.messagebox.showinfo("스도쿠 풀이 검사", "정답입니다!")
#                 self.window.quit()
            else :
                tkinter.messagebox.showinfo("스도쿠 풀이 검사", "틀렸습니다. 다시 해보세요!")
                
        except(Exception):
            tkinter.messagebox.showinfo("스도쿠 풀이 검사", "빈공간이 있습니다.")
            
            
if (__name__ == "__main__"):
    a = SudokuGUI()    
