"""
    Jian Ying Api
    Tests On Jianying V3.3.5 Windows Version
    Author: @PPPPP        
    FOR  DEBUG  ONLY
"""
import os
import uiautomation as api32
import time
import pyautogui as auto
import pyperclip
from . import Logic_warp as lw
from . import Ui_warp as uw


lag_t = 0.5
def lag(lag:float=lag_t): time.sleep(lag)

class Export_Options:
    def assert_in(self,k,supportList:list):
        if k in supportList : return k
        else: IndexError("Keyword Dismatch")
    
    def check(self):
        assert self.export_vid == True or self.export_sub == True , "Please Select At Least On Output Way [vid | srt]"
    def __init__(self,
        export_sub:bool=False,export_vid:bool=False,export_name:str="",export_path:str="",vid_quality:int=480,bit_rate:str="recommend",
        bit_rate_option_kbps:int=16000,bit_rate_option_cbr:bool=False,bit_rate_option_vbr:bool=True,Encode:str="H.264",Format:str="mp4",
        Frame:int=30,export_srt_type:str="srt"
        ) -> None:
        """
        Export Options
            export_vid : Is Export Video [True | False]
                    export_name: Name To Export 
                    export_path: Path To Export
                    vid_quality: Export Video Quality [ 480 | 720 | 1080 | 1440 | 2160 ]
                    bit_rate   : Export Bit Rate   [ "recommend" | "lower" | "higher" | "option" ]
                    bit_rate_option_kbps: Only Enable on "option" bitrate 
                    bit_rate_option_cbr: Constant Bit Rate [True | False]
                    bit_rate_option_vbr: Variable Bit Rate [True | False] Default
                    Encode     : Encode Of The Video ["H.264"|"HEVC"]
                    Format     : Format Of The Video ["mp4"|"mov"]
                    Frame      : [24 | 25 | 30 | 50 | 60]
            export_sub : Is Export SubTitle [True | False]
                    export_srt_type : ["srt"|"txt"]
        """
        self.export_sub = export_sub
        self.export_vid = export_vid
        self.export_name = export_name
        self.export_path = export_path
        self.vid_quality = self.assert_in(vid_quality,[480,720,1080,1440,2160])
        self.bit_rate = self.assert_in(bit_rate,["recommend","lower","higher","option"])
        self.bit_rate_option_kbps = bit_rate_option_kbps
        self.bit_rate_option_cbr = bit_rate_option_cbr
        self.bit_rate_option_vbr = bit_rate_option_vbr
        self.Encode = self.assert_in(Encode,["H.264","HEVC"])
        self.Format = self.assert_in(Format,["mp4","mov"])
        self.Frame = Frame
        self.export_srt_type = self.assert_in(export_srt_type,["txt","srt"])
        self.check()


class Instance:
    """
        Create a JianYing UI Instance
    """
    def __Start_JianYing(self):
        # Start A JianYing Instance
        self.JianYing_Mian_Thread = lw._creat_exe(os.path.join(self.JianYing_Path,"Apps","JianyingPro.exe"))
        self.JianYing_Mian_Thread.start()
        self.Window = api32.WindowControl(searchDepth=1,Name="JianyingPro")

    def _detect_viewport(self,timeout_seconds:int=0.2):
        """
            Current Viewport
            -1 : JianYing Not Launched
            0 : Start Page
            1 : Main Page
            2 : Loading Page
            3 : Media Select Page
            4 : Export Page
            5 : Loading Assets
        """
        jy_main = api32.WindowControl(Name="JianyingPro",searchDepth=1)
        try:
            if jy_main.Exists(maxSearchSeconds=timeout_seconds)==False: return -1
        except : return -1
        if jy_main.TextControl(Name="HomePageStartProjectName",searchDepth=1).Exists(maxSearchSeconds=timeout_seconds): return 0
        elif jy_main.WindowControl(searchDepth=2,ClassName="#32770").Exists(maxSearchSeconds=timeout_seconds) : return 3
        elif jy_main.WindowControl(searchDepth=1,Name="导出").Exists(maxSearchSeconds=timeout_seconds) : return 4
        elif jy_main.WindowControl(searchDepth=1,Name="导入素材").Exists(maxSearchSeconds=timeout_seconds):return 5
        elif uw._search_include(windowObj=jy_main,ClassName="LVLoadingDialog",controlType=api32.WindowControl): return 2
        elif jy_main.GroupControl(Name="MainWindowTitleBarExportBtn",searchDepth=1).Exists(maxSearchSeconds=timeout_seconds):
            self._refresh_control()
            return 1
        else: return -1

    def _refresh_control(self):
        self.Window = api32.WindowControl(searchDepth=1,Name="JianyingPro")
        self.Half = uw._search_include(windowObj=self.Window,controlType=api32.PaneControl,ClassName="SplitView")
        self.Tracks = self.Half.GroupControl(searchDepth=1,Name="MainTimeLineRoot")

    def __init__(self,JianYing_Exe_Path:str=None,Start_Jy:bool=True) -> None:
        self.JianYing_Path = JianYing_Exe_Path if JianYing_Exe_Path is not None else lw._Get_JianYing_Default_Path()
        if Start_Jy: 
            if "JianyingPro" in os.popen("tasklist").read():lw._kill_jianYing()
            self.__Start_JianYing()
            
        print(f"Start JianYing , Currently in Page {self._detect_viewport()}")

    def _Start_New_Draft_Content(self):
        # Return Where New Draft Content Button is
        assert self._detect_viewport() == 0 , "Not In Certificated Page(0)"
        self.Window.TextControl(Name="HomePageStartProjectName",searchDepth=1).Click()
        while self._detect_viewport() != 1:lag()

    def _Select_Drafts(self,draft_num:int=0):
        """
            Select A Draft
        """
        def _Get_Drafts()->list:
            assert self._detect_viewport() == 0 , "Not In Certificated Page(0)"
            _drafts = []
            for i in self.Window.GetChildren():
                if i.Name == "HomePageDraft" : _drafts.append(i)
            return _drafts
        while self._detect_viewport() != 0 : lag()
        _drafts = _Get_Drafts()
        assert len(_drafts) < draft_num + 2 ,IndexError("Out Of Bounds")
        _drafts[draft_num].Click()
        while self._detect_viewport() != 1 : lag()
        
    def _Append_Media(self,path:str,name:str)->tuple:
        """
            Append Media
        """
        if self._detect_viewport() == 1:
            self._To_column("媒体","本地","导入")
            if len(self._Get_Added_Medias()) == 0: # No Media Added, Click Big Button 
                _l = self.Half.ScrollBarControl(searchDepth=1).BoundingRectangle
                _r = self._current_progress().BoundingRectangle
                api32.Click(x=int(_l.left+(_r.left-_l.left)/2),y=_l.ycenter())
            else: # Click The Small Import Button
                api32.Click(x=self._MainTabView("文本").BoundingRectangle.xcenter(),y=self._VETreeMainCellItem("本地").BoundingRectangle.ycenter())
        while self._detect_viewport() != 3 : lag() # Wait Until Meida Dialog Shows Up
        uw.Explorer_Files(self.Window.WindowControl(searchDepth=1,ClassName="#32770"))._type_in(path=path,name=name)

    def _Get_Added_Medias(self)->list:
        """
            Return Added Medias
        """
        Return_List = []
        for i in self.Half.GetChildren():
            if i.Name == "automationroot": Return_List.append(i)
        return Return_List
    
    def _Drag_To_Track(self,mediaNum:int=0):
        """
            Drag Certificated Media Into Tracks
        """
        medias = self._Get_Added_Medias()
        assert self._detect_viewport() == 1 , "Not In Certificated Page(1)"
        assert mediaNum < len(medias)+1 , "mediaNum should not higher than meidas len"
        api32.DragDrop(x1=medias[mediaNum].BoundingRectangle.xcenter(),y1=medias[mediaNum].BoundingRectangle.ycenter(),x2=self.Tracks.BoundingRectangle.xcenter(),y2=self.Tracks.BoundingRectangle.ycenter(),waitTime=1)
        
    def _MainTabView(self,name:str)->api32.GroupControl:
        """
            Return A Object of _MainTabView , Exisit Detect Needed
        """
        _t = self.Half.GroupControl(searchDepth=1,Name=f"MainTabView:{name}")
        assert _t.Exists(maxSearchSeconds=lag_t) , "MainTab Doesn't Exsist"
        return _t

    def _VETreeMainCellItem(self,name:str)->api32.TextControl:
        return self.Half.TextControl(searchDepth=1,Name=f"VETreeMainCellItem:{name}")

    def _VETreeSubCellItem(self,name:str)->api32.TextControl:
        return self.Half.TextControl(searchDepth=1,Name=f"VETreeSubCellItem:{name}")

    def _OnlineResourceItem(self,name:str)->api32.GroupControl:
        return self.Half.GroupControl(searchDepth=1,Name=f"OnlineResourceInfoView:{name}")

    def _To_column(self,Main_tab:str,Vetree:str,Vecell:str)->None:
        """
            Click , Then Return A Object of One Column
            E.g : _To_column("媒体","本地","导入")
        """
        assert self._detect_viewport() == 1 , "Not In Certificated Page(1)"
        _s , _k , _t = self._MainTabView(Main_tab) , self._VETreeMainCellItem(Vetree) , self._VETreeSubCellItem(Vecell)
        _s.Click()
        while _k.Exists(maxSearchSeconds=lag_t) == False : lag()
        if _t.Exists(maxSearchSeconds=lag_t) == False : _k.Click()
        _t.Click()
        return None

    def _here_to_track(self):
        auto.dragTo(x=self.Tracks.BoundingRectangle.xcenter(),y=self.Tracks.BoundingRectangle.ycenter())

    def _Export(self,config:Export_Options):
        """
            Export Operations
        """
        if self._detect_viewport() == 1: self.Window.GroupControl(searchDepth=1,Name="MainWindowTitleBarExportBtn").Click()


        assert self._detect_viewport() == 4 , "Not In Certificated Page(4)"
        _exp_ins = self.Window.WindowControl(Name="导出",searchDepth=1)
        _posi = _exp_ins.GroupControl(Name="ExportFileNameInput",searchDepth=1).BoundingRectangle
        ### Type in Export Name
        auto.tripleClick(x=_posi.xcenter(),y=_posi.ycenter())
        if config.export_name != "":
            api32.SendKeys(config.export_name)
        else:
            config.export_name = pyperclip.copy()
        ### Select Export Path
        if config.export_path != "":
            _exp_ins.ButtonControl(searchDepth=1,Name="ExportFileNameInputBtn").Click()
            while self._detect_viewport() != 3: lag() # Wait For It Turns Out
            _file_ins = uw.Explorer_Files(File_Bar=_exp_ins.WindowControl(ClassName="#32770"))
            _file_ins._type_in(path=config.export_path)
            while self._detect_viewport() != 4:lag()
        else:
            # Default Save Path is CurrentUser+Video
            config.export_path = "C:/Users/{}/Videos".format(os.popen("whoami").read().replace("\n","").split("\\")[1])
        # Video Export
        _vid_ins = _exp_ins.GroupControl(searchDepth=1,Name="automationvideoPanelSettingsGroup")
        _vid_ratio_status = uw._radio_detect(_vid_ins.BoundingRectangle.left+8,_vid_ins.BoundingRectangle.top+8)
        if config.export_vid:
            if _vid_ratio_status == 0 : api32.Click(_vid_ins.BoundingRectangle.left+8,_vid_ins.BoundingRectangle.top+8)
        else:
            if _vid_ratio_status == 1: api32.Click(_vid_ins.BoundingRectangle.left+8,_vid_ins.BoundingRectangle.top+8) # Turn off Video Export
        _sub_ins = _exp_ins.GroupControl(searchDepth=1,Name="automationsubtitlePanelSettingsGroup")
        if config.export_sub:
            _sub_ratio_status = uw._radio_detect(_sub_ins.BoundingRectangle.left+8,_sub_ins.BoundingRectangle.top+8)
            if _sub_ratio_status == 0: api32.Click(_sub_ins.BoundingRectangle.left+8,_sub_ins.BoundingRectangle.top+8) # Turn On Ratio
            if _sub_ratio_status == -1: IndexError("May Be You Havn't Parse Subtitle Yet.")
        else:
            if _sub_ratio_status == 1: api32.Click(_sub_ins.BoundingRectangle.left+8,_sub_ins.BoundingRectangle.top+8) # Turn off subtitle export
        _exp_ins.GroupControl(searchDepth=1,Name="ExportOkBtn").Click() # Confirm Export
        # Progress : _exp_ins TextControl ,Name = ExportProgress:60.4%
        _exp_success = _exp_ins.GroupControl(Name="ExportSucceedCloseBtn",searchDepth=1)
        while _exp_success.Exists(maxSearchSeconds=0.2) == False : lag() # May Lag Because _Export_ins changed...
        _exp_success.Click()
        return {
            "export_path":config.export_path+config.export_name,
            "export_name":config.export_name
        }