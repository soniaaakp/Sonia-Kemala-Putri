import csv
from datetime import datetime
from collections import deque

riwayat_transaksi = deque(maxlen=5)

def format_rupiah(angka):
    return f"Rp{int(angka):,}".replace(",", ".")

def generate_id(prefix):
    return f"{prefix.upper()}{int(datetime.now().timestamp())}"

# ------------------ PRODUK ------------------
def load_produk():
    produk = {}
    try:
        with open('produk.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                produk[row['id']] = row
    except FileNotFoundError:
        pass
    return produk

def simpan_produk(produk):
    with open('produk.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'nama', 'stok', 'harga', 'deskripsi']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in produk.values():
            writer.writerow(item)

def tambah_produk():
    produk = load_produk()
    id_produk = input("ID Produk (kosongkan untuk otomatis): ")
    if not id_produk:
        id_produk = generate_id("J")  # Ganti prefix dengan "J" untuk jaket
    if id_produk in produk:
        print("❌ ID produk sudah ada.")
        return
    nama = input("🧥 Nama Jaket: ")  # Mengganti Sepatu dengan Jaket
    stok = input("📦 Stok: ")
    harga = input("💸 Harga: ")
    deskripsi = input("📝 Deskripsi Jaket (misalnya bahan, fitur, ukuran): ")
    produk[id_produk] = {
        'id': id_produk, 'nama': nama, 'stok': stok,
        'harga': harga, 'deskripsi': deskripsi
    }
    simpan_produk(produk)
    print("✅ Jaket berhasil ditambahkan.")

def lihat_produk():
    produk = load_produk()
    print("\n📋 Daftar Jaket:")  # Mengganti 'Produk' dengan 'Jaket'
    print("-" * 50)
    for p in produk.values():
        print(f"🔹 {p['id']} | {p['nama']} | Stok: {p['stok']} | {format_rupiah(p['harga'])} | Deskripsi: {p['deskripsi']}")
    print("-" * 50)

def ubah_produk():
    produk = load_produk()
    id_produk = input("ID Produk yang ingin diubah: ")
    if id_produk in produk:
        print("Masukkan data baru (kosongkan jika tidak ingin mengubah):")
        nama = input("Nama baru: ") or produk[id_produk]['nama']
        stok = input("Stok baru: ") or produk[id_produk]['stok']
        harga = input("Harga baru: ") or produk[id_produk]['harga']
        deskripsi = input("Deskripsi baru: ") or produk[id_produk]['deskripsi']
        produk[id_produk] = {
            'id': id_produk, 'nama': nama, 'stok': stok,
            'harga': harga, 'deskripsi': deskripsi
        }
        simpan_produk(produk)
        print("✅ Jaket berhasil diubah.")
    else:
        print("❌ Produk tidak ditemukan.")

def hapus_produk():
    produk = load_produk()
    id_produk = input("ID Produk yang ingin dihapus: ")
    if id_produk in produk:
        del produk[id_produk]
        simpan_produk(produk)
        print("🗑 Jaket berhasil dihapus.")
    else:
        print("❌ Produk tidak ditemukan.")

# ------------------ TRANSAKSI ------------------
def simpan_transaksi(data):
    fieldnames = ['id_transaksi', 'tanggal', 'tipe', 'id_produk', 'jumlah', 'total']
    with open('transaksi.csv', 'a+', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        file.seek(0, 2)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

def cetak_struk(data, produk):
    print("\n🧾===== STRUK TRANSAKSI =====")
    print(f"ID Transaksi : {data['id_transaksi']}")
    print(f"Tanggal      : {data['tanggal']}")
    print(f"Jenis        : {'Penjualan' if data['tipe'] == 'jual' else 'Pembelian'}")
    print(f"Produk       : {produk['nama']}")
    print(f"Jumlah       : {data['jumlah']}")
    print(f"Harga Satuan : {format_rupiah(produk['harga'])}")
    print(f"Total        : {format_rupiah(data['total'])}")
    print("Terima kasih telah bertransaksi 💐")
    print("============================\n")

def transaksi(tipe):
    produk = load_produk()
    id_produk = input("ID Produk Jaket: ")  # Mengganti 'ID Produk' dengan 'ID Produk Jaket'
    if id_produk not in produk:
        print("❌ Jaket tidak ditemukan.")
        return
    jumlah = int(input("Jumlah: "))
    stok_sekarang = int(produk[id_produk]['stok'])

    if tipe == 'jual' and jumlah > stok_sekarang:
        print("⚠ Stok tidak mencukupi.")
        return

    harga = int(produk[id_produk]['harga'])
    total = jumlah * harga

    produk[id_produk]['stok'] = str(stok_sekarang - jumlah if tipe == 'jual' else stok_sekarang + jumlah)
    simpan_produk(produk)

    transaksi_data = {
        'id_transaksi': generate_id("T"),
        'tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tipe': tipe,
        'id_produk': id_produk,
        'jumlah': jumlah,
        'total': total
    }
    simpan_transaksi(transaksi_data)
    riwayat_transaksi.append(transaksi_data)
    print(f"✅ Transaksi {tipe} berhasil! Total: {format_rupiah(total)}")
    cetak_struk(transaksi_data, produk[id_produk])

def lihat_riwayat():
    print("\n🧾 Riwayat Transaksi Terbaru:")
    print("-" * 60)
    for t in riwayat_transaksi:
        print(f"{t['id_transaksi']} | {t['tanggal']} | {t['tipe']} | {t['id_produk']} | {t['jumlah']} | {format_rupiah(t['total'])}")
    print("-" * 60)

# ------------------ LAPORAN ------------------
def laporan(periode):
    try:
        with open('transaksi.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
    except FileNotFoundError:
        print("❌ Belum ada transaksi.")
        return

    if not rows:
        print("❌ Belum ada transaksi.")
        return

    now = datetime.now()
    total = 0
    print(f"\n📊 Laporan {periode.title()} — {now:%d %B %Y}")
    print("-" * 75)

    for row in rows:
        try:
            tgl = datetime.strptime(row['tanggal'], '%Y-%m-%d %H:%M:%S')
        except (KeyError, ValueError):
            continue

        if periode == 'harian' and tgl.date() == now.date():
            include = True
        elif periode == 'mingguan' and (now - tgl).days < 7:
            include = True
        elif periode == 'bulanan' and tgl.month == now.month and tgl.year == now.year:
            include = True
        else:
            include = False

        if include:
            print(f"{tgl:%Y-%m-%d %H:%M:%S} | {row['tipe']:<6} | {row['id_produk']:<10} | {row['jumlah']:<3} | {format_rupiah(row['total'])}")
            total += int(row['total'])

    print("-" * 75)
    print(f"💰 Total {periode.title():<8}: {format_rupiah(total)}\n")

# ------------------ MENU ------------------
def menu_produk():
    while True:
        print("\n🔧 Menu Manajemen Jaket Gorpcore Local")  # Mengganti sepatu dengan jaket
        print("[1] Tambah Jaket")
        print("[2] Lihat Jaket")
        print("[3] Ubah Jaket")
        print("[4] Hapus Jaket")
        print("[5] Kembali")
        pilih = input("Pilihan Anda: ")
        if pilih == '1': tambah_produk()
        elif pilih == '2': lihat_produk()
        elif pilih == '3': ubah_produk()
        elif pilih == '4': hapus_produk()
        elif pilih == '5': break
        else: print("❌ Pilihan tidak valid.")

def menu_transaksi():
    while True:
        print("\n💳 Menu Transaksi")
        print("[1] Penjualan")
        print("[2] Pembelian")
        print("[3] Lihat Riwayat")
        print("[4] Kembali")
        pilih = input("Pilihan Anda: ")
        if pilih == '1': transaksi('jual')
        elif pilih == '2': transaksi('beli')
        elif pilih == '3': lihat_riwayat()
        elif pilih == '4': break
        else: print("❌ Pilihan tidak valid.")

def menu_laporan():
    while True:
        print("\n📈 Menu Laporan")
        print("[1] Laporan Harian")
        print("[2] Laporan Mingguan")
        print("[3] Laporan Bulanan")
        print("[4] Kembali")
        pilih = input("Pilihan Anda: ")
        if pilih == '1': laporan('harian')
        elif pilih == '2': laporan('mingguan')
        elif pilih == '3': laporan('bulanan')
        elif pilih == '4': break
        else: print("❌ Pilihan tidak valid.")

def main():
    print("🧥 Selamat datang di Aplikasi Manajemen Toko Jaket Gorpcore Local 🧥")
    while True:
        print("\nMenu Utama")
        print("[1] Manajemen Jaket")
        print("[2] Transaksi")
        print("[3] Laporan")
        print("[4] Keluar")
        pilih = input("Pilih menu: ")
        if pilih == '1': menu_produk()
        elif pilih == '2': menu_transaksi()
        elif pilih == '3': menu_laporan()
        elif pilih == '4':
            print("👋 Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    main()
