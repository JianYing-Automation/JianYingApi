import sys
sys.path.append("..")
from . import Jy_Warp
import uiautomation

def Recognize_Subtitle(filename:str,filepath:str,export_options:Jy_Warp.Export_Options,_jy_instance:uiautomation.Control=None):
    """
        Recognize Subtitle
        Langugage Support Chinese and English.
        It Will Open an instance of jianying if not given.
        filepath,filename,exportoptions is needed.
    """
    if _jy_instance == None: _jy = Jy_Warp.Instance()
    else: _jy = _jy_instance
    while _jy._detect_viewport() != 1: Jy_Warp.lag()
    _jy._Append_Media(path=filepath,name=filename)
    _jy._Drag_To_Track(0)
    wenben = _jy._MainTabView("文本")
    wenben.Click()
    _jy._VETreeMainCellItem("新建文本").Click() # 防止其他例如“花字”子目录过长导致的元素无法识别
    _jy._VETreeMainCellItem("智能字幕").Click()
    uiautomation.Click(x=wenben.BoundingRectangle.xcenter(),y=_jy._VETreeMainCellItem("识别歌词").BoundingRectangle.ycenter())
    while _jy._detect_viewport() == 2 : Jy_Warp.lag()
    _jy._Export(export_options)
