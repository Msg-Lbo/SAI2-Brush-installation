import ctypes
import os
from ctypes import wintypes
import psutil
import py7zr
from download import download_optimized


# 判断程序是否运行
def proc_exist(process_name):  # 判断程序是否在运行
    for pid in psutil.pids():
        try:
            if psutil.Process(pid).name() == process_name:
                return pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


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
    file_url = "https://pan.ylmty.cc/d/115/SYSTEMAX%20Software%20Development.7z"
    file_name = env_var + "/SYSTEMAX Software Development.7z"
    perform_download_and_install(env_var, file_url, file_name)


if __name__ == "__main__":
    main()
