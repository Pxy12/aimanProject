import time
import requests
from originCode import qq_music_api
import random

class download_music:
    def __init__(self,singer,page,num):
        self.data1 = {"comm": {"cv": 4747474, "ct": 24, "format": "json", "inCharset": "utf-8", "outCharset": "utf-8",
                  "notice": 0,
                  "platform": "yqq.json", "needNewCode": 1, "uin": 3223607546,
                  "g_tk_new_20200303": 1188746000,
                  "g_tk": 1188746000},
         "req_1": {"method": "DoSearchForQQMusicDesktop", "module": "music.search.SearchCgiService",
                   "param": {"remoteplace": "txt.yqq.top", "searchid": "61292176913318089",
                             "search_type": 0,
                             "query": singer, "page_num":page , "num_per_page": num}}}

    def main(self):
        qq_music = qq_music_api()
        search_result = qq_music.search_music(self.data1)
        dataArr = search_result['req_1']['data']['body']['song']['list']
        songData = qq_music_api()
        for index in dataArr:
            songID = index['id']
            biz_id = str(songID)
            songMID = index['mid']
            guid = str(7785978040 + random.randint(1, 10))
            albumMid = index["album"]["mid"]
            songmid = [songMID]
            songname = index["name"]
            singer = index["singer"][0]["name"]
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
                "req_1": {
                    "module": "music.musichallSong.PlayLyricInfo",
                    "method": "GetPlayLyricInfo",
                    "param": {
                        "songMID": songMID,
                        "songID": songID
                    }
                },
                "req_2": {
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
                "req_3": {
                    "module": "music.musichallAlbum.AlbumInfoServer",
                    "method": "GetAlbumDetail",
                    "param": {
                        "albumMid": albumMid
                    }
                },
                "req_4": {
                    "module": "music.vkey.GetEVkey",
                    "method": "GetUrl",
                    "param": {
                        "guid": guid,
                        "songmid": songmid,
                        "songtype": [
                            0
                        ],
                        "uin": "3223607546",
                        "loginflag": 1,
                        "platform": "20",
                        "xcdn": 1,
                        "qdesc": "lq96kOgg"
                    }
                }
            }
            # print(json.dumps(data))
            # print(songID,songMID,biz_id,guid,albumMid,songmid)
            urlData = songData.search_music(data)
            midurlinfo = urlData['req_4']['data']['midurlinfo'][0]['xcdnurl'].strip()
            if midurlinfo is not None and midurlinfo.strip():
                with open(rf"C:\Users\32236\Desktop\music\{songname}.mp3", 'wb') as f:
                    f.write(requests.get(midurlinfo).content)
                    time.sleep(random.uniform(1.0, 3.0))
                    print(f"{singer}的歌:{songname}||下载好啦，打开听听吧>>>{midurlinfo}")

if __name__=="__main__":
    singer=download_music('五月天',1,30)
    singer.main()