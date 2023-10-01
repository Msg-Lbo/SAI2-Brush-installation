import ctypes
import os
import shutil
import sys
from ctypes import wintypes

import psutil
import py7zr

from download import download_optimized

time = "当前版本更新于：2023-8-18--v3.5.1"


# 判断程序是否运行
def proc_exist(process_name):  # 判断程序是否在运行
    for pid in psutil.pids():
        try:
            if psutil.Process(pid).name() == process_name:
                return pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


# 备份主函数
def backup_directory(source_path, backup_path):  # 备份文件夹
    try:
        if os.path.exists(source_path):
            print("正在备份当前文件夹...")
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            shutil.copytree(source_path, backup_path)
            print("备份完成...")
            return True
        else:
            print(f"没有找到可备份文件:\n{source_path}")
            print("将进行下一步...")
            return False
    except Exception as e:
        print(f"备份失败，发生错误: {str(e)}\n请联系管理员..")
        return False


# 打印信息主函数
def print_initial_message():  # 打印提示信息
    os.system(f"title {time}")

    # 定义重复的消息
    repeated_message = (
        "自己的笔刷一定要备份好，可以用该工具的备份功能一键备份，然后自己\033[32m妥善保管笔刷\033[0m，笔刷丢失概不负责\n"
    )

    print(
        "----------\033[31m提示\033[0m----------\n\n"
        "安装过程中不要打开SAI2，如果你是第二次使用，也请不要打开笔刷压缩包\n\n"
        "安装笔刷之前，请确保您安装的是本群提供的最新版SAI2或官网下载的SAI2\n\n"
        "如果您安装的是本群提供的SAI2，安装笔刷之前请检查以前保存的*.sai2文件能否正常打开\n\n"
        "如不能打开，请在群里@群主\n\n"
        f"{repeated_message * 3}"  # 重复3次
        "----------\033[31m提示\033[0m----------"
    )


# 同意协议主函数
def get_user_confirmation():  # 同意协议
    is_ok = input("我已阅读以上提示(please input 'ok')：")
    if is_ok == "ok":
        return True
    else:
        os.system('cls')
        print("我看你是没看懂哦..再来一次？(按下任意键关闭)")
        os.system('pause')
        sys.exit()


# 调用备份
def perform_backup(p_env_var):
    source_path = os.path.join(p_env_var, "SYSTEMAX Software Development")
    backup_path = os.path.join(p_env_var, "笔刷包备份/SYSTEMAX Software Development")
    os.system("cls")
    backup_directory(source_path, backup_path)
    os.system('pause')


# 还原
def perform_restore(p_env_var):  # 还原笔刷
    backup_path = os.path.join(p_env_var, "笔刷包备份/SYSTEMAX Software Development")
    if os.path.exists(backup_path):
        try:
            os.system("cls")
            print("正在恢复笔刷...")
            shutil.rmtree(get_documents_folder() + "/SYSTEMAX Software Development")
            shutil.copytree(backup_path, os.path.join(p_env_var, "SYSTEMAX Software Development"))
            print("笔刷恢复完成...")
        except FileNotFoundError:
            print("没有找到您备份的笔刷，真的备份了吗？")
    else:
        print("没有找到您备份的笔刷，真的备份了吗？")
    os.system('pause')


# 定义解压缩文件的函数
def extract_with_py7zr(file_path, extract_path):
    with py7zr.SevenZipFile(file_path, mode='r') as archive:
        archive.extractall(path=extract_path)


# 调用下载
def perform_download_and_install(p_env_var, file_url, file_name):
    os.system("cls")
    print("正在准备下载...")
    # 下载文件
    if download_optimized(file_url, file_name):
        # 解压缩文件
        print("解压...")
        unzip_path = os.path.join(p_env_var)
        extract_with_py7zr(file_name, unzip_path)
        print("笔刷安装完成")
    else:
        print("笔刷下载失败，请重试或联系管理员")
    os.system('pause')


def get_documents_folder():
    CSIDL_PERSONAL = 5  # "Documents" 文件夹的标识符
    SHGFP_TYPE_CURRENT = 0  # 获取当前路径，而不是默认路径

    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)

    return buf.value


def main():
    # 示例数据
    env_var = get_documents_folder()
    file_url = "https://pan.ylmty.cc/d/%E9%98%BF%E9%87%8C%E4%BA%91%E7%9B%98%F0%9F%94%91/SAI2/SYSTEMAX%20Software%20Development.7z"
    file_name = env_var + "/SYSTEMAX Software Development.7z"

    print_initial_message()
    get_user_confirmation()

    while True:
        os.system("cls")
        print("请选择操作：")
        print("1 - 备份笔刷")
        print("2 - 恢复笔刷")
        print("3 - 下载安装笔刷")
        print("0 - 退出")
        choice = input("请输入选项编号：")

        if choice == "1":
            perform_backup(env_var)
        elif choice == "2":
            perform_restore(env_var)
        elif choice == "3":
            perform_download_and_install(env_var, file_url, file_name)
        elif choice == "0":
            print("感谢使用！再见！")
            break
        else:
            print("无效的选项，请重新选择。")
            os.system('pause')


if __name__ == "__main__":
    main()
