# SOAL 1: Deret Fibonacci
def fibonacci(n):
    """Menghasilkan deret Fibonacci dengan n elemen"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    deret = [0, 1]
    for i in range(2, n):
        deret.append(deret[i-1] + deret[i-2])
    
    return deret

# Test deret Fibonacci
print("SOAL 1: Deret Fibonacci")
print(f"Deret 9 angka pertama: {fibonacci(9)}")
print()

# SOAL 2: Keuntungan Saham Terbaik
def keuntungan_saham_terbaik(harga):
    """
    Mencari keuntungan terbaik dari jual-beli saham
    Membeli di harga terendah dan menjual di harga tertinggi setelahnya
    """
    if len(harga) < 2:
        return 0
    
    keuntungan_max = 0
    harga_beli_min = harga[0]
    
    for i in range(1, len(harga)):
        # Hitung keuntungan jika menjual di hari ini
        keuntungan_sekarang = harga[i] - harga_beli_min
        
        # Update keuntungan maksimum
        keuntungan_max = max(keuntungan_max, keuntungan_sekarang)
        
        # Update harga beli minimum
        harga_beli_min = min(harga_beli_min, harga[i])
    
    return keuntungan_max

# Test keuntungan saham
print("SOAL 2: Keuntungan Saham Terbaik")
contoh = [10, 9, 6, 5, 15]
print(f"Contoh {contoh}: {keuntungan_saham_terbaik(contoh)}")

# Soal-soal yang diminta
soal2_1 = [7, 8, 3, 10, 8]
soal2_2 = [5, 12, 11, 12, 10]
soal2_3 = [7, 18, 27, 10, 29]
soal2_4 = [20, 17, 15, 14, 10]

print(f"1. {soal2_1}: {keuntungan_saham_terbaik(soal2_1)}")
print(f"2. {soal2_2}: {keuntungan_saham_terbaik(soal2_2)}")
print(f"3. {soal2_3}: {keuntungan_saham_terbaik(soal2_3)}")
print(f"4. {soal2_4}: {keuntungan_saham_terbaik(soal2_4)}")
print()

# SOAL 3: Menghitung Angka dalam List Campuran
def hitung_angka(arr):
    """Menghitung berapa banyak angka (tipe int) dalam list campuran"""
    count = 0
    for item in arr:
        if isinstance(item, int):
            count += 1
    return count

# Test hitung angka
print("SOAL 3: Menghitung Angka dalam List")
contoh3 = [2, 'h', 6, 'u', 'y', 't', 7, 'j', 'y', 'h', 8]
print(f"Contoh {contoh3}: {hitung_angka(contoh3)}")

# Soal-soal yang diminta
soal3_1 = ['b', 7, 'h', 6, 'h', 'k', 'i', 5, 'g', 7, 8]
soal3_2 = [7, 'b', 8, 5, 6, 9, 'n', 'f', 'y', 6, 9]
soal3_3 = ['u', 'h', 'b', 'n', 7, 6, 5, 1, 'g', 7, 9]

print(f"1. {soal3_1}: {hitung_angka(soal3_1)}")
print(f"2. {soal3_2}: {hitung_angka(soal3_2)}")
print(f"3. {soal3_3}: {hitung_angka(soal3_3)}")

# PENJELASAN ALGORITMA
print("\n" + "="*50)
print("PENJELASAN ALGORITMA:")
print("="*50)

print("\n1. FIBONACCI:")
print("   - Dimulai dengan [0, 1]")
print("   - Setiap angka berikutnya = jumlah 2 angka sebelumnya")
print("   - Contoh: 0+1=1, 1+1=2, 1+2=3, 2+3=5, dst.")

print("\n2. KEUNTUNGAN SAHAM:")
print("   - Cari harga terendah untuk membeli")
print("   - Cari harga tertinggi setelah membeli untuk menjual")
print("   - Keuntungan = Harga Jual - Harga Beli")
print("   - Algoritma: tracking harga minimum dan keuntungan maksimum")

print("\n3. HITUNG ANGKA:")
print("   - Iterasi setiap elemen dalam list")
print("   - Gunakan isinstance(item, int) untuk cek tipe data")
print("   - Increment counter jika bertemu angka (integer)")