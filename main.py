import os
import json
import datetime

FILE_PATH = "rekening.json"

# Data default jika file belum ada
default_data = {
    "1111": {"pin": "1234", "saldo": 1500000},
    "2222": {"pin": "2345", "saldo": 2500000},
    "3333": {"pin": "3456", "saldo": 500000}
}

# Buat file jika belum ada
def ensure_file_exists():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as file:
            json.dump(default_data, file, indent=4)
        print("File rekening.json berhasil dibuat.\n")

# Load data rekening
def load_rekening():
    with open(FILE_PATH, "r") as file:
        return json.load(file)

# Simpan ke file
def save_rekening(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

# Clear screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Login
def login(rekening_db):
    print("===== LOGIN ATM =====")
    for _ in range(3):
        norek = input("Masukkan nomor rekening: ")
        pin = input("Masukkan PIN: ")
        if norek in rekening_db and rekening_db[norek]["pin"] == pin:
            print("Login berhasil!\n")
            return norek
        else:
            print("Nomor rekening atau PIN salah.\n")
    print("Terlalu banyak percobaan. Program keluar.")
    exit()

# Cetak struk
def cetak_struk(norek, jenis, jumlah, saldo):
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n========== STRUK TRANSAKSI ==========")
    print(f"Tanggal/Waktu  : {waktu}")
    print(f"No. Rekening   : {norek}")
    print(f"Jenis Transaksi: {jenis}")
    print(f"Jumlah         : Rp{jumlah:,}")
    print(f"Saldo Sekarang : Rp{saldo:,}")
    print("=====================================\n")

def menu_atm(norek, rekening_db):
    while True:
        clear_screen()
        print(f"=== ATM - Rekening {norek} ===")
        print("1. Cek Saldo")
        print("2. Setor Uang")
        print("3. Tarik Uang")
        print("4. Logout")
        print("==============================")

        pilihan = input("Masukkan pilihan (1-4): ")
        print("\n------------------------------")

        if pilihan == "1":
            saldo = rekening_db[norek]["saldo"]
            print(f"Saldo Anda: Rp{saldo:,}")

        elif pilihan == "2":
            try:
                jumlah = int(input("Masukkan jumlah setor: Rp"))
                if jumlah > 0:
                    rekening_db[norek]["saldo"] += jumlah
                    save_rekening(rekening_db)
                    print(f"Setor tunai sebesar Rp{jumlah:,} berhasil.")
                    cetak_struk(norek, "Setor Tunai", jumlah, rekening_db[norek]["saldo"])
                else:
                    print("Jumlah harus lebih dari 0.")
            except ValueError:
                print("Input harus berupa angka.")

        elif pilihan == "3":
            try:
                jumlah = int(input("Masukkan jumlah tarik: Rp"))
                if 0 < jumlah <= rekening_db[norek]["saldo"]:
                    rekening_db[norek]["saldo"] -= jumlah
                    save_rekening(rekening_db)
                    print(f"Tarik tunai sebesar Rp{jumlah:,} berhasil.")
                    cetak_struk(norek, "Tarik Tunai", jumlah, rekening_db[norek]["saldo"])
                elif jumlah > rekening_db[norek]["saldo"]:
                    print("Saldo tidak mencukupi.")
                else:
                    print("Jumlah harus lebih dari 0.")
            except ValueError:
                print("Input harus berupa angka.")

        elif pilihan == "4":
            print("Logout berhasil. Program berakhir.")
            return True  # tanda program harus berhenti

        else:
            print("Pilihan tidak valid.")

        input("\nTekan ENTER untuk kembali ke menu...")

def main():
    ensure_file_exists()
    while True:
        clear_screen()
        rekening_db = load_rekening()
        norek = login(rekening_db)
        should_exit = menu_atm(norek, rekening_db)
        if should_exit:
            break  # keluar dari loop utama dan program selesai

if __name__ == "__main__":
    main()
