import time
import requests
import os
from originCode import qq_music_api
import random


class DownloadMusic:
    """
    音乐下载类，用于搜索和下载QQ音乐平台的歌曲

    功能：
    - 根据歌手名搜索歌曲
    - 获取歌曲播放URL
    - 检查文件是否已存在，避免重复下载
    - 下载歌曲到本地指定目录
    """

    def __init__(self, singer, page, num, download_dir=None):
        """
        初始化下载器

        参数:
            singer (str): 歌手名称
            page (int): 搜索页码
            num (int): 每页歌曲数量
            download_dir (str): 下载目录路径，默认为None
        """
        # 保存搜索参数为实例变量，便于后续使用
        self.singer = singer
        self.page = page
        self.num = num

        # 设置下载目录
        if download_dir is None:
            # 默认下载目录
            self.download_dir = r"C:\Users\32236\Desktop\music"
        else:
            self.download_dir = download_dir

        # 确保下载目录存在
        os.makedirs(self.download_dir, exist_ok=True)

        # 构建搜索请求数据
        self.data1 = {
            "comm": {
                "cv": 4747474,
                "ct": 24,
                "format": "json",
                "inCharset": "utf-8",
                "outCharset": "utf-8",
                "notice": 0,
                "platform": "yqq.json",
                "needNewCode": 1,
                "uin": 3223607546,
                "g_tk_new_20200303": 1188746000,
                "g_tk": 1188746000
            },
            "req_1": {
                "method": "DoSearchForQQMusicDesktop",
                "module": "music.search.SearchCgiService",
                "param": {
                    "remoteplace": "txt.yqq.top",
                    "searchid": "61292176913318089",  # 搜索ID，可考虑动态生成
                    "search_type": 0,
                    "query": singer,  # 搜索关键词（歌手名）
                    "page_num": page,  # 页码
                    "num_per_page": num  # 每页数量
                }
            }
        }

    def _get_safe_filename(self, songname, songID):
        """
        生成安全的文件名，并检查是否已存在

        参数:
            songname (str): 歌曲名称
            songID (str/int): 歌曲ID

        返回:
            tuple: (安全文件名, 完整文件路径, 是否已存在)
        """
        # 创建安全的文件名（移除非法字符）
        safe_filename = "".join(c for c in songname if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_filename:
            safe_filename = f"song_{songID}"  # 如果文件名无效，使用歌曲ID

        # 构建完整的文件路径
        file_path = os.path.join(self.download_dir, f"{safe_filename}.mp3")

        # 检查文件是否已存在
        file_exists = os.path.exists(file_path)

        return safe_filename, file_path, file_exists

    def main(self):
        """
        主执行函数，负责整个下载流程

        流程：
        1. 搜索歌手歌曲列表
        2. 遍历每首歌曲获取下载URL
        3. 检查文件是否已存在
        4. 下载歌曲文件到本地（仅当文件不存在时）
        """
        # 创建QQ音乐API实例
        qq_music = qq_music_api()

        # 执行搜索，获取歌曲列表
        search_result = qq_music.search_music(self.data1)

        # 检查搜索结果是否有效
        if not search_result or 'req_1' not in search_result:
            print("搜索失败，无法获取歌曲列表")
            return

        # 提取搜索结果中的数据部分
        data_body = search_result['req_1']['data']
        if 'body' not in data_body or 'song' not in data_body['body']:
            print("搜索结果格式异常")
            return

        # 获取歌曲列表数组
        dataArr = data_body['body']['song']['list']

        # 检查是否有歌曲
        if not dataArr:
            print(f"未找到歌手 '{self.singer}' 的歌曲")
            return

        # 创建新的API实例用于获取歌曲详情
        songData = qq_music_api()

        # 统计变量
        total_songs = len(dataArr)
        skipped_songs = 0
        downloaded_songs = 0
        error_songs = 0

        print(f"找到 {total_songs} 首歌曲，开始处理...")

        # 遍历每首歌曲，获取下载链接并下载
        for index, song_info in enumerate(dataArr, 1):
            # 检查歌曲基本信息是否完整
            if 'id' not in song_info or 'mid' not in song_info:
                print(f"[{index}/{total_songs}] 歌曲信息不完整，跳过")
                error_songs += 1
                continue

            # 提取歌曲基本信息
            songID = song_info['id']  # 歌曲ID
            biz_id = str(songID)  # 转换为字符串格式的业务ID
            songMID = song_info['mid']  # 歌曲MID
            guid = str(7785978040 + random.randint(1, 10))  # 生成随机GUID

            # 检查专辑信息
            if "album" not in song_info or "mid" not in song_info["album"]:
                print(f"[{index}/{total_songs}] 专辑信息不完整，跳过")
                error_songs += 1
                continue

            albumMid = song_info["album"]["mid"]  # 专辑MID
            songmid = [songMID]  # 歌曲MID列表

            # 检查歌曲名
            if "name" not in song_info:
                print(f"[{index}/{total_songs}] 歌曲名缺失，跳过")
                error_songs += 1
                continue

            songname = song_info["name"]  # 歌曲名称

            # 检查歌手信息
            if "singer" not in song_info or not song_info["singer"] or "name" not in song_info["singer"][0]:
                print(f"[{index}/{total_songs}] 歌手信息缺失，跳过")
                error_songs += 1
                continue

            singer = song_info["singer"][0]["name"]  # 歌手名称

            # 获取安全文件名并检查文件是否存在
            safe_filename, file_path, file_exists = self._get_safe_filename(songname, songID)

            # 如果文件已存在，跳过下载
            if file_exists:
                print(f"[{index}/{total_songs}] 歌曲 '{singer} - {songname}' 已存在，跳过下载")
                skipped_songs += 1
                continue

            # 构建获取歌曲详情的请求数据
            data = {
                "comm": {
                    "cv": 4747474,
                    "ct": 24,
                    "format": "json",
                    "inCharset": "utf-8",
                    "outCharset": "utf-8",
                    "notice": 0,
                    "platform": "yqq.json",
                    "needNewCode": 1,
                    "uin": 3223607546,
                    "g_tk_new_20200303": 1188746000,
                    "g_tk": 1188746000
                },
                "req_1": {  # 获取歌词信息
                    "module": "music.musichallSong.PlayLyricInfo",
                    "method": "GetPlayLyricInfo",
                    "param": {
                        "songMID": songMID,
                        "songID": songID
                    }
                },
                "req_2": {  # 获取评论数量
                    "method": "GetCommentCount",
                    "module": "music.globalComment.GlobalCommentRead",
                    "param": {
                        "request_list": [
                            {
                                "biz_type": 1,
                                "biz_id": biz_id,
                                "biz_sub_type": 0
                            }
                        ]
                    }
                },
                "req_3": {  # 获取专辑详情
                    "module": "music.musichallAlbum.AlbumInfoServer",
                    "method": "GetAlbumDetail",
                    "param": {
                        "albumMid": albumMid
                    }
                },
                "req_4": {  # 获取歌曲播放URL（关键请求）
                    "module": "music.vkey.GetEVkey",
                    "method": "GetUrl",
                    "param": {
                        "guid": guid,
                        "songmid": songmid,
                        "songtype": [0],
                        "uin": "3223607546",
                        "loginflag": 1,
                        "platform": "20",
                        "xcdn": 1,
                        "qdesc": "lq96kOgg"  # 固定参数
                    }
                }
            }

            # 发送请求获取歌曲详情数据
            urlData = songData.search_music(data)

            # 检查URL数据是否有效
            if not urlData or 'req_4' not in urlData or 'data' not in urlData['req_4']:
                print(f"[{index}/{total_songs}] 无法获取歌曲 '{songname}' 的URL信息，跳过")
                error_songs += 1
                continue

            # 提取URL信息
            midurlinfo_data = urlData['req_4']['data']
            if 'midurlinfo' not in midurlinfo_data or not midurlinfo_data['midurlinfo']:
                print(f"[{index}/{total_songs}] 歌曲 '{songname}' 没有可用的URL，跳过")
                error_songs += 1
                continue

            # 获取实际的歌曲下载URL
            midurlinfo = midurlinfo_data['midurlinfo'][0].get('xcdnurl', '').strip()

            # 检查URL是否有效
            if midurlinfo and midurlinfo.strip():
                try:
                    # 下载歌曲文件
                    print(f"[{index}/{total_songs}] 开始下载: {singer} - {songname}")
                    response = requests.get(midurlinfo, timeout=30)
                    response.raise_for_status()  # 检查HTTP请求是否成功

                    # 保存文件到本地
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    # 添加随机延迟，避免请求过于频繁
                    delay = random.uniform(1.0, 3.0)
                    print(f"[{index}/{total_songs}] ✓ {singer}的《{songname}》下载完成！等待 {delay:.2f} 秒后继续...")
                    downloaded_songs += 1
                    time.sleep(delay)

                except requests.exceptions.RequestException as e:
                    print(f"[{index}/{total_songs}] 下载歌曲 '{songname}' 时网络错误: {e}")
                    error_songs += 1
                except IOError as e:
                    print(f"[{index}/{total_songs}] 保存文件 '{songname}' 时出错: {e}")
                    error_songs += 1
                except Exception as e:
                    print(f"[{index}/{total_songs}] 下载歌曲 '{songname}' 时未知错误: {e}")
                    error_songs += 1
            else:
                print(f"[{index}/{total_songs}] 歌曲 '{songname}' 的URL无效，跳过下载")
                error_songs += 1

        # 下载完成统计
        print("\n" + "=" * 50)
        print("下载完成统计:")
        print(f"总歌曲数: {total_songs}")
        print(f"成功下载: {downloaded_songs}")
        print(f"跳过已存在: {skipped_songs}")
        print(f"错误/失败: {error_songs}")
        print(f"下载目录: {self.download_dir}")
        print("=" * 50)


if __name__ == "__main__":
    """
    程序入口点
    示例：下载赵英俊的歌曲，第1页，每页10首
    """
    singer = DownloadMusic('五月天', 2, 10)
    # 开始下载流程
    singer.main()