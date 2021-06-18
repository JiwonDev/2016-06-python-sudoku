# -*- coding:utf-8 -*-
import random


class CheckSudoku:
    sudokuBack = []

    def __init__(self):

        # 기본seed값
        for i in range(0, 9):
            self.sudokuBack.append([])
            for j in range(0, 9):
                self.sudokuBack[i].append(0)

        self.grid = self.makeSudoku()
        self.checkgrid = self.isValid(self.grid)

    def insertNum(self, inX=0, inY=0):
        # 넣을 숫자를 생성하고 섞는다
        line = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(line)

        # line에서 넣을 수 없는 숫자를 0으로 변경한다.
        # sudokuBack의 값과 비교하여 넣을수 없는 값은 0으로 바꾼다.
        # sudokuBack의 가로 0~9, 세로0~9, 가로세로3x3값들과 비교
        for i in range(0, 9):
            for j in range(0, 9):
                if (line[i] == self.sudokuBack[inX][j]):  # 세로 0~9비교
                    line[i] = 0
                    break
                if (line[i] == self.sudokuBack[j][inY]):  # 가로 0~9비교
                    line[i] = 0
                    break

        for y in range(0, 3):
            for x in range(0, 3):
                for i in range(0, 9):  # 3x3 칸 비교
                    if (line[i] == self.sudokuBack[x + (inX // 3) * 3][y + (inY // 3) * 3]):
                        line[i] = 0

        for i in range(0, 9):
            if (line[i] != 0):  # 되는 숫자가 있다면 넣고 True를 반환한다.
                self.sudokuBack[inX][inY] = line[i];
                return True
        return False  # 전부 안된다면 False를 반환한다.

    def makeSudoku(self):
        x, y = 0, 0  # step[1] back을 0으로 초기화한다
        while x < 9:
            y = 0
            while y < 9:
                if self.sudokuBack[x][y] != 0:  # 이미 값이 있다면 넘어간다.
                    pass
                elif self.insertNum(x, y):
                    pass  # 넣을 수 있는 숫자가 없다면 다른 숫자를 변경시킨다.
                else:
                    inputCheck = False  # 숫자를 넣을 수 없다.

                    y = y - 1  # y를 1감소시킨다.(한칸이동)
                    if y < 0:  # 0을 넘어가면 한줄올린다.(오른쪽위로)
                        y = 8
                        x = x - 1
                    if x < 0: break;

                    while (not inputCheck):  # (반복)숫자를 넣을 수 없다면 이전 블록을 수정한다.
                        # 이전 칸에 +1을한다
                        self.sudokuBack[x][y] += 1
                        # 더 했는데 9를 넘었다면 현재 값을 지우고
                        # 이전 블록으로 또 이동한다.
                        if (self.sudokuBack[x][y] > 9):
                            self.sudokuBack[x][y] = 0
                            y = y - 1
                            if (y < 0):
                                y = 8
                                x = x - 1
                            # 실패했다면 x=0으로 한 뒤 재시도한다.
                            if (x < 0):
                                break
                        else:
                            # 0~9사이라면 넣을 수 있는 값인지 체크한다.
                            inputCheck = self.checkNum(x, y)
                y = y + 1
            x = x + 1
        return self.sudokuBack

    def checkNum(self, inX, inY):
        for i in range(0, 9):
            # 세로줄에 중복되는 숫자가 있다면
            if (inY != i):
                if (self.sudokuBack[inX][inY] == self.sudokuBack[inX][i]):
                    return False
        for i in range(0, 9):
            # 가로줄에 중복되는 숫자가 있다면
            if (inX != i):
                if (self.sudokuBack[inX][inY] == self.sudokuBack[i][inY]):
                    return False
            # 3x3 확인
            for y in range(0, 3):
                for x in range(0, 3):
                    if (inX != x + (inX // 3) * 3 and inY != y + (inY // 3) * 3):
                        if (self.sudokuBack[inX][inY] == self.sudokuBack[x + (inX // 3) * 3][y + (inY // 3) * 3]):
                            return False
        return True

    # 풀이가 유효한지 검사한다.
    def isValid(self, grid):
        for i in range(9):
            for j in range(9):
                # 1~9까지의 숫자인지 + 가로,세로,3x3 검사
                if grid[i][j] < 1 or grid[i][j] > 9\
                        or not self.isValidAt(i, j, grid):
                    return False

        return True

    # 그리드에서 grid[i][j]가 유효한지 검사한다.
    def isValidAt(self, i, j, grid):
        # i번 행에서 grid[i][j]가 유효한지 검사한다.
        for column in range(9):
            if column != j and grid[i][column] == grid[i][j]:
                return False

        # j번 행에서 grid[i][j]가 유효한지 검사한다.
        for row in range(9):
            if row != i and grid[row][j] == grid[i][j]:
                return False

        # 3x3에서 grid[i][j]가 유효한지 검사한다.   
        for row in range((i // 3) * 3, (i // 3) * 3 + 3):
            for col in range((j // 3) * 3, (j // 3) * 3 + 3):
                if row != i and col != j and\
                        grid[row][col] == grid[i][j]:
                    return False
        return True
