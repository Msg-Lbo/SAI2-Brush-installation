import requests
from tqdm import tqdm


def download_optimized(url: str, fname: str):
    # 验证URL
    if not url or not fname:
        print("URL和文件名不能为空")
        return False

    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()  # 检查请求是否成功
        total = int(resp.headers.get('content-length', 0))

        # 使用ASCII字符，并设定进度条宽度为50
        with open(fname, 'wb') as file, tqdm(
                desc=fname,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                ascii=True,  # 使用ASCII字符
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
        return True
    except requests.RequestException as e:
        print(f"下载失败，发生错误: {str(e)}")
        return False
