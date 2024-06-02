import os
import json

class SimpleFileSystem:
    def __init__(self, filename):
        # 文件名
        self.filename = filename
        # 根目录
        self.file_system = {"root": {}}
        # 当前路径内容
        self.current_directory = self.file_system["root"]
        # 路径
        self.path = ["root"]
        # 加载文件系统
        self.load_file_system()
    def printself(self):
        print(self.current_directory)
        print(self.path)
    def load_file_system(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.file_system = json.load(f)
                self.current_directory = self.file_system["root"]
                for directory in self.path[1:]:
                    self.current_directory = self.current_directory[directory]

    def save_file_system(self):
        with open(self.filename, 'w') as f:
            json.dump(self.file_system, f, indent=4)

    def create_file(self, filename, content=""):
        if filename in self.current_directory:
            print(f"File '{filename}' already exists.")
        else:
            self.current_directory[filename] = content
            self.save_file_system()

    def read_file(self, filename):
        if filename in self.current_directory:
            return self.current_directory[filename]
        else:
            print(f"File '{filename}' not found.")
            return None

    def write_file(self, filename, content):
        if filename in self.current_directory:
            self.current_directory[filename] = content
            self.save_file_system()
        else:
            print(f"File '{filename}' not found.")

    def delete_file(self, filename):
        if filename in self.current_directory:
            del self.current_directory[filename]
            self.save_file_system()
        else:
            print(f"File '{filename}' not found.")

    def create_directory(self, directory_name):
        if directory_name in self.current_directory:
            print(f"Directory '{directory_name}' already exists.")
        else:
            self.current_directory[directory_name] = {}
            self.save_file_system()

    def change_directory(self, directory_name):
        if directory_name == "..":
            if len(self.path) > 1:
                self.path.pop()
                self.current_directory = self.file_system["root"]
                for directory in self.path[1:]:
                    self.current_directory = self.current_directory[directory]
            else:
                print("Already at root directory.")
        elif directory_name in self.current_directory:
            if isinstance(self.current_directory[directory_name], dict):
                self.current_directory = self.current_directory[directory_name]
                self.path.append(directory_name)
            else:
                print(f"'{directory_name}' is not a directory.")
        else:
            print(f"Directory '{directory_name}' not found.")
    # 列目录
    def list_directory(self):
        return list(self.current_directory.keys())
fs = SimpleFileSystem("root.txt")
print(fs.list_directory())
fs.create_directory("dir1")
fs.create_directory("dir2")
fs.printself()
fs.change_directory("dir1")
fs.printself()
fs.create_file("file1.txt", "Hello, World!")
fs.create_file("file2.txt", "This is a test file.")
fs.printself()
fs.create_directory("dir1_dir")
print("目录")
print(fs.list_directory())
fs.change_directory("dir1_dir")
fs.printself()
fs.create_file("file3.txt", "This is another test file.")
fs.printself()
print("1")
fs.change_directory("..")
fs.printself()
print("2")
fs.change_directory("..")
fs.printself()
fs.change_directory("dir2")
fs.printself()
fs.create_file("file4.txt", "This is a new test file.")
fs.printself()
fs.create_file("file5.txt", "This is another new test file.")
fs.printself()
fs.create_directory("dir2_dir")
fs.printself()
fs.change_directory("dir2_dir")
fs.create_file("file6.txt", "This is a test file in dir2_dir.")
fs.printself()
fs.change_directory("..")
fs.printself()
fs.change_directory("..")
fs.printself()
print(fs.list_directory())
