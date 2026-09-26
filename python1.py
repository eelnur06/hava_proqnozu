from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import requests

seherler = [
    "Bakı",
    "Gəncə",
    "Sumqayıt",
    "Şəki",
    "Quba",
    "Lənkəran",
    "Mingəçevir",
    "London",
    "Paris",
    "İstanbul",
    "Berlin",
    "Moskva",
    "Roma",
    "Dubay",
    "New York",
]


def seher_melumatini_al(seher):
  url = "https://geocoding-api.open-meteo.com/v1/search"
  params = {"name": seher, "count": 1, "language": "az", "format": "json"}
  response = requests.get(url, params=params, timeout=10)
  response.raise_for_status()
  data = response.json()
  if "results" not in data:
    return None
  return data["results"][0]


def havaya_bax():
  seher = seher_secimi.get()
  if not seher:
    messagebox.showwarning("Xəbərdarlıq", "Zəhmət olmasa şəhər seçin.")
    return
  try:
    location = seher_melumatini_al(seher)
    if not location:
      messagebox.showerror("Xəta", "Şəhər tapılmadı.")
      return
    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]
    country = location.get("country", "")
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "wind_speed_10m"
        ),
        "timezone": "auto",
    }
    response = requests.get(weather_url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    current = data["current"]
    temperatur = current["temperature_2m"]
    rütubet = current["relative_humidity_2m"]
    hiss_olunan = current["apparent_temperature"]
    külək = current["wind_speed_10m"]
    seher_label.config(text=f"{city_name}, {country}")
    temperatur_label.config(text=f"{temperatur} °C")
    rütubet_label.config(text=f"💧 Rütubət: {rütubet}%")
    hiss_label.config(text=f"🌡️ Hiss olunan: {hiss_olunan} °C")
    külək_label.config(text=f"💨 Külək: {külək} km/saat")
    vaxt_label.config(
        text=(
            "Son yenilənmə: " + datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        )
    )
    mənbə_label.config(text="Məlumat mənbəyi: Open-Meteo API")
  except requests.exceptions.RequestException:
    messagebox.showerror(
        "API xətası", "Hava məlumatını API-dən almaq mümkün olmadı."
    )
  except Exception as error:
    messagebox.showerror("Xəta", str(error))


root = tk.Tk()
root.title("Hava Məlumatı")
root.geometry("500x600")
root.resizable(False, False)
root.configure(bg="#EAF4FF")
başlıq = tk.Label(
    root,
    text="🌤️ HAVA MƏLUMATI",
    font=("Arial", 26, "bold"),
    fg="#1565C0",
    bg="#EAF4FF",
)
başlıq.pack(pady=(30, 20))
şəhər_yazı = tk.Label(
    root, text="Şəhər seç:", font=("Arial", 13, "bold"), bg="#EAF4FF"
)
şəhər_yazı.pack(pady=5)
seher_secimi = ttk.Combobox(
    root, values=seherler, state="readonly", font=("Arial", 14), width=22
)
seher_secimi.pack(pady=10)
seher_secimi.current(0)
havaya_bax_button = tk.Button(
    root,
    text="Havaya bax",
    command=havaya_bax,
    font=("Arial", 14, "bold"),
    bg="#1976D2",
    fg="white",
    activebackground="#0D47A1",
    activeforeground="white",
    padx=30,
    pady=10,
    cursor="hand2",
    relief="flat",
)
havaya_bax_button.pack(pady=20)
seher_label = tk.Label(
    root, text="Şəhər", font=("Arial", 20, "bold"), bg="#EAF4FF", fg="#263238"
)
seher_label.pack(pady=10)
temperatur_label = tk.Label(
    root, text="-- °C", font=("Arial", 45, "bold"), bg="#EAF4FF", fg="#1565C0"
)
temperatur_label.pack(pady=10)
rütubet_label = tk.Label(
    root, text="💧 Rütubət: --", font=("Arial", 13), bg="#EAF4FF"
)
rütubet_label.pack(pady=5)
hiss_label = tk.Label(
    root, text="🌡️ Hiss olunan: --", font=("Arial", 13), bg="#EAF4FF"
)
hiss_label.pack(pady=5)
külək_label = tk.Label(
    root, text="💨 Külək: --", font=("Arial", 13), bg="#EAF4FF"
)
külək_label.pack(pady=5)
vaxt_label = tk.Label(
    root, text="Son yenilənmə: --", font=("Arial", 9), fg="#607D8B", bg="#EAF4FF"
)
vaxt_label.pack(pady=(20, 5))
mənbə_label = tk.Label(
    root,
    text="Məlumat mənbəyi: --",
    font=("Arial", 10, "italic"),
    fg="#607D8B",
    bg="#EAF4FF",
)
mənbə_label.pack(pady=5)
root.mainloop()