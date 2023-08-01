import random
import pandas as pd

# Konstanta dan variabel untuk konfigurasi genetika
JUMLAH_DOSEN = 10
JUMLAH_MAHASISWA = 30
MAX_MAHASISWA_PER_DOSEN = 3
JUMLAH_GENERASI = 100
MUTASI_PROBABILITAS = 0.1

# Pembagian bidang keilmuan dosen
BIDANG_KEILMUAN_DOSEN = {
    i: 1 if i < 6 else 2 for i in range(1, JUMLAH_DOSEN + 1)
}

# Pembagian topik keilmuan mahasiswa
TOPIC_KEILMUAN_MAHASISWA = {
    i: 1 if i <= 15 else 2 for i in range(1, JUMLAH_MAHASISWA + 1)
}

# Deskripsi bidang keilmuan
DESKRIPSI_BIDANG_KEILMUAN = {
    1: "Bidang Keilmuan 1",
    2: "Bidang Keilmuan 2"
}

# Deskripsi topik bidang keilmuan skripsi mahasiswa
DESKRIPSI_TOPIK_MAHASISWA = {
    1: "Topik Keilmuan 1",
    2: "Topik Keilmuan 2"
}

def inisialisasi_kromosom():
    return [random.randint(1, JUMLAH_DOSEN) for _ in range(JUMLAH_MAHASISWA)]

def fitness(kromosom):
    fitness_score = 0
    dosen_count = {dosen: 0 for dosen in range(1, JUMLAH_DOSEN + 1)}

    for i in range(JUMLAH_MAHASISWA):
        dosen = kromosom[i]
        bidang_dosen = BIDANG_KEILMUAN_DOSEN[dosen]
        topik_mahasiswa = TOPIC_KEILMUAN_MAHASISWA[i+1]

        if dosen_count[dosen] < MAX_MAHASISWA_PER_DOSEN and bidang_dosen == topik_mahasiswa:
            fitness_score += 1
            dosen_count[dosen] += 1

    return fitness_score

def seleksi(populasi, scores):
    return random.choices(populasi, weights=scores, k=len(populasi))

def crossover(parent1, parent2):
    pivot = random.randint(1, JUMLAH_MAHASISWA - 1)
    child1 = parent1[:pivot] + parent2[pivot:]
    child2 = parent2[:pivot] + parent1[pivot:]
    return child1, child2

def mutasi(kromosom):
    for i in range(JUMLAH_MAHASISWA):
        if random.random() < MUTASI_PROBABILITAS:
            kromosom[i] = random.randint(1, JUMLAH_DOSEN)
    return kromosom

def genetika():
    populasi = [inisialisasi_kromosom() for _ in range(JUMLAH_MAHASISWA * 10)]

    for _ in range(JUMLAH_GENERASI):
        scores = [fitness(kromosom) for kromosom in populasi]
        parents = seleksi(populasi, scores)

        next_population = []
        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i+1]
            child1, child2 = crossover(parent1, parent2)
            child1 = mutasi(child1)
            child2 = mutasi(child2)
            next_population.extend([child1, child2])

        populasi = next_population

    # Pilih kromosom terbaik dari populasi terakhir
    best_kromosom = max(populasi, key=fitness)
    return best_kromosom

def main():
    hasil_penempatan = genetika()

    data = {
        'Dosen': [],
        'Keterangan Bidang Keilmuan Dosen': [],
        'Mahasiswa': [],
        'Topik Bidang Keilmuan Skripsi Mahasiswa': []
    }

    for i in range(JUMLAH_MAHASISWA):
        dosen = hasil_penempatan[i]
        bidang_dosen = BIDANG_KEILMUAN_DOSEN[dosen]
        mahasiswa = i + 1
        topik_mahasiswa = TOPIC_KEILMUAN_MAHASISWA[i+1]

        data['Dosen'].append(f'Dosen {dosen}')
        data['Keterangan Bidang Keilmuan Dosen'].append(DESKRIPSI_BIDANG_KEILMUAN[bidang_dosen])
        data['Mahasiswa'].append(f'Mahasiswa {mahasiswa}')
        data['Topik Bidang Keilmuan Skripsi Mahasiswa'].append(DESKRIPSI_TOPIK_MAHASISWA[topik_mahasiswa])

    tabel_penempatan = pd.DataFrame(data)

    print("Hasil Penempatan:")
    print(tabel_penempatan)

    nama_file_csv = "hasil_penempatan.csv"
    tabel_penempatan.to_csv(nama_file_csv, index=False)
    print(f"Hasil penempatan telah disimpan dalam file {nama_file_csv}")

if __name__ == "__main__":
    main()
