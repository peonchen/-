import os #提供了访问操作系统功能的接口
import json    #通过解析和序列化josn文件
import mysql.connector   #mysql连接
from mysql.connector import Error   #mysql异常报错
import hashlib   # 提供md5加密
import getpass    #输入密码不可见

class SimpleFileSystem:
    def __init__(self, filename, username):
        # 文件名
        self.filename = filename
        # 用户名
        self.username = username
        # 根目录
        self.file_system = {username: {"type": "directory", "contents": {}}}
        # 当前路径内容
        self.current_directory = self.file_system[self.username]["contents"]
        # 路径
        self.path = [username]
        # 加载文件系统
        self.load_file_system()
    # 加载文件
    def load_file_system(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.file_system = json.load(f)
                if self.username not in self.file_system:
                    self.file_system[self.username] = {"type": "directory", "contents": {}}
                self.current_directory = self.file_system[self.username]["contents"]
                for directory in self.path[1:]:
                    self.current_directory = self.current_directory[directory]["contents"]
        else:
            self.file_system[self.username] = {"type": "directory", "contents": {}}
            self.save_file_system()
    # 保存文件
    def save_file_system(self):
        with open(self.filename, 'w') as f:
            json.dump(self.file_system, f, indent=4)
    # 创建文件
    def create_file(self, filename, content=""):
        if filename in self.current_directory:
            print(f"File '{filename}' already exists.")
        else:
            self.current_directory[filename] = {"type": "file", "content": content}
            self.save_file_system()
    # 写入文件
    def write_file(self, filename, content):
        if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
            self.current_directory[filename]["content"] = content
            self.save_file_system()
        else:
            print(f"File '{filename}' not found.")
    # 删除文件
    def delete_file(self, filename):
        if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
            del self.current_directory[filename]
            self.save_file_system()
        else:
            print(f"File '{filename}' not found.")
    # 删除文件夹
    def delete_directory(self, directory):
        if directory in self.current_directory and self.current_directory[directory]["type"] == "directory":
            del self.current_directory[directory]
            self.save_file_system()
        else:
            print(f"directory '{directory}' not found.")
    # 新建目录
    def create_directory(self, directory_name):
        if directory_name in self.current_directory:
            print(f"Directory '{directory_name}' already exists.")
        else:
            self.current_directory[directory_name] = {"type": "directory", "contents": {}}
            self.save_file_system()
    # 输出文件
    def print_file(self, filename):
        if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
            print(self.current_directory[filename]["content"])
        else:
            print(f"File '{filename}' not found.")
    # 打印路径
    def showpath(self):
        return "/" + "/".join(self.path)
    # 切换目录
    def change_directory(self, directory_name):
        if directory_name == "..":
            if len(self.path) > 1:
                self.path.pop()
                self.current_directory = self.file_system[self.username]["contents"]
                for directory in self.path[1:]:
                    self.current_directory = self.current_directory[directory]["contents"]
            else:
                print("Already at root directory.")
        elif directory_name in self.current_directory:
            if self.current_directory[directory_name]["type"] == "directory":
                self.current_directory = self.current_directory[directory_name]["contents"]
                self.path.append(directory_name)
            else:
                print(f"'{directory_name}' is not a directory.")
        else:
            print(f"Directory '{directory_name}' not found.")
    # 列出当前目录
    def list_directory(self):
        return list(self.current_directory.keys())
    # 重命名
    def rename_file(self, old_filename, new_filename):
        if old_filename in self.current_directory:
            if new_filename in self.current_directory:
                print(f"File '{new_filename}' already exists.")
            else:
                self.current_directory[new_filename] = self.current_directory.pop(old_filename)
                self.save_file_system()
        else:
            print(f"File '{old_filename}' not found.")
    # 移动
    def move_file(self, filename, target_directory_path):
        if filename in self.current_directory:
            target_directory = self.traverse_path(target_directory_path)
            if target_directory is not None and target_directory["type"] == "directory":
                target_directory["contents"][filename] = self.current_directory.pop(filename)
                self.save_file_system()
            else:
                print(f"Target directory '{target_directory}' not found.")
        else:
            print(f"File '{filename}' not found.")
    # 移动子函数
    def traverse_path(self, path):
        #  拆分路径
        components = path.split('/')[1:]
        # 修改当前目录
        current_directory = self.file_system[self.username]
        # 跳过root
        components = components[1:] 
        # 不断切换当前目录，找到目的路径是否存在
        for component in components:
            if component == "":
                return None
            if component:
                if component in current_directory["contents"] and current_directory["contents"][component]["type"] == "directory":
                    current_directory = current_directory["contents"][component]
                else:
                    return None
        return current_directory
# md5加密
def md5_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def login(is_register):
    username = input("请输入用户名：")
    # 密码不可见
    password = getpass.getpass("请输入密码：")
    # 密码用md5 加密
    password = md5_hash(password)
    flag = 0
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="chen2630",
            database="czxt"
        )
        cursor = db.cursor()
        # 登录
        if not is_register:
            query = "SELECT * FROM user WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            if result:
                print(f"登录成功：欢迎 {username}!")
                flag = username
            else:
                print("登录失败：账户名或密码不正确。")
        # 注册
        else:
            query = "SELECT * FROM user WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                print("注册失败：用户名已存在。")
            else:
                query = "INSERT INTO user(`username`,`password`) VALUES(%s,%s)"
                cursor.execute(query, (username, password))
                db.commit()
                print("注册成功")
                flag = username
    # 捕捉异常
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        if 'db' in locals() or 'db' in globals():
            db.close()
        return flag

def operate(username):
    if username == 0:
        return 0
    fs = SimpleFileSystem("root.json", username)
    while True:
        command = input("$ ")
        argnum = len(command.split())
        if command == "exit" and argnum == 1:   # 退出
            break
        elif command.startswith("cd") and argnum == 2:   #切换目录
            directory_name = command.split(" ")[1]
            fs.change_directory(directory_name)
        elif command.startswith("mkdir") and argnum == 2:   #新建文件夹
            directory_name = command.split(" ")[1]
            fs.create_directory(directory_name) 
        elif command.startswith("touch") and argnum == 3:    #新建文件
            filename = command.split(" ")[1]
            content = " ".join(command.split(" ")[2:])
            fs.create_file(filename, content)
        elif command.startswith("vim") and argnum == 3:    # 修改文件
            filename = command.split(" ")[1]
            content = " ".join(command.split(" ")[2:])
            fs.write_file(filename, content)
        elif command.startswith("ls") and argnum == 1:    #打印当前目录
            print(fs.list_directory())
        elif command.startswith("cat") and argnum == 2:   #输出文件内容
            filename = command.split(" ")[1]
            fs.print_file(filename)
        elif command.startswith("rm") and argnum == 3:    # 删除文件（夹）
            if command.split(" ")[1] == "-d":
                directory_name = command.split(" ")[2]   
                fs.delete_directory(directory_name)
            elif command.split(" ")[1] == "-f":
                filename = command.split(" ")[2]
                fs.delete_file(filename)
            else:
                print("Invalid command.")
        elif command.startswith("pwd") and argnum == 1:   # 打印当前路径
            print(fs.showpath())
        elif command.startswith("mv") and argnum == 4:    
            if command.split(" ")[1] == "-f":        #重命名文件（夹）
                old_filename = command.split(" ")[2]
                new_filename = command.split(" ")[3]
                fs.rename_file(old_filename, new_filename)
            elif command.split(" ")[1] == "-d":       # 移动文件
                filename = command.split(" ")[2]
                target_path = command.split(" ")[3]
                fs.move_file(filename, target_path)
            else:
                print("Invalid command.")
        elif command.startswith("useradd") and argnum == 1:
            login(1)
        else:
            print("Invalid command.")

if __name__ == "__main__":
    # mysql验证登录
    # operate(login(0))
    # 直接登录
    operate('root')
    # operate('chen')
