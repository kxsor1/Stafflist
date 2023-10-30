import tkinter as tk
from tkinter import ttk
import sqlite3

# Главное окно
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

###################################################################################
    # Хранение и создание виджетов
    def init_main(self):
        # Создание области кнопок
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Добавить
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Обновить
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.upd_img, command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)

        # Удалить
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.del_img, command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # Поиск
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Обновление
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

##############################################################################################
        # Создание таблицы
        self.tree=ttk.Treeview(self, columns=('id', 'name', 'phone', 'email', 'salary'),
                                height=45, show='headings')
        
        # Добавление параметров колонкам
        self.tree.column('id', width=35, anchor=tk.CENTER)
        self.tree.column('name', width=200, anchor=tk.CENTER)
        self.tree.column('phone', width=125, anchor=tk.CENTER)
        self.tree.column('email', width=140, anchor=tk.CENTER)
        self.tree.column('salary', width=110, anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E_mail')
        self.tree.heading('salary', text='Зарплата')

        # Упаковка
        self.tree.pack(side=tk.LEFT)

        # Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

#################################################################################################
    # Метод для записи данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # Метод для отображения данных
    def view_records(self):
        self.db.cur.execute("""SELECT * FROM users""")
        # Удалить всё из виджета

        [self.tree.delete(i) for i in self.tree.get_children()]
        # Добавляем в таблицу все данные из бд
        [self.tree.insert('', 'end', values=row)
        for row in self.db.cur.fetchall()]

    # Метод обновления данных
    def update_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''UPDATE users SET name=?, phone=?, email=?, salary=? WHERE id=?''',
                            (name, phone, email, salary, id))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления данных
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute('''DELETE FROM users WHERE id=?''',
                                (self.tree.set(row, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска по ФИО
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute('''SELECT * FROM users WHERE name LIKE ?''', (name, ))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
        for row in self.db.cur.fetchall()]

###########################################################################################
    # Метод, отвечающий за вызов окна добавления
    def open_child(self):
        Child()

    # Метод, отвечающий за вызов окна обновления
    def open_update_child(self):
        Update()

    # Метод, отвечающий за вызов окна Поиска
    def open_search(self):
        Search()


###############################################################################################
###############################################################################################
###############################################################################################


# Окно добавления данных
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    
    def init_child(self):
        self.title('Добавить')
        self.geometry("400x250")
        root.resizable(False, False)
        # Перехватить все события, происходящие в приложении
        self.grab_set()
        # Захватить фокус
        self.focus_set()

#######################################################################################
        # Подписи
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зар.плата: ')
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

######################################################################################################
        # Кнопка закрытия
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)
        
        # Кнопка добавления
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get(),
                                            self.entry_salary.get()))
        
# Окно изменения ланных
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()

        self.btn_upd = ttk.Button(self, text='Редактировать')
        self.btn_upd.bind('<Button-1>', lambda event:
                            self.view.update_record(self.entry_name.get(),
                            self.entry_phone.get(),
                            self.entry_email.get(),
                            self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>', lambda event: self.destroy(), add="+")
        self.btn_upd.place(x=200, y=170)

    # Подгрузка данных в форму
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('''SELECT * FROM users WHERE id=?''', (id, ))

        # Получаем доступ к первой записи из выборки
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

################################################################################################
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Поиск")
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

#####################################################################################################

        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

#########################################################################################
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=70)

        self.btn_search = ttk.Button(self, text="Найти")
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_name.get()))

########################################################################################################
# Класс БД
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('staff.db')
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT,
            salary TEXT
            )"""
        )
        self.conn.commit()

    def insert_data(self, name, phone, email, salary):
        self.cur.execute("""INSERT INTO users (name, phone, email, salary) VALUES(?, ?, ?, ?)""", (name, phone, email, salary))
        self.conn.commit()


# Окошко
if __name__ == '__main__':
    root = tk.Tk()
    # Экземпляр класса DB
    db= DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')      # Заголовок
    root.geometry("665x450")            # Размер окна
    root.resizable(False, False)        # Не даём открыть в полный экран и растягивать окно
    root.configure(bg='White')
    root.mainloop() 