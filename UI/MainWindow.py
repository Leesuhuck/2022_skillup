# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
from PIL import Image
from UI.ImageView import ImageViewer
from UI.exsel_create import Ui_exsel_create
import sys
import time
import math
import os

from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
from Database.DB import DBManager

print(os.getcwd())

class Ui_MainWindow(QMainWindow, DBManager):
    def __init__(self):
        super().__init__()
        self.all_RadioList = []
        self.pass_RadioList = []
        self.fail_RadioList = []
        self.nt_RadioList = []
        self.na_RadioList = []
        self.nl_RadioList = []
        self.pre_idx = ""
        self.idx = ""
        self.button = ""
        self.result = {}
        self.EC = Ui_exsel_create()
        self.setupUi()
        self.cliced_lang = None

    def setupUi(self):
        self.widget = QWidget()
        self.resize(1472, 900)
        self.setWindowTitle("다국어 자동화")
        self.setWindowIcon(QIcon("web-removebg-preview.png"))

        # 전체 화면 배치
        self.horizontalLayout = QHBoxLayout(self.widget)

        # 좌측 이미지 리스트
        self.img_scrollArea = QScrollArea()
        self.img_scrollArea.setWidgetResizable(True)
        self.img_scrollArea.setFixedWidth(90)
    
        self.img_scrollAreaWidgetContents = QWidget()
        self.img_VBoxLayout = QVBoxLayout(self.img_scrollAreaWidgetContents)
        self.img_VBoxLayout.setAlignment(Qt.AlignTop)

        self.img_scrollArea.setWidget(self.img_scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.img_scrollArea)

        # 우측 큰 이미지
        self.right_VBoxLayout = QVBoxLayout()

        self.img_Label = QLabel()
        self.img_Label.setMinimumSize(1350, 600)
        self.img_Label.setStyleSheet("color: gray;"
                             "border-style: solid;"
                             "border-width: 1px;"
                             "border-color: #747474;"
                             "border-radius: 1px")

        self.right_VBoxLayout.addWidget(self.img_Label)

        # 필드 세팅
        self.field_gridLayout = QGridLayout()
        self.set_field()

        self.right_VBoxLayout.addLayout(self.field_gridLayout)

        # 평가 목록, all pass, fail
        self.bottom_HBoxLayout = QHBoxLayout()

        self.Tgroupbox = QGroupBox("평가 목록")
        self.Tgroupbox.setMinimumWidth(1000)
        self.Tgroupbox.setFixedHeight(200)
        self.testList_Layout = QHBoxLayout()
        self.Tgroupbox.setLayout(self.testList_Layout)

        self.setWidget_func()

        self.bottom_HBoxLayout.addWidget(self.Tgroupbox)

        # ALL PASS, ALL FAIL, ALL N/T, ALL N/A
        self.all_groupbox = QGroupBox("ALL")
        self.all_groupbox.setFixedHeight(200)
        self.testAll_VBoxLayout = QVBoxLayout()
        self.allPass_RadioButton = QPushButton("ALL PASS")
        self.allFail_RadioButton = QPushButton("ALL FAIL")
        self.allNT_RadioButton = QPushButton("ALL N/T")
        self.allNA_RadioButton = QPushButton("ALL N/A")
        self.allNull_RadioButton = QPushButton("ALL NULL")
        self.testAll_VBoxLayout.addWidget(self.allPass_RadioButton)
        self.testAll_VBoxLayout.addSpacing(5)
        self.testAll_VBoxLayout.addWidget(self.allFail_RadioButton)
        self.testAll_VBoxLayout.addSpacing(5)
        self.testAll_VBoxLayout.addWidget(self.allNT_RadioButton)
        self.testAll_VBoxLayout.addSpacing(5)
        self.testAll_VBoxLayout.addWidget(self.allNA_RadioButton)
        self.testAll_VBoxLayout.addSpacing(5)
        self.testAll_VBoxLayout.addWidget(self.allNull_RadioButton)
        self.testAll_VBoxLayout.setAlignment(Qt.AlignCenter)

        self.allPass_RadioButton.clicked.connect(self.allPass_clicked)
        self.allFail_RadioButton.clicked.connect(self.allFail_clicked)
        self.allNT_RadioButton.clicked.connect(self.allNT_clicked)
        self.allNA_RadioButton.clicked.connect(self.allNA_clicked)
        self.allNull_RadioButton.clicked.connect(self.allNull_clicked)
        self.all_groupbox.setLayout(self.testAll_VBoxLayout)
        self.bottom_HBoxLayout.addWidget(self.all_groupbox)

        self.version_groupbox = QGroupBox("버전 정보")
        self.version_groupbox.setMinimumWidth(200)
        self.version_groupbox.setFixedHeight(200)
        self.version_VBoxLayout = QVBoxLayout()
        self.version_textEdit = QTextEdit()
        self.version_VBoxLayout.addWidget(self.version_textEdit)
        self.version_groupbox.setLayout(self.version_VBoxLayout)
        self.bottom_HBoxLayout.addWidget(self.version_groupbox)

        self.result_groupbox = QGroupBox("진행 상황")
        self.result_groupbox.setFixedHeight(200)
        self.result_Layout = QVBoxLayout()
        self.null_lbl = QLabel("미평가:")
        self.pass_lbl = QLabel("PASS:")
        self.fail_lbl = QLabel("FAIL:")
        self.nt_lbl = QLabel("N/T:")
        self.na_lbl = QLabel("N/A:")
        self.result_Layout.addWidget(self.null_lbl)
        self.result_Layout.addWidget(self.pass_lbl)
        self.result_Layout.addWidget(self.fail_lbl)
        self.result_Layout.addWidget(self.nt_lbl)
        self.result_Layout.addWidget(self.na_lbl)
        self.result_groupbox.setLayout(self.result_Layout)

        self.bottom_HBoxLayout.addWidget(self.result_groupbox)

        self.right_VBoxLayout.addLayout(self.bottom_HBoxLayout)
        self.horizontalLayout.addLayout(self.right_VBoxLayout)

        # 메뉴바
        self.menubar = self.menuBar()
        self.menu = self.menubar.addMenu("Menu")
        self.menu.aboutToShow.connect(self.update_open_menu)

        self.setup = self.menubar.addMenu("Setup")
        self.actionLanguage = QAction("Language", self)
        self.actionField = QAction("Field", self)
        self.actionTest_List = QAction("Test List", self)
        self.actionExcel_Setting = QAction("Excel Setting", self)
        self.setup.addAction(self.actionLanguage)
        self.setup.addAction(self.actionField)
        self.setup.addAction(self.actionTest_List)
        self.setup.addAction(self.actionExcel_Setting)

        # 상태바
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.setCentralWidget(self.widget)

    def allPass_clicked(self):
        for pass_radio in self.pass_RadioList:
            pass_radio.setChecked(True)

    def allFail_clicked(self):
        for fail_radio in self.fail_RadioList:
            fail_radio.setChecked(True)

    def allNT_clicked(self):
        for nt_radio in self.nt_RadioList:
            nt_radio.setChecked(True)

    def allNA_clicked(self):
        for na_Radio in self.na_RadioList:
            na_Radio.setChecked(True)

    def allNull_clicked(self):
        for nl_radio in self.nl_RadioList:
            nl_radio.setChecked(True)

    def DBManager_Test_List(self):

        self.c.execute(f"SELECT 평가목록 FROM Test_List")
        List = self.c.fetchall()
        List = list(set(List))

        result = []
        for i in List:
            name = str(i)
            name = name[2 : name.find(",")- 1]

            result.append(name)

        return result

    def setWidget_func(self):
        self.pass_RadioList.clear()
        self.fail_RadioList.clear()
        self.nt_RadioList.clear()
        self.na_RadioList.clear()
        self.nl_RadioList.clear()
        self.all_RadioList.clear()

        self.testList = list(self.DBManager_Test_List())

        if len(self.testList) != 0:
            
            for i in range(self.testList_Layout.count()):
                self.testList_Layout.itemAt(i).widget().deleteLater()

            for i,val in enumerate(self.testList):

                val = str(val)
                globals()[f'testList_groupbox_{i}'] = QGroupBox(val)
                globals()[f'testList_groupbox_{i}'].setMinimumSize(80, 125)

                testList_lay = QVBoxLayout()

                globals()[f'gb{i}_pass'] = QRadioButton("PASS")
                globals()[f'gb{i}_fail'] = QRadioButton("FAIL")
                globals()[f'gb{i}_nt'] = QRadioButton("N/T")
                globals()[f'gb{i}_na'] = QRadioButton("N/A")
                globals()[f'gb{i}_nl'] = QRadioButton("NULL")
                globals()[f'gb{i}_nl'].setChecked(True)

                results = [globals()[f'gb{i}_pass'], globals()[f'gb{i}_fail'], globals()[f'gb{i}_nt'], globals()[f'gb{i}_na'], globals()[f'gb{i}_nl']]

                self.pass_RadioList.append(globals()[f'gb{i}_pass'])
                self.fail_RadioList.append(globals()[f'gb{i}_fail'])
                self.nt_RadioList.append(globals()[f'gb{i}_nt'])
                self.na_RadioList.append(globals()[f'gb{i}_na'])
                self.nl_RadioList.append(globals()[f'gb{i}_nl'])
                self.all_RadioList = self.pass_RadioList + self.fail_RadioList\
                                   + self.nt_RadioList + self.na_RadioList + self.nl_RadioList

                # 평가 목록 그룹 자녀 생성
                for result in results:
                    testList_lay.addWidget(result)

                globals()[f'testList_groupbox_{i}'].setLayout(testList_lay)

                self.testList_Layout.addWidget(globals()[f'testList_groupbox_{i}'])
                self.testList_Layout.setAlignment(Qt.AlignLeft)

    def update_open_menu(self):
        self.menu.clear()
        self.menuOpen = self.menu.addMenu("Open")
        self.c.execute('SELECT * FROM Setup_Language')
        langList = self.c.fetchall()
    
        for lang in langList:
            subMenu = QAction(lang[0], self)
            subMenu.triggered.connect(partial(self.show_imgList, lang))
            
            subMenu.setCheckable(True)
            if (self.cliced_lang == subMenu.text()):
                subMenu.setChecked(True)
            else:
                subMenu.setChecked(False)

            self.menuOpen.addAction(subMenu)
                
        self.menu.addMenu(self.menuOpen)

        self.actionSave = QAction("Save", self)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.triggered.connect(self.save_result)

        self.actionCreateExcel = QAction("Create Excel", self)
        self.actionCreateExcel.triggered.connect(self.exsel_setiing_show)
        self.actionClose = QAction("Close", self)
        self.menu.addAction(self.actionSave)
        self.menu.addAction(self.actionCreateExcel)
        self.menu.addAction(self.actionClose)
        self.actionClose.triggered.connect(self.closeEvent) # close이벤트

    def save_result(self):
        print(self.result)

    def qbutton_clicked(self, state, idx, button):
        self.idx = idx
        self.button = button

        img_dir = self.img_dir[0] + '\\' + self.imgList[idx]
        pixmap = QPixmap(img_dir)
        self.img = Image.open(img_dir)

        self.img_Label.resize(self.img.width, self.img.height)

        if self.img.width < self.img_Label.width() and self.img.height < self.img_Label.height():
            pass
        elif self.img.width/self.img.height < self.img_Label.width()/self.img_Label.height():
            pixmap = pixmap.scaledToHeight(self.img_Label.height())
        else:
            pixmap = pixmap.scaledToHeight(self.img_Label.width())
        self.img_Label.setPixmap(QPixmap(pixmap))
        self.img_Label.setAlignment(Qt.AlignCenter)

        self.img_Label.mouseDoubleClickEvent = partial(self.double_click_img, img_dir)

        # 다른 이미지 버튼 누를 때 액션
        if self.pre_idx != idx and self.pre_idx != "":
            result_data = []

            # self.result에 값 저장하고 기존 데이타 삭제하기
            for i,field in enumerate(self.fieldList):
                field_data = {field[0]:globals()[f'desc_LineEdit{i}'].text()}
                result_data.append(field_data)
                globals()[f'desc_LineEdit{i}'].clear()

            for i,val in enumerate(self.testList):
                if globals()[f'gb{i}_pass'].isChecked():
                    radio_data = {val:"PASS"}
                elif globals()[f'gb{i}_fail'].isChecked():
                    radio_data = {val:"FAIL"}
                elif globals()[f'gb{i}_nt'].isChecked():
                    radio_data = {val:"N/T"}
                elif globals()[f'gb{i}_na'].isChecked():
                    radio_data = {val:"N/A"}
                else:
                    radio_data = {val:""}

                globals()[f'gb{i}_nl'].setChecked(True)
                result_data.append(radio_data)

            result_data.append({"버전 정보":self.version_textEdit.toPlainText()})
            self.result[self.pre_idx] = result_data
                
            # self.result에 기존 평가 data로 세팅
            for i,data in enumerate(self.result[idx][:len(self.fieldList)]):
                globals()[f'desc_LineEdit{i}'].setText(*data.values())

            for i,data in enumerate(self.result[idx][len(self.fieldList):-1]):
                if [*data.values()][0] == 'PASS':
                    globals()[f'gb{i}_pass'].setChecked(True)
                elif [*data.values()][0] == 'FAIL':
                    globals()[f'gb{i}_fail'].setChecked(True)
                elif [*data.values()][0] == 'N/T':
                    globals()[f'gb{i}_nt'].setChecked(True)
                elif [*data.values()][0] == 'N/A':
                    globals()[f'gb{i}_na'].setChecked(True)
                else:
                    globals()[f'gb{i}_nl'].setChecked(True)


        print(self.result)

        self.pre_idx = idx

    def double_click_img(self, img_dir, e):
        self.viewer = ImageViewer(img_dir)
        self.viewer.show()

    def show_imgList(self, lang):
        # 선택한 언어 기억
        self.cliced_lang = lang[0]

        # 평가결과 기록 삭제
        self.result.clear()

        # 레이블 초기화
        # for i,field in enumerate(self.fieldList):
        #         field_data = {field[0]:globals()[f'desc_LineEdit{i}'].text()}
        #         self.result[self.pre_idx].append(field_data)
        #         globals()[f'desc_LineEdit{i}'].clear()

        # 이미지 리스트 초기화
        for i in range(self.img_VBoxLayout.count()):
            self.img_VBoxLayout.itemAt(i).widget().deleteLater()

        # 이미지 경로 불러옴
        self.c.execute("SELECT 경로 FROM Setup_Language WHERE 언어=?", (lang[0],))
        self.img_dir = self.c.fetchone()
        self.imgList = [fn for fn in os.listdir(self.img_dir[0])
                if (fn.endswith('.png') or fn.endswith('.jpg'))]

        # 이미지 버튼 추가
        self.qbuttons = {}
        self.icons = {}
        for index, filename in enumerate(self.imgList):
            self.result[index] = []
            pixmap = QPixmap(self.img_dir[0] + '\\' + filename)
            pixmap = pixmap.scaled(40, 40, Qt.IgnoreAspectRatio)
            icon = QIcon()
            icon.addPixmap(pixmap)
            self.icons[index] = icon

        for index, icon in self.icons.items():
            button = QPushButtonIcon()
            button.setIcon(icon)
            button.clicked.connect(lambda state, button = button, idx = index :
                        self.qbutton_clicked(state, idx, button))
            self.img_VBoxLayout.addWidget(button)
            self.qbuttons[index] = button

        self.qbuttons[0].click()
        self.horizontalLayout.addLayout(self.img_VBoxLayout)

    def set_field(self):
        self.c.execute('SELECT * FROM Setup_Field')
        self.fieldList = self.c.fetchall()

        for i,field in enumerate(self.fieldList):
            if i%2==0:
                globals()[f'field_Label{i}'] = QLabel(field[0])
                self.field_gridLayout.addWidget(globals()[f'field_Label{i}'], 0,i)
                globals()[f'desc_LineEdit{i}'] = QLineEdit()
                self.field_gridLayout.addWidget(globals()[f'desc_LineEdit{i}'], 0,i+1)
            else:
                globals()[f'field_Label{i}'] = QLabel(field[0])
                self.field_gridLayout.addWidget(globals()[f'field_Label{i}'], 1,i-1)
                globals()[f'desc_LineEdit{i}'] = QLineEdit()
                self.field_gridLayout.addWidget(globals()[f'desc_LineEdit{i}'], 1,i)
            
    def exsel_setiing_show(self):
        self.EC.setupUi()
        self.EC.show()    

    def closeEvent(self, event) -> None: # a0: QtGui.QCloseEvent
        sys.exit()

class QPushButtonIcon(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setIconSize(QSize(40, 40))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
