import re
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from tkinter import *
import os


def dismiss(win):
    win.grab_release()
    win.destroy()
def password_code(password):
    key = 3
    coded_password = ""
    for i in password:
        coded_password_temp = chr(ord(i) + key)
        coded_password += coded_password_temp
        key = -key + 1
    return coded_password


def open_file():
    try:
        text = open("useripass.txt", "r+")
        return text
    except FileNotFoundError:
        try:
            text = open("useripass.txt", "w")
            text.close()
            text = open("useripass.txt", "r+")
            return text
        except FileNotFoundError:
            text = open("useripass.txt", "r+")
            return text


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.create_login_widgets()
        self.users = {}

        button_style = ttk.Style()
        button_style.configure("my.TButton", font="Verdana 12")

    def create_login_widgets(self):
        self.label = Label(text="Для начала программы введите логин и пароль", font="Verdana 16 bold")

        self.username_label = Label(self.root, text="Логин:", font="Verdana 15")
        self.username_entry = Entry(self.root, width=30, justify="center")

        self.password_label = Label(self.root, text="Пароль:", font="Verdana 15")
        self.password_entry = Entry(self.root, width=30, justify="center", show="*")

        self.register_button = Button(self.root, text="Регистрация", command=self.register_user)

        self.login_button = Button(self.root, text="Вход", command=self.authenticate_user)



        self.label.place(x=65, y=25)
        self.username_label.place(x=310, y=55)
        self.username_entry.place(x=255, y=85)
        self.password_label.place(x=310, y=105)
        self.password_entry.place(x=255, y=135)
        self.login_button.place(x=260, y=165, width=180)
        self.register_button.place(x=260, y=195, width=180)

    def register_user(self):
        login = self.username_entry.get()
        password_raw = self.password_entry.get()
        password = password_code(password_raw)

        if len(login) == 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите желаемые логин и пароль")

        elif len(login) == 0 and len(password) != 0:
            messagebox.showwarning(title="Ошибка", message="Введите логин")

        elif len(login) != 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите пароль")

        else:
            file = open_file()
            temp = file.readline()[:-1].split(' ')

            while True:
                if temp != [""]:
                    self.users[temp[0]] = temp[1]
                    temp = file.readline()[:-1].split(' ')
                else:
                    break

            flag_reg = False

            for i in self.users.items():
                l, p = i
                if login == l:
                    flag_reg = True

            if not flag_reg:
                file = open_file()
                file.seek(0, os.SEEK_END)
                file.write(f'{login} {password}\n')
                file.close()

                for widget in self.root.winfo_children():
                    widget.destroy()

                Label(self.root, text=f"Вы успешно зарегистрировались!",
                      font="Verdana 16 bold").place(x=165, y=60)
                button = ttk.Button(self.root, text="Выбрать файл", style="my.TButton", command=self.create_file_selection_widgets)
                button.place(x=290, y=170)
            else:
                messagebox.showwarning(title="Ошибка", message="Такой аккаунт уже существует")

    def authenticate_user(self):
        login = self.username_entry.get()
        password_raw = self.password_entry.get()
        password = password_code(password_raw)

        if len(login) == 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите логин и пароль")

        elif len(login) == 0 and len(password) != 0:
            messagebox.showwarning(title="Ошибка", message="Введите логин")

        elif len(login) != 0 and len(password) == 0:
            messagebox.showwarning(title="Ошибка", message="Введите пароль")

        else:
            file = open_file()
            a = file.readline()[:-1].split(" ")

            while True:
                if a != [""]:
                    self.users[a[0]] = a[1]
                    a = file.readline()[:-1].split(" ")
                else:
                    break

            flag_reg = False
            for i in self.users.items():
                login_check, password_check = i
                if login == login_check and password == password_check:
                    flag_reg = True
                    break

            if flag_reg:
                for widget in self.root.winfo_children():
                    widget.destroy()

                Label(self.root, text="Вы успешно авторизировались!", font="Verdana 16 bold").place(x=175, y=60)
                button = ttk.Button(self.root, text="Выбрать файл", style="my.TButton", command=self.create_file_selection_widgets)
                button.place(x=300, y=170)

            else:
                messagebox.showwarning(title="Ошибка", message="Неверный логин или пароль")

    def create_file_selection_widgets(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            data = self.read_file(file_path)
            start_node = self.convert_to_int(data[self.convert_to_int(data[0]) + 1])
            if start_node == (self.convert_to_int(data[self.convert_to_int(data[0]) + 2])):
                messagebox.showwarning(title="Ошибка", message="Начальная и конечная вершины совпадают\n Выберите другой файл")
            else:
                shortest_paths = self.dijkstra_algorithm(data, start_node)
                if shortest_paths == "Путь не существует":
                    messagebox.showwarning(title="Ошибка", message="Между указанными точками не существует пути\n Выберите другой файл")
                else:
                    self.create_graph(data, shortest_paths)

    def read_file(self, file_path):
        file = open(file_path, "r")
        values = file.read().split("\n")
        data = []
        for key in values:
            value = re.findall(r"[-+]?\d*\.\d+|\d+", key)
            if value:
                data.append(value)
        return data

    def convert_to_int(self, value):
        return int(''.join(map(str, value)))

    def dijkstra_algorithm(self, data, start_node):
        n = self.convert_to_int(data[0])
        W = [[int(i) for i in row] for row in data[1:n + 1]]
        start = self.convert_to_int(data[n + 1]) - 1
        finish = self.convert_to_int(data[n + 2]) - 1
        INF = 1e8
        visited = [False] * n
        dist = [INF] * n
        dist[start] = 0
        while False in visited:
            u = self.go_from(dist, visited)
            for v in range(n):
                if W[u][v] != 0 and not visited[v]:
                    dist[v] = min(dist[v], dist[u] + W[u][v])
            visited[u] = True

        if INF in dist:
            return "Путь не существует"
        else:
            return dist[finish]

    def go_from(self, dist, visited):
        index = 0
        dist_min = float('inf')
        for i in range(len(dist)):
            if dist[i] < dist_min and not visited[i]:
                dist_min = dist[i]
                index = i
        return index

    def create_graph(self, data, shortest_paths):
        G = nx.DiGraph()
        n = self.convert_to_int(data[0])
        edges = []
        for i in range(n):
            for j in range(n):
                if self.convert_to_int(data[i + 1][j]) != 0:
                    edges.append((i, j, self.convert_to_int(data[i + 1][j])))
        G.add_weighted_edges_from(edges)

        pos = nx.spring_layout(G, seed=10)
        labels = {}
        for i in range(n):
            labels[i] = str(i+1)

        edge_labels = {(i, j): str(G[i][j]['weight']) for i, j in G.edges}

        fig, ax = plt.subplots()
        nx.draw(G, pos, with_labels=False, node_color='skyblue', node_size=1500, arrowsize=20, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax)
        nx.draw_networkx_labels(G, pos, labels, font_size=20, font_color='black', ax=ax,
                                verticalalignment='bottom')

        win = Toplevel()
        w = win.winfo_screenwidth()
        h = win.winfo_screenheight()
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 360  # смещение от середины
        h = h - 300
        win.geometry(f'720x600+{w}+{h}')
        win.title('')
        win.resizable(False, False)
        win.protocol('WM_DELETE_WINDOW', lambda: dismiss(win))
        win.grab_set()

        shortest_path_label = Label(win, text=f"Кратчайшее расстояние до точки: {shortest_paths}")
        shortest_path_label.pack()
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack()
        ttk.Button(win, text="Выбрать другой файл", command=lambda: (win.destroy())).pack()
        ttk.Button(win, text="Выбрать другой аккаунт", command=lambda: (win.destroy(), self.root.destroy(), main())).pack()




def main():
    root = Tk()
    root.title("")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 360  # смещение от середины
    h = h - 150
    root.geometry(f'720x300+{w}+{h}')
    root.resizable(False, False)
    app = GraphApp(root)
    root.mainloop()



if __name__ == "__main__":
    main()