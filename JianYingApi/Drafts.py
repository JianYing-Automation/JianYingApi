import json , os  , shutil , uuid 

class _Drafts:
    def __init__(self,path:os.PathLike,Drafts_Name:str) -> None:
        # Drafts_Name : draft_content.json | draft_meta_info.json
        if os.path.isdir(path) == False : path = os.path.split(path)[0] # Make Sure It's a Dir Path
        self.path = path
        self.Drafts_Name = Drafts_Name
        self.Struct = {}
        self._load()
    
    def _load(self) -> None:
        self.Struct = json.loads(open(os.path.join(self.path,self.Drafts_Name),"r",encoding="utf-8").read())

    def _save(self) -> None:
        open(os.path.join(self.path,self.Drafts_Name),"w",encoding="utf-8").write(json.dumps(self.Struct))


class Meta(_Drafts):
    # Draft_Meta_Info
    def __init__(self, path: os.PathLike) -> None:
        super().__init__(path, "draft_meta_info.json")
    
    def Import2Lib(self,path:os.PathLike,metetype:str):
        """
            导入媒体到媒体库中 ,这不会加入到轨道中去
            metertype: video , photo , music
        """
        name = os.path.split(path)[-1]
        self.Struct["draft_materials"][0]["value"].append({
            "extra_info":name,
            "file_Path":path,
            "metetype":metetype,
            "id":str(uuid.uuid1())})

class Content(_Drafts):
    # Draft_Content
    def __init__(self, path: os.PathLike) -> None:
        super().__init__(path, "draft_content.json")

    def AddMaterial(self,Mtype:str,Content:dict): self.Struct["materials"][Mtype].append(Content)

    def NewTrack(self,TrackType:str)->dict:
        """ 
            Create a new track
            TrackType: text video audio effect
            return Track
        """
        _t = {"id":str(uuid.uuid1()),"type":TrackType,"segments":[]}
        self.Struct["tracks"].append(_t)
        return _t

    def GetTracksById(self,Track_id:str)->dict: return [i for i in self.Struct["tracks"] if i["id"] == Track_id][0]
    
    def DelTrack(self,Track_id:str): self.Struct["tracks"] = [i for i in self.Struct["tracks"] if i["id"] != Track_id]

    def UpdateTrack(self,Track_id:str,New_Track:dict):
        self.DelTrack(Track_id=Track_id) 
        self.Struct["tracks"].append(New_Track)

    def Add2Track(self,Track_id:str,Content:dict):
        """
            Import A #$%#$% into Track
            Track_id : Track_id
            Content: Whatever U Want
        """
        _t = self.GetTracksById(Track_id=Track_id)
        _t["segments"].append(Content)
        self.UpdateTrack(Track_id=Track_id,New_Track=_t)
    
    def _recaculate_max_duration(self):
        _k = []
        for i in self.Struct["tracks"]:
            for _v in i["segments"]:
                if "target_timerange" in _v : _k.append(_v["target_timerange"]["start"]+_v["target_timerange"]["duration"])
        self.Struct["duration"] = max(_k)

class Projects():
    def __init__(self,Path:os.PathLike) -> None:
        self.Meta = Meta(path=Path)
        self.Content = Content(path=Path)
    def Save(self):
        self.Content._recaculate_max_duration() , self.Meta._save() , self.Content._save()

def Create_New_Drafts(path:os.PathLike)->Projects:
    # 创建新草稿
    if os.path.exists(path=path) == False: os.mkdir(path=path)
    shutil.copy("./blanks/draft_content.json",path)
    shutil.copy("./blanks/draft_meta_info.json",path)
    return Projects(Path=path)