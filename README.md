# JianYing-Api 第三方剪映Api  
![JianYing V3.3.5](https://img.shields.io/badge/JianYing-3.3.5-blue.svg) 通过uiautomation实现  


```python
import JianYingApi as Api
import pyautogui
JianYing_Instance = Api.JianYing_Warp.Instance() #启动一个剪映实例
JianYing_Instance._Select_Drafts(0) #选择第一个草稿并进入主界面
JianYing_Instance._Append_Media(path="D:/movies",name="Pulp_Fiction.mp4") #导入一个媒体到库中
JianYing_Instance._Drag_To_Track(0) #把库中第一个媒体拽入轨道上
JianYing_Instance._To_column("特效","特效效果","收藏") #选择特效栏
pyautogui.moveTo(JianYing_Instance._OnlineResourceItem("蓝色丝印")) # 鼠标移动到“蓝色丝印”的特效上
puautogui._here_to_track() #拖拽到时间轴轨道上
Export_Options = Api.Export_Options(
    export_name:"Pulp_Fiction",
    export_path:r"D:\Creative",
    export_vid:True
)
```
#### 已经实现的功能
- 剪映控件基本库(可以在UI中作为元素的)
- 媒体的导入导出
- 拖拽元素到轨道上
- 字幕,歌词识别
#### 已知问题
- 无法获取轨道中的音频对象
- 在滚动条下方的元素无法被正确获取
#### Todo
- 考研
- 文稿匹配
- 在能力允许的情况下完成轨道操作(裁剪、拖拽、拼合、变速.....)
- 配置文件的读取、解析和修改(`draft_content_json`)
- 关键帧的设定
- 代理设定
- 详细的导出设置