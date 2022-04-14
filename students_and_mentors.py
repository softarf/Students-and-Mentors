
# -*- coding: utf-8 -*-

from random import random, sample

def average_score(grades_dict):  # Подсчёт средней оценки.
    num = 0
    full = 0
    for val in grades_dict.values():
        for score in val:
            num += 1
            full += score
    if num > 0:
        res = full / num
    else:
        res = 0
    return res

def texted(courses_name):  # Печать элементов списка.
    text = ''
    i = 1
    for item in courses_name:
        if i != 1:
            text += ', ' + item
        else:
            text += ' ' + item
        i += 1
    return text

class Men:
    def __init__(self, any_name='Adam', any_surname='', any_sex='м'):
        self.name = any_name             # Имя
        self.surname = any_surname       # Фамилия
        self.sex = any_sex               # Пол

    def __str__(self):
        quote = f' Имя: {self.name}\n Фамилия: {self.surname}'
        return quote

    def _rate_hw_method(evaluator, getting, course, flag, k):  # Выставление оценки.
        #   Если flag == 1, то функция вызвана проверяющим, если flag == 0, то студентом.
        #   k - "коэффициент корректировки успеваемости"
        if type(getting) in (Student, Lecturer):
            if flag == 1:
                ev, gt = evaluator, getting
            elif flag == 0:
                ev, gt = getting, evaluator
            if course in gt.courses_in_progress and course in ev.courses_attached:
                grade = int((random() ** k) * 11)
                getting.grades[course] = getting.grades.get(course, []) + [grade]
                res = grade
            else:
                res = 'Не выставлена'
        else:
            print(' Человек не подходит. Неизвестный класс:', type(getting))
            res = 'Человек не подходит'
        return res

class Student(Men):
    def __init__(self, any_name='Adam', any_surname='', any_sex='м'):
        super().__init__(any_name, any_surname, any_sex)
        self.finished_courses = []       # Завершённые курсы
        self.courses_in_progress = []    # Изучаемые курсы
        self.grades = {}                 # Журнал успеваемости
    
    def add_courses(self, course_name):
        self.finished_courses.append(course_name)
    
    def rate_hw(self, lectur, cours):  # Выставление оценки.
        res = super()._rate_hw_method(lectur, cours, 0, 0.25)
        return res

    def __str__(self):
        quote = super().__str__()
        res = average_score(self.grades)
        quote += f'\n Средняя оценка за домашние задания: {res:4.2f}\n Курсы в процессе изучения:'
        quote += texted(self.courses_in_progress)
        quote += f'\n Завершённые курсы:'
        quote += texted(self.finished_courses)
        return quote
        
    def __lt__(self, other):
        #if type(other) in (Student, ):
        if isinstance(other, Student):
            aver1 = average_score(self.grades)
            aver2 = average_score(other.grades)
            res = aver1 < aver2
        else:
            print(' Человек не подходит. Неизвестный класс:', type(other))
            res = 'Человек не подходит'
        return res

class Teacher(Men):
    def __init__(self, any_name='Adam', any_surname='', any_sex='м'):
        super().__init__(any_name, any_surname, any_sex)
        self.courses_attached = []       # Закреплённые курсы

class Lecturer(Teacher):
    def __init__(self, any_name='Adam', any_surname='', any_sex='м'):
        super().__init__(any_name, any_surname, any_sex)
        self.grades = {}                 # Оценки

    def __str__(self):
        quote = super().__str__()
        res = average_score(self.grades)
        quote += f'\n Средняя оценка за лекции: {res:4.2f}'
        return quote
        
    def __lt__(self, other):
        if type(other) in (Lecturer, ):
            aver1 = average_score(self.grades)
            aver2 = average_score(other.grades)
            res = aver1 < aver2
        else:
            print(' Человек не подходит. Неизвестный класс:', type(other))
            res = 'Человек не подходит'
        return res

class Reviewer(Teacher):
    def __init__(self, any_name='Adam', any_surname='', any_sex='м'):
        super().__init__(any_name, any_surname, any_sex)
    
    def rate_hw(self, student, course):  # Выставление оценки.
        res = super()._rate_hw_method(student, course, 1, 0.5)
        return res

    def __str__(self):
        quote = super().__str__()
        return quote

def subject_set(received_list, subjects, mn_or_st=1):
    k = 0
    for i in range(len(received_list)):
        for j in range(len(subjects) - abs(mn_or_st)):
            if mn_or_st != 0:
                received_list[i].courses_attached.append(subjects[k % 3])
                k += 1
            else:
                if j == i % 3:  # Данный предмет для студента запишем в пройденные (finished_courses).
                    # Воспользуемся методом .add_courses() встроенным в класс Student.
                    received_list[i].add_courses(subjects[j])
                    # Или можно обратиться к атрибуту .finished_courses напрямую.
                    # received_list[i % 5].finished_courses.append(subjects[j])
                else:      # Остальные как изучаемые.
                    received_list[i].courses_in_progress.append(subjects[j])

def data_input():
    #  Все персонажи вымышленные. Совпадение с реальными людьми случайное.
    students_list = []
    lecturers_list = []
    reviewers_list = []
    subjects_list = []
    word_lines = ['Иванов Сергей м', 'Сергеев Петр м', 'Петров Василий м', 'Васильев Андрей м',
                   'Вилкова Анна ж','Андреев Денис м']
    for i in range(len(word_lines)):
        word_line = word_lines[i].strip().split()
        one_student = Student(word_line[1], word_line[0], word_line[2])
        students_list.append(one_student)
    word_lines = ['Ильназ Гильязов м', 'Александр Иванов м', 'Алёна Батицкая ж']
    for i in range(len(word_lines)):
        word_line = word_lines[i].strip().split()
        one_lecturer = Lecturer(word_line[0], word_line[1], word_line[2])
        lecturers_list.append(one_lecturer)
    word_lines = ['Павел Дерендяев м', 'Николай Лопин м', 'Алексей Яковлев м']
    for i in range(len(word_lines)):
        word_line = word_lines[i].strip().split()
        one_reviewer = Reviewer(word_line[0], word_line[1], word_line[2])
        reviewers_list.append(one_reviewer)
    subjects_list = ['Основы программирования на Python', 'Git', 'SQL и получение данных']
    subject_set(lecturers_list, subjects_list, 1)
    subject_set(reviewers_list, subjects_list, -1)
    subject_set(students_list, subjects_list, 0)
    return lecturers_list, reviewers_list, students_list, subjects_list

def course_average(analyzeds, course):
    num = 0
    full = 0
    for men in analyzeds:
        if course in men.grades.keys():
            val = men.grades[course]
            for score in val:
                num += 1
                full += score
    if num > 0:
        res = full / num
    else:
        res = 0
    return res

def print_list(men, flag):
    print(f' Имя: {men.name}   Фамилия: {men.surname}   Пол: {men.sex}')
    if flag != 0:
        print(' Предметы:', men.courses_attached)
    else:
        print(' Завершённые:', men.finished_courses)
        print(' Изучаемые  :', men.courses_in_progress)
    if flag != -1:
        print(' Оценки: ', men.grades)


#                                         Головной блок
#                  1. Наследование классов.
lecturers, reviewers, students, courses = data_input()

#                  2.1 "Каждый проверяющий выставляет по три оценки каждому студенту"
for i in range(len(reviewers)):
    rev = reviewers[i]
    for j in range(len(students)):
        stud = students[j]
        for k in range(len(courses)):
            cour = courses[k]
            for m in range(3):
                result = rev.rate_hw(stud, cour)
#                 quote = f'Проверил: {rev.surname} {rev.name}, студент: {stud.name} {stud.surname}'  # Для теста.
#                 print(f' {quote}, курс: {cour}, оценка: {result}\n Все оценки: {stud.grades}')     # Для теста.

#                  2.1.a Тестирование на иной класс. Для теста.
# Tom = Men('Василий', 'Петров', 'м')
# rev = reviewers[2]
# stud = Tom
# cour = 'Git'
# result = rev.rate_hw(stud, cour)
# quote = f'Проверил: {rev.surname} {rev.name}, оцениваемый: {stud.name} {stud.surname},'  # Для теста.
# print(f' {quote} соотв. типа: {type(stud) in (Student, Lecturer)}, курс: {cour}, оценка: {result}')     # Для теста.
# Jerry = Teacher('Алёна', 'Батицкая', 'ж')
# rev = reviewers[2]
# stud = Jerry
# cour = 'Git'
# result = rev.rate_hw(stud, cour)
# quote = f'Проверил: {rev.surname} {rev.name}, оцениваемый: {stud.name} {stud.surname},'  # Для теста.
# print(f' {quote} соотв. типа: {type(stud) in (Student, Lecturer)}, курс: {cour}, оценка: {result}')     # Для теста.

#                  2.2 "Каждый студент выставляет по одной оценке каждому лектору"
for i in range(len(students)):
    stud = students[i]
    for j in range(len(lecturers)):
        lec = lecturers[j]
        for k in range(len(courses)):
            cour = courses[k]
            result = stud.rate_hw(lec, cour)
#             quote = f'Студент: {stud.name} {stud.surname}, лектор: {lec.surname} {lec.name}'    # Для теста.
#             print(f' {quote}, курс: {cour}, оценка: {result}\n Все оценки: {lec.grades}')   # Для теста.

#                  3.1 Перегрузка магического метода __str__
print('\n В этом учебном году.')
print('\n Лекторы:')
for pers in lecturers:
    print(pers)
print('\n Проверяющие:')
for pers in reviewers:
    print(pers)
print('\n Студенты:')
for pers in students:
    print(pers)

#                  3.2 Сравнивание между собой по средней оценке.
print()
print(lecturers[1] < lecturers[0])
print(students[2] < students[1])
print(students[0] < lecturers[2])

#                  4.1 Подсчёт средней оценки за домашние задания по всем студентам в рамках конкретного курса.
course = 'Основы программирования на Python'
stud_aver = course_average(students, course)
print(f'\n course: {course},  stud_aver = {stud_aver:4.2f}')

#                  4.2 Подсчёт средней оценки за лекции всех лекторов в рамках конкретного курса.
course = 'SQL и получение данных'
lec_aver = course_average(lecturers, course)
print(f' course: {course},  lec_aver = {lec_aver:4.2f}')


#                  Печать конечного состояния. Для теста.
# my_list = [lecturers, reviewers, students]
# flags = [('Лекторы.', 1), ('Проверяющие.', -1), ('Студенты.', 0)]
# for i in range(3):
#     print()
#     print(flags[i][0])
#     flg = flags[i][1]
#     for item in my_list[i]:
#         print_list(item, flg)

# print('\n  -- Конец --  ')  #                 - Для блокнота
input('\n  -- Конец --  ')	#	Типа  "Пауза" - Для среды
