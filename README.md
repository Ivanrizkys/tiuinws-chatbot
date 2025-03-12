# Workflows
Merupakan dokumentasi dari chatbot [tiuinws_bot](https://t.me/tiuinws_bot) yang dapat digunakan untuk dapat dijadikan panduan untuk mengelola chatbot. Disini akan dijelaskan tata cara penggunaan Workflows yang digunakan untuk dapat mengupdate chatbot dataset. Workflows pada repo ini dibagi menjadi dua yaitu [RE-Training Model](https://github.com/Ivanrizkys/tiuinws-chatbot/actions/workflows/re-training-model.yml) dan [Update JSON File](https://github.com/Ivanrizkys/tiuinws-chatbot/actions/workflows/update-json-file.yml). Kedua Workflows ini mempunyai kegunan dan fungsingya masing masing. BERHATI HATILAH DALAM MENJALANKAN WORKFLOW KARENA DAPAT MENGUBAH DATASET CHATBOT !!!

## Update JSON File

Merupakan workflow yang digunakan untuk mengupdate JSON File yang digunakan untuk dataset chatbot. Jika workflow ini dijalankan, model dari chatbot tidak akan di training ulang. Workflow ini dijalankan ketika:

- Terdapat perubahan pada column answer di suatu data yang sudah ditambahkan sebelumnya

## Re-Traning Model

Merupakan workflow yang digunakan untuk mengupdate JSON File dan melakukan traning ulang pada model yang digunakan oleh chatbot. Workflow ini dijalankan ketika:

- Terdapat penambahan data pada tabel intents
- Terdapat perubahan pada column di suatu data yang sudah ditambahkan sebelumnya
