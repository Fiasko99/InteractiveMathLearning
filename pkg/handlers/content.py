import math
import os
from functools import partial
from typing import Callable, List, Union

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ..commons import ROOT_PATH
from ..gui import Ui_ContentWindow
from .canvas import MplCanvas
from .profile import UiProfileWindowImpl
from .settings import UiSettingsWindowImpl

__all__ = ["UiContentWindowImpl"]


class UiContentWindowImpl(QMainWindow, Ui_ContentWindow):
    x: List[float]
    y: List[float]
    formula: Callable[[], List[float]]
    window: Union[UiProfileWindowImpl, UiSettingsWindowImpl]

    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.client = client
        from .auth import UiAuthWindowImpl

        self.auth = UiAuthWindowImpl
        self.client_profile = UiProfileWindowImpl
        self.settings = UiSettingsWindowImpl
        self.profile.triggered.connect(self.open_profile)
        self.editProfile.triggered.connect(self.edit_profile)
        self.exitProfile.triggered.connect(self.logout)
        self.section.clicked.connect(self.on_item_clicked)
        self.widget = QWidget()
        self.scrollArea.setWidget(self.widget)
        self.layout_SArea = QVBoxLayout(self.widget)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar2QT(self.canvas, self.scrollArea)
        self.a = 1
        self.b = 1
        self.c = 1
        self.z = 1

    def on_item_clicked(self, item):
        try:
            self.draw_plot()
            if item.data() == "Квадратичная функция":
                self.x = [diapason * 0.1 for diapason in range(-100, 101)]
                self.formula = lambda: [
                    self.a * pow(x, 2) + x * self.b + self.c for x in self.x
                ]
                self.draw_quadratic_plot()
            elif item.data() == "График функции \ny = ( (x + a) (x + b) ) / x":
                self.x = [
                    diapason * 0.1 for diapason in range(-100, 101) if diapason != 0
                ]
                self.formula = lambda: [
                    (x + self.a) * ((x + self.b) / x) for x in self.x
                ]
                self.draw_asymptote_2_plot()
            elif item.data() == "График функции \ny = ( x^2 - a ) / x":
                self.x = [
                    diapason * 0.1 for diapason in range(-100, 101) if diapason != 0
                ]
                self.formula = lambda: [(pow(x, 2) - self.a) / x for x in self.x]
                self.draw_asymptote_3_plot()
            elif item.data() == "График функции \ny = e^(x - 1) / x":
                self.x = [
                    diapason * 0.001 for diapason in range(-4000, 4001) if diapason != 0
                ]
                self.formula = lambda: [math.exp(x - self.a) / x for x in self.x]
                self.draw_asymptote_22_plot()
            elif item.data() == "График функции \ny = xe^x":
                self.x = [diapason * 0.001 for diapason in range(-10000, 1000)]
                self.formula = lambda: [math.exp(x) * x for x in self.x]
                self.draw_asymptote_23_plot()

            elif item.data() == "График функции \ny = (a - x^3) / ( x^2 )":
                self.x = [
                    diapason * 0.1 for diapason in range(-100, 101) if diapason != 0
                ]
                self.formula = lambda: [
                    (self.a / pow(x, 3)) / pow(x, 2) for x in self.x
                ]
                self.draw_asymptote_new_plot_1()
            elif item.data() == "График функции \ny = -( x / (x + 2) ) ^ 2":
                self.x = [
                    diapason * 0.1 for diapason in range(-1000, 1001) if diapason != -20
                ]
                self.formula = lambda: [-1 * pow((x / (x + 2)), 2) for x in self.x]
                self.draw_asymptote_new_plot_2()
            elif item.data() == "График функции \ny = x^3 - ax":
                self.x = [diapason * 0.1 for diapason in range(-100, 101)]
                self.formula = lambda: [pow(x, 3) - self.a * x for x in self.x]
                self.draw_asymptote_new_plot_3()
            elif item.data() == "График функции \ny = x^4 + ax^3 + bx^2 + cx + z":
                self.x = [diapason * 0.1 for diapason in range(-100, 101)]
                self.formula = lambda: [
                    pow(x, 4)
                    + self.a * pow(x, 3)
                    + self.b * pow(x, 2)
                    + self.c * x
                    + self.z
                    for x in self.x
                ]
                self.draw_asymptote_new_plot_4()
            elif item.data() == "График функции \ny = x^( 1/2 )":
                self.x = [diapason * 0.1 for diapason in range(0, 101)]
                self.formula = lambda: [math.sqrt(x) for x in self.x]
                self.draw_asymptote_new_plot_5()

            elif item.data() == "График функции \ny = x lnx":
                self.x = [diapason * 0.1 for diapason in range(0, 101) if diapason != 0]
                self.formula = lambda: [x * math.log(x) for x in self.x]
                self.draw_asymptote_25_plot()
            elif item.data() == "График функции \ny = log (a) x":
                self.x = [diapason * 0.1 for diapason in range(1, 101)]
                self.formula = lambda: [
                    math.log(x, self.a if self.a != 0 and self.a != 1 else 0.1)
                    for x in self.x
                ]
                self.draw_asymptote_new_plot_3()

            elif item.data() == "Формула cos x":
                self.x = [
                    diapason * 0.1 for diapason in range(-100, 101) if diapason != 0
                ]
                self.formula = lambda: [math.cos(x) for x in self.x]
                self.draw_trig_1_plot()
            elif item.data() == "Формула sin x":
                self.x = [
                    diapason * 0.1 for diapason in range(-100, 101) if diapason != 0
                ]
                self.formula = lambda: [math.sin(x) for x in self.x]
                self.draw_trig_2_plot()
            elif item.data() == "Формула tg x":
                self.x = [
                    diapason * 0.1 for diapason in range(-100, 101) if diapason != 0
                ]
                self.formula = lambda: [math.sin(x) / math.cos(x) for x in self.x]
                self.draw_trig_3_plot()
            elif item.data() == "Формула ctg x":
                self.x = [
                    diapason * 0.1 for diapason in range(-100, 101) if diapason != 0
                ]
                self.formula = lambda: [math.cos(x) / math.sin(x) for x in self.x]
                self.draw_trig_4_plot()
            self.redraw_plot()
        except Exception as e:
            print(e)

    def draw_asymptote_new_plot_1(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        a = QTextEdit()
        a.setFixedHeight(24)
        a.setPlaceholderText("a = " + str(self.a))
        a.setDocumentTitle("a")
        a.textChanged.connect(partial(self.edit_param, a))
        layout_groupbox.addWidget(a)

        text = QLabel("Исследуем функцию, заданную формулой:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex1_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("1. Область определения: x < 0; x > 0 или x != 0")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex1_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("2. Точки пересечения с осью x")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex1_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "3. Функция ни четная, ни нечетная. "
            "Симметрии относительно оси ординат нет. "
            "Симметрии относительно начала координат нет. Так как "
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex1_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "4. Функция непрерывная при x != 0. "
            "Точка x = 0 есть точка разрыва второго рода."
        )
        layout_groupbox.addWidget(text)

        text = QLabel(
            "5. Вертикальная асимптота x = 0. Наклонные ассимптоты y = -x. Так как"
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex1_5.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("6. Первая производная ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex1_6.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        image_path = os.path.realpath(ROOT_PATH("ex1_7.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        image_path = os.path.realpath(ROOT_PATH("ex1_8.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_new_plot_2(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        a = QTextEdit()
        a.setFixedHeight(24)
        a.setPlaceholderText("a = " + str(self.a))
        a.setDocumentTitle("a")
        a.textChanged.connect(partial(self.edit_param, a))
        layout_groupbox.addWidget(a)

        text = QLabel("Исследуем функцию, заданную формулой:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex12_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "1. Область определения: x < -2; x > -2 или x + 2 = 0 или x != -2"
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex12_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("2. Точки пересечения с осями: x = 0 y = 0")
        layout_groupbox.addWidget(text)

        text = QLabel(
            "3. Симметрия относительно оси ординат: нет. "
            "Симметрия относительно начала координат: нет. Так как"
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex12_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "4. Функция непрерывна при x != -2. "
            "Точка x = -2 - точка разрыва второго рода."
        )
        layout_groupbox.addWidget(text)

        text = QLabel(
            "5. Вертикальные асимптоты: x = -2. "
            "Налонные асимптоты: нет. Горизонтальные асимптоты: y = -1."
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex12_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Предел данной функции на бесконечности равен числу -1")
        layout_groupbox.addWidget(text)

        text = QLabel("6. Первая произовдная: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex12_5.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Так как: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex12_6.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        image_path = os.path.realpath(ROOT_PATH("ex12_7.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        image_path = os.path.realpath(ROOT_PATH("ex12_8.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Возможные точки перегиба: x = 1 \n Тестовые интервалы")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex12_9.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_new_plot_3(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        a = QTextEdit()
        a.setFixedHeight(24)
        a.setPlaceholderText("a = " + str(self.a))
        a.setDocumentTitle("a")
        a.textChanged.connect(partial(self.edit_param, a))
        layout_groupbox.addWidget(a)

        text = QLabel("ОДЗ: x – произвольный. ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex13_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "Найдём критические точки (то есть внутренние точки области определения функции, "
            "в которых её производная равна 0 или не существует):"
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex13_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "Производная существует при любом x. 2) Найдём промежутки знакопостоянства y′: "
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex13_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("3) Эскиз графика y: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex13_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Таким образом, x=1 – точка локального минимума функции y.")
        layout_groupbox.addWidget(text)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_new_plot_4(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        a = QTextEdit()
        a.setFixedHeight(24)
        a.setPlaceholderText("a = " + str(self.a))
        a.setDocumentTitle("a")
        a.textChanged.connect(partial(self.edit_param, a))
        layout_groupbox.addWidget(a)

        b = QTextEdit()
        b.setFixedHeight(24)
        b.setPlaceholderText("b = " + str(self.b))
        b.setDocumentTitle("b")
        b.textChanged.connect(partial(self.edit_param, b))
        layout_groupbox.addWidget(b)

        c = QTextEdit()
        c.setFixedHeight(24)
        c.setPlaceholderText("c = " + str(self.c))
        c.setDocumentTitle("c")
        c.textChanged.connect(partial(self.edit_param, c))
        layout_groupbox.addWidget(c)

        z = QTextEdit()
        z.setFixedHeight(24)
        z.setPlaceholderText("z = " + str(self.z))
        z.setDocumentTitle("z")
        z.textChanged.connect(partial(self.edit_param, z))
        layout_groupbox.addWidget(z)

        text = QLabel("Исследовать функцию и построить ее график: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex14_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "Найдём критические точки (то есть внутренние точки области определения функции, "
            "в которых её производная равна 0 или не существует): "
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex14_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "откуда находим x=−1. Для того, чтобы найти точки локального максимума/минимума функции, "
            "нужно понять, как схематично выглядит её график. "
            "\n2) Найдём промежутки знакопостоянства y′:"
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex14_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("3) Эскиз графика y:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex14_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Таким образом, x = −1 – точка минимума функции y.")
        layout_groupbox.addWidget(text)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_new_plot_5(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        text = QLabel(
            """
            1) Выражение  имеет смысл только при неотрицательных значениях x, 
            следовательно областью определения функции является промежуток .

            2) Множеством значений функции является промежуток 
            
            3) Значение функции y=0 является наименьшим, а наибольшего значения функция не имеет.
            
            4) Функция не является ни четной, ни нечетной.
            
            5) Функция непериодическая.
            
            6) График функции пересекается с осями в единственной точке - (0;0).
            
            7)Точка (0;0) является нулем функции.
            
            8) Функция монотонно возрастает на области определения.
            
            9) Функция принимает положительные значения на промежутке, 
            график расположен в I координатном угле.
        """
        )
        layout_groupbox.addWidget(text)

        self.layout_SArea.addWidget(group_box)

    def draw_trig_1_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        text = QLabel(
            """
            1. Область определения — все действительные числа (множество R).
 
            2. Множество значений — промежуток [−1;1].
             
            3. Функция y=cosx имеет период 2π.
             
            4. Функция y=cosx является чётной.
             
            5. Нули функции: x=π2+πn,n∈Z;
            наибольшее значение равно 1 при x=2πn,n∈Z;
            наименьшее значение равно −1 при  x=π+2πn,n∈Z;
            значения функции положительны на интервале (−π2;π2), 
                с учётом периодичности функции на интервалах (−π2+2πn;π2+2πn),n∈Z;
            значения функции отрицательны на интервале (π2;3π2), 
                с учётом периодичности функции на интервалах (π2+2πn;3π2+2πn),n∈Z.
             
            6. Функция y=cosx:
            - возрастает на отрезке [π;2π], с учётом 
                периодичности функции на отрезках [π+2πn;2π+2πn],n∈Z;
            - убывает на отрезке [0;π], с учётом 
                периодичности функции на отрезках [2πn;π+2πn],n∈Z.
        """
        )
        layout_groupbox.addWidget(text)

        self.layout_SArea.addWidget(group_box)

    def draw_trig_2_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        text = QLabel(
            """
            1. Е(f): R - множество всех действительных чисел
            
            2. D(f): [-1;1]
            
            3. Функция нечетная sin(-x)=-sinx
    
            4.Т=2π
            
            5. y>o, при х Є (0+2πk; π +2πk), kЄ Z
            
            y<o, при х Є (-π +; 0+2πk ), kЄ Z
            
            6.Функция возрастает от [-1;1] при
            - x Є[-π/2+2πk; π/2+2πk] , kЄ Z
            - Функция убывает от [-1;1] при
            - x Є [π/2+2πk; 3/2π+2πk] , kЄ Z
            
            7. Уmax=1 при х=π/2+2πk , kЄ Z
            Уmin=-1 при х=-π/2+2πk , kЄ Z
        """
        )
        layout_groupbox.addWidget(text)

        self.layout_SArea.addWidget(group_box)

    def draw_trig_3_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        text = QLabel(
            """
            1. Область определения — множество всех действительных чисел x≠π2+πn,n∈Z.

            2. Множество значений — множество R всех действительных чисел.
            
            3. Функция y=tgx периодическая с периодом π.
            
            4. Функция y=tgx нечётная.
            
            5. Функция y=tgx принимает:
            - значение 0 при x=πn,n∈Z;
            - положительные значения на интервалах (πn;π2+πn),n∈Z;
            - отрицательные значения на интервалах (−π2+πn;πn),n∈Z.
            
            6. Функция y=tgx возрастает на интервалах (−π2+πn;π2+πn),n∈Z.
        """
        )
        layout_groupbox.addWidget(text)

        self.layout_SArea.addWidget(group_box)

    def draw_trig_4_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        text = QLabel(
            """
            1. Область определения — множество всех действительных чисел x≠πn,n∈Z.
 
            2. Множество значений — множество R всех действительных чисел.
             
            3. Функция y=ctgx периодическая с периодом π.
             
            4. Функция y=ctgx нечётная.
             
            5. Функция y=ctgx принимает:
            - значение 0 при x=π2+πn,n∈Z;
            - положительные значения на интервалах (πn;π2+πn),n∈Z;
            - отрицательные значения на интервалах (−π2+πn;πn),n∈Z.
             
            6. Функция y=ctgx убывает на интервалах (πn;π+πn),n∈Z.
        """
        )
        layout_groupbox.addWidget(text)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_22_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        a = QTextEdit()
        a.setFixedHeight(24)
        a.setPlaceholderText("a = " + str(self.a))
        a.setDocumentTitle("a")
        a.textChanged.connect(partial(self.edit_param, a))
        layout_groupbox.addWidget(a)

        text = QLabel(
            "Исследовать функцию средствами дифференциального исчисления и построить ее график: "
        )
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex22_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "1. Область определения: x не равен 0  или x принадлежит R \ {0} "
        )
        layout_groupbox.addWidget(text)

        text = QLabel("2. Нули функции: y не равен 0, так как e^(x - 1) > 0  ")
        layout_groupbox.addWidget(text)

        text = QLabel("3. Ни четная ни нечетная.")
        layout_groupbox.addWidget(text)

        text = QLabel("4. Возрастание, убывание: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex22_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Промежутки монотонности: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex22_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("5. Выпуклость, вогнутость: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex22_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Получим: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex22_5.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("6.Наклонные асимптоты: \ny = ax + b")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex22_6.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Наклонных асимптот нет.")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex22.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_23_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        text = QLabel(
            "Исследовать методами дифференциального исчисления функцию и, "
            "используя результаты исследования, построить ее график. y = x * e^x"
        )
        layout_groupbox.addWidget(text)

        text = QLabel("1.Область определения:  x принадлежит множетсву R")
        layout_groupbox.addWidget(text)

        text = QLabel("2.Нули функции:\ny = 0 -> x = 0")
        layout_groupbox.addWidget(text)

        text = QLabel("3.Промежутки знакопостоянства:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex23_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("4.Возрастание, убывание:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex23_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Для определения критической точки решим уравнение:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex23_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("5.Выпуклость, вогнутость:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex23_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("6.Наклонные асимптоты: \ny = ax + b")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex23_5.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Наклонных асимптот нет. \nПостроим график функции:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex23.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_25_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        text = QLabel("Исследуйте функцию и постройте ее график: \ny = xln x")
        layout_groupbox.addWidget(text)

        text = QLabel("1.Область определения функции: x > 0")
        layout_groupbox.addWidget(text)

        text = QLabel("2. Нули функции: \nxln x = 0")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex25_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("3.Промежутки знакопостоянства:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex25_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("4.Возрастание, убывание: \ny = xln x")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex25_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("5.Выпуклость, вогнутость.")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex25_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("По полученным исследованиям построим график функций:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex25.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_3_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        a = QTextEdit()
        a.setFixedHeight(24)
        a.setPlaceholderText("a = " + str(self.a))
        a.setDocumentTitle("a")
        a.textChanged.connect(partial(self.edit_param, a))
        layout_groupbox.addWidget(a)

        heading = QLabel("Наклонные асимптоты 2")
        layout_groupbox.addWidget(heading)

        text = QLabel("Исследуйте функцию и постройте ее график: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("1.Область определения функции")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("2.Нули функции. ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("График функции пересекает ось Ox в найденных точках.")
        layout_groupbox.addWidget(text)

        text = QLabel("3.Промежутки знакопостоянства:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("4. Четность, нечетность:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("4. Четность, нечетность:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_5.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "Функция нечетная, график функции симметричен относительно начала координат."
        )
        layout_groupbox.addWidget(text)

        text = QLabel("5. Промежутки возрастания, убывания:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_6.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("6.Выпуклость, вогнутость:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_7.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("7. Пределы в нуле")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_8.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("8.Наклонные асимптоты y = ax + b")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3_19.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("График:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        self.layout_SArea.addWidget(group_box)

    def draw_asymptote_2_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)

        a = QTextEdit()
        a.setFixedHeight(24)
        a.setPlaceholderText("a = " + str(self.a))
        a.setDocumentTitle("a")
        a.textChanged.connect(partial(self.edit_param, a))
        layout_groupbox.addWidget(a)

        b = QTextEdit()
        b.setFixedHeight(24)
        b.setPlaceholderText("b = " + str(self.b))
        b.setDocumentTitle("b")
        b.textChanged.connect(partial(self.edit_param, b))
        layout_groupbox.addWidget(b)

        heading = QLabel("Наклонные асимптоты 1")
        layout_groupbox.addWidget(heading)

        text = QLabel("Исследуйте функцию и постройте ее график: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_1.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Решение: ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("1.Область определения ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_3.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("2.Четность, нечетность. ")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_4.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Функция ни четная, ни нечетная.")
        layout_groupbox.addWidget(text)

        text = QLabel("3.Нули функции:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_5.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("4.Промежутки знакопостоянства:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_6.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("5.Возрастание, убывание.")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_7.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Покажем на плоскости:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_8.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel(
            "Там, где производная положительна «+», "
            "график функции возрастает, где отрицательна «-», убывает."
        )
        layout_groupbox.addWidget(text)

        text = QLabel("6.Выпуклость, вогнутость.")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_9.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("7.Наклонные асимптоты:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_10.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Где:")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2_11.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        text = QLabel("Получили: y = x + 9")
        layout_groupbox.addWidget(text)
        image_path = os.path.realpath(ROOT_PATH("ex2.jpg"))
        label_image = QLabel()
        label_image.setPixmap(QPixmap(image_path))
        layout_groupbox.addWidget(label_image)

        self.layout_SArea.addWidget(group_box)

    def draw_quadratic_plot(self):
        group_box = QGroupBox("Теория:", self)
        layout_groupbox = QVBoxLayout(group_box)
        a = QTextEdit()
        a.setFixedHeight(24)
        a.setPlaceholderText("a = " + str(self.a))
        a.setDocumentTitle("a")
        a.textChanged.connect(partial(self.edit_param, a))
        b = QTextEdit()
        b.setFixedHeight(24)
        b.setPlaceholderText("b = " + str(self.b))
        b.setDocumentTitle("b")
        b.textChanged.connect(partial(self.edit_param, b))
        c = QTextEdit()
        c.setFixedHeight(24)
        c.setPlaceholderText("c = " + str(self.c))
        c.setDocumentTitle("c")
        c.textChanged.connect(partial(self.edit_param, c))
        layout_groupbox.addWidget(a)
        layout_groupbox.addWidget(b)
        layout_groupbox.addWidget(c)
        heading = QLabel("Квадратичная функция")
        layout_groupbox.addWidget(heading)
        heading = QLabel(
            """
                    Функция, заданная формулой y = ax2 + bx + c,
                    где x и y - переменные, а a, b, c - заданные числа,
                    причем a ≠ 0, называется квадратичной функцией.

                    График квадратичной функции - парабола. Если a > 0,
                    то ветви параболы направлены вверх. Если a < 0,
                    то ветви параболы направлены вниз.
                """
        )
        layout_groupbox.addWidget(heading)
        self.layout_SArea.addWidget(group_box)

    def clear_box(self, layout=False):
        if not layout:
            layout = self.layout_SArea
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_box(item.layout())

    def draw_plot(self):
        self.reset_canvas()
        self.clear_box(self.layout_SArea)
        group_box = QGroupBox("График:", self)
        group_box.setMinimumSize(500, 500)
        layout_groupbox = QVBoxLayout(group_box)
        layout_groupbox.addWidget(self.toolbar)
        layout_groupbox.addWidget(self.canvas)
        self.canvas.axes.cla()
        self.canvas.axes.grid()
        graphic_btn = QPushButton("Построить график")
        graphic_btn.clicked.connect(self.redraw_plot)
        layout_groupbox.addWidget(graphic_btn)
        reset_btn = QPushButton("Вернуть")
        reset_btn.clicked.connect(self.reset_canvas)
        layout_groupbox.addWidget(reset_btn)
        self.layout_SArea.addWidget(group_box)

    def redraw_plot(self):
        try:
            self.y = self.formula()
            self.canvas.axes.plot(self.x, self.y)
            self.canvas.draw()
        except Exception as e:
            print(e)

    def reset_canvas(self):
        self.a = 1
        self.b = 1
        self.c = 1
        self.z = 1
        self.canvas.axes.cla()
        self.canvas.axes.grid()
        self.redraw_plot()

    def edit_param(self, text_edit):
        try:
            if text_edit.documentTitle() == "a":
                self.a = int(text_edit.toPlainText())
            elif text_edit.documentTitle() == "b":
                self.b = int(text_edit.toPlainText())
            elif text_edit.documentTitle() == "c":
                self.c = int(text_edit.toPlainText())
            self.y = self.y
        except Exception as e:
            print(e, "Не число")

    def closeEvent(self, event):
        dialog = QMessageBox
        ret = QMessageBox.question(
            self, "", "Уверены что хотите выйти из профиля?", dialog.Yes | dialog.No
        )
        if ret == dialog.Yes:
            self.logout()
        else:
            event.ignore()

    def logout(self):
        self.auth = self.auth()
        self.auth.show()
        self.hide()

    def open_profile(self):
        self.window = self.client_profile(self.client)
        self.window.fill_profile()
        self.window.show()

    def edit_profile(self):
        self.window = self.settings(self.client)
        self.window.show()
