import JianYingApi as Api
import pyautogui
if __name__ == "__main__":
    JianYing_Instance = Api.Jy_Warp.Instance(Start_Jy=True) #启动一个剪映实例
    JianYing_Instance._Select_Drafts(0) #选择第一个草稿并进入主界面
    JianYing_Instance._Append_Media(path=r"C:\Users\ppzzh\Desktop",name="pf.flv") #导入一个媒体到库中
    JianYing_Instance._Drag_To_Track(0) #把库中第一个媒体拽入轨道上
    JianYing_Instance._VETreeMainCellItem("特效").Click() #选择特效栏
    pyautogui.moveTo(JianYing_Instance._OnlineResourceItem("蓝色丝印")) # 鼠标移动到“蓝色丝印”的特效上
    JianYing_Instance._here_to_track() #拖拽到时间轴轨道上
    Export_Options = Api.Jy_Warp.Export_Options(
        export_vid=True,
        export_name="Pulp_Fiction",
        export_path=r"D:/",
    )