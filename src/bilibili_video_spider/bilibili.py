from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import subprocess as sub
import threading

import tkinter.messagebox
from spider import Spider

spider = Spider()

top = Tk()
top.title("Bilibili视频下载器 for 可爱的猪娃")

# 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央,其中width和height为界面宽和高
width = 600
height = 500
screenwidth = top.winfo_screenwidth()
screenheight = top.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
top.geometry(alignstr)

# 阻止窗口调整大小
top.resizable(0, 0)
# 设置窗口图标
top.iconbitmap('./source/pig.ico')

# 框架布局
# frame_root = Frame(top)
# frame_left = Frame(frame_root)
# frame_right = Frame(frame_root)

# frame_left.pack(side=LEFT)
# frame_right.pack(side=RIGHT)
# frame_root.pack()
# , anchor=N

tip1 = Label(top, text='请输入视频链接：         ', font=('楷体', 20)).place(x=20, y=20, anchor=NW)
input_url = Entry(top, bg='#F7F3EC').place(x=20, y=60, width=480, height=30, anchor=NW)
get_list_button = Button(top, text='搜索', font=('楷体', 15), command=lambda: thread_it(search)). \
    place(x=520, y=60, height=30, anchor=NW)


# tip2 = Label(frame_left, text='请选择保存位置：         ', font=('楷体', 25)).place(x=10, y=100, anchor=NW)
# 保存地址输入框
# input_save_address = Entry(frame_left, bg='#F7F3EC')
# input_save_address.pack(ipadx=159, ipady=8, padx=20, anchor=W)

# 搜索按钮，输入url搜索相关的视频
# get_list_button = Button(frame_right, text='搜索', font=('楷体', 15), command=lambda: thread_it(search))
# get_list_button.pack(pady=10, side=TOP, anchor=W)
# “浏览文件夹”按钮
# browse_folder_button = Button(frame_right, text='浏览', font=('楷体', 15), command=lambda: thread_it(browse_folder))
# browse_folder_button.pack(pady=10, side=TOP, anchor=W)

# 查询出的视频信息
# video_info_list = Listbox(frame_left, width=65).pack(padx=20, pady=10)


def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


def search():
    url = input_url.get()
    if not url:
        tkinter.messagebox.showerror('提示', '视频地址不能为空？')
    else:
        print(spider.get_playlist(url))


def download():
    pass


# 浏览本地文件夹，选择保存位置
def browse_folder():
    # 浏览选择本地文件夹
    save_address = filedialog.askdirectory()
    # 把获得路径，插入保存地址输入框（即插入input_save_address输入框）
    input_save_address.insert(0, save_address)


top.mainloop()
