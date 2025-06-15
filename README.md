# Applicant Tracking System - Keyword Matching
Aplikasi ini dapat melakukan pencarian sejumlah kata kunci terhadap data berupa sekumpulan file CV. Aplikasi menggunakan algoritma string matching terhadap ekstraksi teks dari file untuk mencari kemunculan kata yang identik ataupun kata yang mirip menggunakan algoritma Knuth-Morris-Pratt, Boyer-Moore, atau Aho-Corasick. Selain itu, aplikasi juga dapat melakukan ekstraksi informasi penting dari CV menggunakan regular expressions.
- Knuth-Morris-Pratt  
  Inti dari algoritma ini adalah memanfaatkan kegagalan dalam pencocokan dan melewati karakter yang sudah cocok. Ketika sebuah ketidakcocokan ditemukan, KMP menggunakan tabel bantu yang telah dihitung sebelumnya (dengan sebuah bounding function) untuk mengetahui seberapa jauh pola pencarian dapat digeser ke kanan. Hal ini memungkinkan algoritma untuk melanjutkan pencarian tanpa perlu memeriksa ulang karakter-karakter yang sudah diketahui cocok, sehingga membuat prosesnya sangat efisien.
- Boyer-Moore  
  Pada algoritma ini, pencocokan dimulai dari ujung kanan ke kiri. Algoritma ini juga melakukan prekomputasi terlebih dahulu berupa tabel kemunculan karakter dalam alfabet teks pada pattern yang ingin dicocokkan. Ketika ditemukan kegagalan pencocokan, pencocokan dapat diteruskan dengan menggeser pattern berdasarkan tabel kemunculan karakter. Hal ini memungkinkan algoritma untuk mencocokan dengan cepat dengan melakukan pergeseran beberapa karakter.
- Aho-Corasick  
  Algoritma Aho-Corasick adalah metode pencarian efisien untuk menemukan banyak kata kunci sekaligus di dalam sebuah teks hanya dalam sekali traversal. Algoritma ini bekerja dengan membangun semua kata kunci menjadi sebuah struktur data serupa dengan state machine. Saat mencari, algoritma ini menelusuri teks dan state machine tersebut. Jika terjadi ketidakcocokan, "failure links" akan memindahkannya ke state berikutnya yang paling mungkin cocok tanpa perlu mengulang pencocokan dari awal.

# Requirements
Dapat dijalankan menggunakan package manager uv. Program memiliki dependensi berikut
- PyQt6 (library GUI)
- PyMuPdf (ekstraksi pdf CV)
- Faker (seeding basis data)
- PyMySQL (library koneksi basis data)

# Instructions
  Lakukan penambahan file pdf CV terlebih dahulu dengan seeding:
  ```
  uv run src/main.py --seed PATH [ROLE]
  ```
  PATH berupa direktori yang berisi file CV dan relatif terhadap root directory program. Opsional: tag ROLE untuk posisi lamaran.

  Untuk memulai pencarian, jalankan perintah berikut:
  ```
  uv run src/main.py
  ```
  Masukkan keywords yang ingin dicari dipisahkan koma, kemudian tekan tombol pilihan algoritma pencarian yang akan digunakan. Dapat juga mengisi jumlah pencarian teratas. Tekan tombol Search untuk memulai pencarian.

# Contributors
| Nama                         | NIM      |
| :--------------------------- | :------- |
| Syahrizal Bani Khairan       | 13523063 |
| Muhammad Iqbal Haidar        | 13523111 |
| Ferdin Arsenarendra Purtadi  | 13523117 |

Untuk Tugas Besar 3  
Strategi Algoritma IF2211
