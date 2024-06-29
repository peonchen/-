import os
import json
import mysql.connector
from mysql.connector import Error
import hashlib
import getpass
class SimpleFileSystem:
    def __init__(self, filename):
        # 文件名
        self.filename = filename
        # 根目录
        self.file_system = {"root": {"type":"directory", "contents":{}}}
        # 当前路径内容
        self.current_directory = self.file_system["root"]["contents"]
        # 路径
        self.path = ["root"]
        # 加载文件系统
        self.load_file_system()
    # 测试函数
    def printself(self):
        print(self.current_directory)
        print(self.path)
    # 加载文件
    def load_file_system(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.file_system = json.load(f)
                # print("测试")
                # self.printself()
                self.current_directory = self.file_system["root"]["contents"]
                for directory in self.path[1:]:
                    self.current_directory = self.current_directory[directory]["contents"]
                # print("测试")
                # self.printself()
    # 保存文件
    def save_file_system(self):
        with open(self.filename, 'w') as f:
            json.dump(self.file_system, f, indent=4)
    # 创建文件
    def create_file(self, filename, content=""):
        if filename in self.current_directory:
            print(f"File '{filename}' already exists.")
        else:
            self.current_directory[filename] = {"type":"file", "content":content}
            self.save_file_system()
    #读取文件
    # def read_file(self, filename):
    #     if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
    #         return self.current_directory[filename]["content"]
    #     else:
    #         print(f"File '{filename}' not found.")
    #         return None
    # 修改文件
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
    # 创建目录
    def create_directory(self, directory_name):
        if directory_name in self.current_directory:
            print(f"Directory '{directory_name}' already exists.")
        else:
            self.current_directory[directory_name] = {"type":"directory", "contents":{}}
            self.save_file_system()
    # 打印当前文件
    def print_file(self,filename):
        if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
            print(self.current_directory[filename]["content"])
        else:
            print(f"File '{filename}' not found.")
    # 打印路径
    def showpath(self):
        return "/"+"/".join(self.path)
    # 切换目录
    def change_directory(self, directory_name):
        if directory_name == "..":
            if len(self.path) > 1:
                self.path.pop()
                self.current_directory = self.file_system["root"]["contents"]
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
    # 列目录
    def list_directory(self):
        return list(self.current_directory.keys())
    # 修改文件名
    def rename_file(self,old_filename,new_filename):
        if old_filename in self.current_directory:
            if new_filename in self.current_directory:
                print(f"File '{new_filename}' already exists.")
            else:
                self.current_directory[new_filename] = self.current_directory.pop(old_filename)
                self.save_file_system() 
        else:
            print(f"File '{old_filename}' not found.")
    # 移动文件
    def move_file(self,filename,target_path):
        if filename in self.current_directory:
            target_directory_path,target_filename = os.path.split(target_path)
            target_directory = self.traverse_path(target_directory_path)
            if target_directory is not None and target_directory["type"] == "directory":
                target_directory["contents"][target_filename] = self.current_directory.pop(filename)
                self.save_file_system()
            else:
                print(f"Target directory '{target_directory}' not found.")
        else:
            print(f"File '{filename}' not found.")
    def traverse_path(self, path):
        components = path.split('/')[1:]
        # print(components)
        current_directory = self.file_system["root"]
        
        # Handle absolute path starting with '/'
        components = components[1:]  # Skip the first empty component
        # print(components)
        for component in components:
            if component:
                if component in current_directory["contents"] and current_directory["contents"][component]["type"] == "directory":
                    current_directory = current_directory["contents"][component]
                else:
                    return None
        
        return current_directory
def md5_hash(password):
    # 使用 MD5 加密密码
    return hashlib.md5(password.encode()).hexdigest()
def login():
    username = input("请输入用户名：")
    password = getpass.getpass("请输入密码：")
    password=md5_hash(password)
    # print(password)
    flag = 0
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="chen2630",
            database="czxt"
        )
        # 连接成功后可以执行数据库操作
        cursor = db.cursor()
        query = "SELECT * FROM user WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone() 
        if result:
            print(f"登录成功：欢迎 {username}!")
            flag = 1
        else:
            print("登录失败：账户名或密码不正确。")
        
        # 处理查询结果等操作
        
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        # 关闭数据库连接
        if 'db' in locals() or 'db' in globals():
            db.close()
        return flag
def oprate():
    fs = SimpleFileSystem("root.txt")
    while True:
        command = input("$ ")
        argnum = len(command.split())
        if command == "exit" and argnum == 1:  # 退出
            break
        elif command.startswith("cd") and argnum == 2:   #切目录
            directory_name = command.split(" ")[1]
            fs.change_directory(directory_name)
        elif command.startswith("mkdir") and argnum == 2:  #创建文件夹
            directory_name = command.split(" ")[1]
            fs.create_directory(directory_name)
        elif command.startswith("touch") and argnum == 3:  #创建文件
            filename = command.split(" ")[1]
            content = " ".join(command.split(" ")[2:])
            fs.create_file(filename, content)
        elif command.startswith("vim") and argnum == 3:   #修改文件
            filename = command.split(" ")[1]
            content = " ".join(command.split(" ")[2:])
            fs.write_file(filename, content)        
        elif command.startswith("ls") and argnum == 1:   #列出目录
            print(fs.list_directory())
        elif command.startswith("cat") and argnum == 2:  #读出文件内容
            filename = command.split(" ")[1]
            fs.print_file(filename)
        elif command.startswith("rm") and argnum == 3:    #删除文件
            if command.split(" ")[1] == "-d":
                directory_name = command.split(" ")[2]
                fs.delete_directory(directory_name)
            elif command.split(" ")[1] == "-f":
                filename = command.split(" ")[2]
                fs.delete_file(filename)
            else:
                print("Invalid command.")
        elif command.startswith("pwd") and argnum == 1:   # 打印路径
            print(fs.showpath())
        elif command.startswith("mv") and argnum == 4:
            if command.split(" ")[1] == "-f":
                old_filename = command.split(" ")[2]
                new_filename = command.split(" ")[3]
                fs.rename_file(old_filename,new_filename)
            elif command.split(" ")[1] == "-d":
                filename = command.split(" ")[2]
                target_path = command.split(" ")[3]
                fs.move_file(filename,target_path)
            else:
                print("Invalid command.")
        else:
            print("Invalid command.")

if __name__ == "__main__":          
    if(login()):
        oprate()
    