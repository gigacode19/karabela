
from time import ctime
import speech_recognition as sr
from gtts import gTTS
import vlc

# Konuşma sözlüğü
sozluk = {
    "Selamünaleyküm": "Aleyküm selam",
    "Selam": "Selam",
    "Merhaba": "Merhaba",
    "Karabela": "Efendim",
    "adın ne": "Ben karabela",
    "nerelisin": "Trabzonluyum elhamdülillah",
    "Sen kimsin": "Bana karabela diyebilirsin",
    "kaç yaşındasın": "Yaradılış kodum 2020 de yazıldı",
    "buraya gel": "Geliyorum patron",
    "hava nasıl": "Bilmiyorum",
    "beni dinle": "Dinliyorum",
    "Beni duyuyor musun": "Evet duyuyorum",
    "Bana bak": "Bakıyorum",
    "duydun mu": "Duydum",
    "orada mısın": "Burdayım"
}

def TARİH():
    tarih = ctime()
    gün = tarih[:3]
    ayR = tarih[8:10]
    ay = tarih[4:7]
    yıl = tarih[20:]

    günler = {
        "Mon": "Pazartesi", "Tue": "Salı", "Wed": "Çarşamba",
        "Thu": "Perşembe", "Fri": "Cuma", "Sat": "Cumartesi", "Sun": "Pazar"
    }
    aylar = {
        "Jan": "Ocak", "Feb": "Şubat", "Mar": "Mart", "Apr": "Nisan", "May": "Mayıs",
        "Jun": "Haziran", "Jul": "Temmuz", "Aug": "Ağustos", "Sep": "Eylül",
        "Oct": "Ekim", "Nov": "Kasım", "Dec": "Aralık"
    }

    gün = günler.get(gün, gün)
    ay = aylar.get(ay, ay)

    tarih = f"{ayR} {ay} {yıl} {gün}"
    return tarih

def GÜN():
    tarih = ctime()
    gün = tarih[:3]
    günler = {
        "Mon": "Pazartesi", "Tue": "Salı", "Wed": "Çarşamba",
        "Thu": "Perşembe", "Fri": "Cuma", "Sat": "Cumartesi", "Sun": "Pazar"
    }
    return günler.get(gün, gün)

def AY():
    tarih = ctime()
    ay = tarih[4:7]
    aylar = {
        "Jan": "Ocak", "Feb": "Şubat", "Mar": "Mart", "Apr": "Nisan", "May": "Mayıs",
        "Jun": "Haziran", "Jul": "Temmuz", "Aug": "Ağustos", "Sep": "Eylül",
        "Oct": "Ekim", "Nov": "Kasım", "Dec": "Aralık"
    }
    return aylar.get(ay, ay)

def YIL():
    tarih = ctime()
    yıl = tarih[20:]
    return yıl

def SAAT():
    tarih = ctime()
    saat = tarih[11:16]
    return saat

##-------------------------------------------------------------------
def DİNLE():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        KONUŞ("Dinliyorum..")
        r.adjust_for_ambient_noise(source, duration=0.5)  # Ortam gürültüsüne göre ayarla
        # Gürültü azaltma (örnek olarak Wiener filtresi)
        r.energy_threshold = 4000  # Enerji eşiğini ayarlayın (deneme yanılma ile optimize edilebilir)
        audio = r.listen(source)
    
    try:
        cevap = r.recognize_google(audio, language="tr-TR")
        return cevap
    except sr.UnknownValueError:
        return "Duyamadım"
    except sr.RequestError as e:
        if "recognition connection failed" in str(e):  # Ağ bağlantı hatası kontrolü
            return "İnternet bağlantısı yok."
        else:
            return "Ses hizmetine ulaşılamıyor."

def KONUŞ(cevap):
    tts = gTTS(text=cevap, lang="tr")
    tts.save("cevap.mp3")
    
    # VLC ile ses çalma
    player = vlc.MediaPlayer("cevap.mp3")
    player.play()

    while player.is_playing():
        pass  # Ses çalarken bekle
    
    print(f"Karabela: {cevap}\n")


def SOHPET():
    while True:
        duyulan = DİNLE()
        print(f"Siz: {duyulan}\n")

        if duyulan == "Duyamadım":
            KONUŞ("Duyamadım")
        elif duyulan == "saat kaç":
            KONUŞ(SAAT())
        elif duyulan == "Hangi gündeyiz":
            KONUŞ(GÜN())
        elif duyulan == "Hangi aydayız":
            KONUŞ(AY())
        elif duyulan == "hangi yıldayız":
            KONUŞ(YIL())
        elif duyulan == "ayın kaçı":
            KONUŞ(TARİH())
        elif duyulan == "tarih ne":
            KONUŞ(TARİH())
        elif duyulan == "Sistemi kapat":
            KONUŞ("Sistem kapatılıyor, artık komut alamayacağım.")
            break
        else:
            cevap = sozluk.get(duyulan, "Henüz bu cümleyi bilmiyorum.")
            KONUŞ(cevap)

if __name__ == "__main__":
    SOHPET()
