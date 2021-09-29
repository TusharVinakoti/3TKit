from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty, StringProperty
from kivy.config import Config
from kivymd.uix.list import OneLineAvatarListItem
from kivy.utils import platform
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import qrcode


Config.set("graphics", "resizable", True)

class HomeScreen(Screen):
    pass


class YTScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class IPToolScreen(Screen):
    pass


class IMTSKScreen(Screen):
    pass


class QRCodeScreen(Screen):
    pass

class DevScreen(Screen):
    pass

class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()


class Mainapp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            previous=True,
            ext = [".png", ".jpg"],
        )
    

    def build(self):

        self.theme_cls.primary_palette = "Red"
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(ProfileScreen(name="profile"))
        self.sm.add_widget(IPToolScreen(name="iptool"))
        self.sm.add_widget(IMTSKScreen(name="imtsk"))
        self.sm.add_widget(QRCodeScreen(name="code"))

        Builder.load_file("main.kv")
        return self.sm


    def stat(self):

        self.dialog = MDDialog(title='ToolKit',
                                type="simple",
                                size_hint=(0.8, 1),
                                items=[
                                    Item(text="Home", on_release=lambda x: self.home_switch(x)),
                                    Item(text="IMTSK", on_release=lambda x: self.imtsk_switch(x)),
                                    Item(text="QRCode", on_release=lambda x: self.qrcode_switch(x)),
                                    Item(text="IPTool", on_release=lambda x: self.iptool_switch(x)),
                                    Item(text="About Dev", on_release=lambda x: self.profile_switch(x)),



                                ],
                                buttons=[
                                            MDFlatButton(text="Close", on_release=self.close_dialog)
                                        ],

                                auto_dismiss = True
                                   )
        self.dialog.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def home_switch(self, obj):
        self.sm.current = "home"
        self.dialog.dismiss()

    def imtsk_switch(self, obj):
        self.sm.current = "imtsk"
        self.dialog.dismiss()

    def qrcode_switch(self, obj):
        self.sm.current = "code"
        self.dialog.dismiss()

    def iptool_switch(self, obj):
        self.sm.current = "iptool"
        self.dialog.dismiss()

    def profile_switch(self, obj):
        self.sm.current = "profile"
        self.dialog.dismiss()

    def file_manager_open(self):
        import os
        path1 = os.environ['USERPROFILE']
        self.file_manager.show(path1)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        import os
        path1= os.path.expanduser("~")
        imtsk_screen = self.sm.get_screen("imtsk")

        import random, string
        x = "Sketch"+''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        import cv2
        image = cv2.imread(path) # loads an image from the specified file
        # convert an image from one color space to another
        grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(grey_img) # helps in masking of the image
        # sharp edges in images are smoothed while minimizing too much blurring
        blur = cv2.GaussianBlur(invert, (21, 21), 0)
        invertedblur = cv2.bitwise_not(blur)
        sketch = cv2.divide(grey_img, invertedblur, scale=256.0)
        path2 = os.path.join(path1 + "Pictures")
        status = cv2.imwrite(os.path.join(path1 + "/Documents", x+".png"), sketch) # converted image is saved as mentioned name
        toast("Sketched Imaged Saved To Documents")


    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


    def create_qr(self):
        code_screen = self.sm.get_screen("code")
        import random, string
        x = "QRCode"+''.join(random.choices(string.ascii_letters + string.digits, k=5))
        qr_content = code_screen.ids["qr_content"].text
        if qr_content == "":
            toast("Please Enter Text or Url")
        else:
            qr = qrcode.QRCode(version=1,box_size=10,border=5)
            qr.add_data(qr_content)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            import os
            path1= os.path.expanduser("~")
            img.save(x+".png")
            toast("QRCode Created")

    def find_ip(self):
        ip_screen = self.sm.get_screen("iptool")
        ip_URL = ip_screen.ids["ip_URL"]
        ip_url = ip_screen.ids["ip_url"]
        ip_add = ip_screen.ids["ip_add"]
        if "https://www." and "http://www." and ".com" not in ip_URL.text:
            toast("Please Enter A Valid Url")
        elif "https://" in ip_URL.text:
            toast("Remove https:// from the url")
        elif "www." and ".com" in ip_URL.text:
            import socket
            ip_address = socket.gethostbyname(ip_URL.text)
            ip_url.text = f"Url: {ip_URL.text}"
            ip_add.text = f"IPv4: {ip_address}"
            toast("IPv4 Address Found")







Mainapp().run()
