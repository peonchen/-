import os
import json

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
    def printself(self):
        print(self.current_directory)
        print(self.path)
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

    def save_file_system(self):
        with open(self.filename, 'w') as f:
            json.dump(self.file_system, f, indent=4)

    def create_file(self, filename, content=""):
        if filename in self.current_directory:
            print(f"File '{filename}' already exists.")
        else:
            self.current_directory[filename] = {"type":"file", "content":content}
            self.save_file_system()

    def read_file(self, filename):
        if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
            return self.current_directory[filename]["content"]
        else:
            print(f"File '{filename}' not found.")
            return None

    def write_file(self, filename, content):
        if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
            self.current_directory[filename]["content"] = content
            self.save_file_system()
        else:
            print(f"File '{filename}' not found.")

    def delete_file(self, filename):
        if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
            del self.current_directory[filename]
            self.save_file_system()
        else:
            print(f"File '{filename}' not found.")

    def create_directory(self, directory_name):
        if directory_name in self.current_directory:
            print(f"Directory '{directory_name}' already exists.")
        else:
            self.current_directory[directory_name] = {"type":"directory", "contents":{}}
            self.save_file_system()
    def print_file(self,filename):
        if filename in self.current_directory and self.current_directory[filename]["type"] == "file":
            print(self.current_directory[filename]["content"])
        else:
            print(f"File '{filename}' not found.")
    def showpath(self):
        return "/"+"/".join(self.path)

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
if __name__ == "__main__":
    fs = SimpleFileSystem("root.txt")
    while True:
        command = input("$ ")
        argnum = len(command.split())
        if command == "exit" and argnum == 1:
            break
        elif command.startswith("cd") and argnum == 2:
            directory_name = command.split(" ")[1]
            fs.change_directory(directory_name)
        elif command.startswith("mkdir") and argnum == 2:
            directory_name = command.split(" ")[1]
            fs.create_directory(directory_name)
        elif command.startswith("touch") and argnum == 3:
            filename = command.split(" ")[1]
            content = " ".join(command.split(" ")[2:])
            fs.create_file(filename, content)
        elif command.startswith("vim") and argnum == 3:
            filename = command.split(" ")[1]
            content = " ".join(command.split(" ")[2:])
            fs.write_file(filename, content)        
        elif command.startswith("ls") and argnum == 1:
            print(fs.list_directory())
        elif command.startswith("cat") and argnum == 2:
            filename = command.split(" ")[1]
            fs.print_file(filename)
        elif command.startswith("rm") and argnum == 3:
            if command.split(" ")[1] == "-d":
                directory_name = command.split(" ")[2]
                fs.delete_directory(directory_name)
            elif command.split(" ")[1] == "-f":
                filename = command.split(" ")[2]
                fs.delete_file(filename)
            else:
                print("Invalid command.")
        elif command.startswith("pwd") and argnum == 1:
            print(fs.showpath())
        else:
            print("Invalid command.")
