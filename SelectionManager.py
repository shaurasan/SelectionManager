import maya.cmds as cmds
import functools


class SelectionManager:


    def __init__(self):
        #イニシャライザ
        if cmds.window("myWindow", exists = True):
            cmds.deleteUI("myWindow", window = True)

        self.data = {}
        self.create_ui()



    #ボタンをクリックで登録
    def get_objects(self, *args):
        #long=Trueでフルパス　別グループの名前の重複などの対策
        selected_objects = cmds.ls(sl = True, l = True)
        if not selected_objects:
            cmds.warning("オブジェクトが選択されていません。")
            return

        button_name = ""

        if len(selected_objects) == 1:
            button_name = selected_objects[0].split("|")[-1]

        else:
            #ポップアップの入力
            #cancelButton,dismissStringはキャンセルescやウィンドウを閉じた際の挙動
            result = cmds.promptDialog(
                title="ボタン名の登録",
                message="登録したい名前を入力してください。",
                button=["決定", "キャンセル"],
                defaultButton="決定",
                cancelButton="キャンセル",
                dismissString="キャンセル"
            )
            if result == "決定":
                text = cmds.promptDialog(query = True, text = True)
                if text:
                    button_name = text
                else:
                    cmds.warning("名前を入力してください。")
                    return
            else:
                #キャンセルで何もしない
                return

        #辞書に選択を保存
        self.data[button_name] = selected_objects

        cmds.setParent(self.main_column)
        """
        functools.partialは既存の関数の一部引数を固定
        新しい関数を作成する。
        この場合、run_commandはselect_objectsのbutton_name引数を固定
        """
        run_command = functools.partial(self.select_objects, button_name)
        cmds.button(label = button_name, c = run_command)

    def select_objects(self, button_name, *args):
        #args[0]は押されたボタンのUI名
        print(button_name)  # 押されたボタンのUI名が表示される
        cmds.select(self.data[button_name], r = True)

    def delete_button(self, *args):
        new_buttons = cmds.columnLayout(self.main_column, q = True, childArray = True)

        if new_buttons:
            for button in new_buttons:
                cmds.deleteUI(button)
        
        self.data.clear() 

    
    #ウィンドウを作成
    def create_ui(self):
        #インスタンス変数 self.変数名
        #tlb ツールボックススタイル
        self.window = cmds.window("myWindow", title = "オブジェクトセレクタ", widthHeight = (400, 300), tlb = True)
        
        """

        タブレイアウト例
        tab = cmds.tabLayout(scr = True, innerMarginWidth=5, innerMarginHeight=1)
        cmds.tabLayout(tab, e=True, tabLabel=[(tabColumn, "オブジェクト登録"),(tabColumn2, "オブジェクト選択")])

        """
        form = cmds.formLayout()

        #crは子をスクロール領域と同じ幅にする
        scroll = cmds.scrollLayout(cr = True)
        self.main_column = cmds.columnLayout(adj = True)
        
        cmds.setParent("..")
        cmds.setParent("..")
        
        button_column = cmds.columnLayout(adj = True)
        cmds.button(label = "オブジェクトを登録", c = self.get_objects)
        cmds.button(label = "すべて削除", bgc = (0.5,0,0), c = self.delete_button)

        #ap パーセント、オフセット
        cmds.formLayout(form, e = True, af = [(button_column, "bottom", 0),
                                           (button_column, "left", 0),
                                           (button_column, "right", 0),
                                           (scroll, "top", 0),
                                           (scroll, "left", 0),
                                           (scroll, "right", 0)],
                                           ac = [(scroll, "bottom", 0, button_column)])

        cmds.showWindow(self.window)

        

excute = SelectionManager()

"""
コンセプト：自分がつかうだろうなセット

ボタンをクリックで登録したオブジェクトを選択
獲得したオブジェクト名をボタンラベルにする
動的にボタンを生成する
右クリで削除とか
全削除ボタン
画像をUIに組み込む
選択オブジェクトのマテリアルを取得
複数のオブジェクトも登録
名前を自身で登録する
ポップアップで名前入力
保存するかどうか
名前検索とか
"""
