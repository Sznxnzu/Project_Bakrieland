import streamlit as st
import streamlit.components.v1 as components
import base64
import io
from PIL import Image

# HTML dan JavaScript untuk mengambil tangkapan layar dari sisi klien (browser pengguna)
# Menggunakan html2canvas untuk menangkap konten halaman Streamlit.
CLIENT_SIDE_SCREEN_CAPTURE_HTML = """
<script src="https://unpkg.com/streamlit-component-lib/dist/streamlit-component-lib.js"></script>
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
<style>
  body {
    font-family: 'Inter', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 200px;
    padding: 20px;
    background-color: #f0f2f6;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  button {
    background-color: #4CAF50; /* Green */
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 12px;
    transition: background-color 0.3s ease, transform 0.2s ease;
    box-shadow: 0 4px #999;
  }
  button:hover { background-color: #45a049; }
  button:active {
    background-color: #3e8e41;
    box-shadow: 0 2px #666;
    transform: translateY(2px);
  }
  #status-message {
      margin-top: 15px;
      font-size: 0.9em;
      color: #333;
      text-align: center;
      min-height: 20px; /* Reserve space */
  }
  #preview-img {
      max-width: 100%;
      height: auto;
      margin-top: 20px;
      border: 1px solid #ddd;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.08);
      display: none; /* Hidden by default */
  }
</style>
<div>
  <p>Tekan tombol di bawah ini untuk menangkap tampilan halaman Streamlit ini.</p>
  <button id="captureButton">Tangkap Halaman Ini</button>
  <p id="status-message"></p>
  <img id="preview-img" alt="Pratinjau Tangkapan Halaman">
</div>

<script>
  const captureButton = document.getElementById('captureButton');
  const statusMessage = document.getElementById('status-message');
  const previewImg = document.getElementById('preview-img');

  // Fungsi untuk memperbarui pesan status di UI
  function updateStatus(message, type = 'info') {
      statusMessage.style.color = type === 'error' ? 'red' : (type === 'success' ? 'green' : '#333');
      statusMessage.innerText = message;
  }

  // Event listener untuk tombol tangkap layar
  captureButton.onclick = async () => {
    updateStatus("Sedang menangkap halaman... Mohon tunggu sebentar. ⏳");
    previewImg.style.display = 'none'; // Sembunyikan pratinjau sebelumnya

    try {
      // html2canvas akan menangkap elemen body dari iframe ini.
      // Jika Streamlit app memiliki container utama, bisa juga ditargetkan
      // seperti document.querySelector('#main-content') jika ada ID tersebut.
      // window.parent.document.body
      const canvas = await html2canvas(document.body, {
          scale: window.devicePixelRatio, // Menjaga kualitas di layar HiDPI (Retina)
          logging: false, // Nonaktifkan logging di console
          useCORS: true // Penting jika ada gambar dari domain lain
      });

      // Ubah konten canvas menjadi Data URL (Base64 encoded PNG)
      const imageDataUrl = canvas.toDataURL('image/png');

      // Tampilkan pratinjau gambar di dalam komponen HTML itu sendiri
      previewImg.src = imageDataUrl;
      previewImg.style.display = 'block';

      updateStatus("Halaman berhasil ditangkap! Data dikirim ke Streamlit. ✨", 'success');

      // Kirim data gambar (Data URL) kembali ke Streamlit
      if (window.parent && window.parent.Streamlit) {
          window.parent.Streamlit.setComponentValue(imageDataUrl);
      } else {
          updateStatus("Error: Objek Streamlit parent tidak ditemukan. Tidak dapat mengirim data kembali.", 'error');
      }

    } catch (err) {
        updateStatus(`Terjadi kesalahan saat menangkap halaman: ${err.message} 😞`, 'error');
        // Kirim null kembali ke Streamlit untuk mengindikasikan kegagalan
        if (window.parent && window.parent.Streamlit) {
            window.parent.Streamlit.setComponentValue(null);
        }
    }
  };

  // Beri tahu Streamlit bahwa komponen HTML siap
  if (window.parent && window.parent.Streamlit) {
    window.parent.Streamlit.setComponentReady();
  }
</script>
"""

st.set_page_config(page_title="Tangkap Halaman Streamlit", layout="centered")

st.title("📸 Tangkap Halaman Streamlit Ini")
st.markdown("""
Aplikasi ini memungkinkan Anda mengambil tangkapan gambar dari **halaman Streamlit ini** yang sedang Anda lihat di browser Anda.
Setelah ditangkap, Anda dapat mengunduh gambar tersebut.

**Penting:**
* Ini akan menangkap tampilan halaman Streamlit yang terlihat di browser Anda, bukan seluruh layar perangkat Anda.
* Ketika Anda mengunduh gambar di ponsel, perilaku penyimpanannya (misalnya, langsung ke galeri atau ke folder "Downloads") akan tergantung pada browser dan sistem operasi ponsel Anda.
""")

# Menampilkan komponen HTML/JavaScript
# Kita berikan key unik agar Streamlit tahu kapan komponen ini berubah atau perlu di-rerender
# height disesuaikan agar tombol dan pesan status terlihat jelas
screenshot_data_url = components.html(
    CLIENT_SIDE_SCREEN_CAPTURE_HTML,
    height=350, # Sesuaikan tinggi komponen agar muat
    scrolling=False,
    key="client_screenshot_capture_html2canvas" # Mengubah key agar unik
)

# Jika data tangkapan layar diterima dari komponen JavaScript
if screenshot_data_url:
    try:
        # Hapus bagian "data:image/png;base64," dari Data URL
        # Pastikan data dimulai dengan "data:image/png;base64,"
        if screenshot_data_url.startswith("data:image/png;base64,"):
            encoded_data = screenshot_data_url.split(",", 1)[1]
        else:
            # Jika format tidak sesuai, mungkin ada error atau data tidak lengkap
            raise ValueError("Format Data URL tidak valid.")

        # Decode string Base64 menjadi bytes
        image_bytes = base64.b64decode(encoded_data)

        # Tampilkan gambar yang ditangkap
        st.subheader("Hasil Tangkapan Halaman Anda:")
        st.image(image_bytes, caption="Tangkapan Halaman Streamlit Anda", use_column_width=True)

        # Menawarkan tombol unduh kepada pengguna
        st.download_button(
            label="💾 Unduh Tangkapan Halaman",
            data=image_bytes,
            file_name="tangkapan_halaman_streamlit.png",
            mime="image/png"
        )
        st.success("Tangkapan halaman berhasil diterima dan ditampilkan! ✨")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses gambar yang diterima: {e} 😞")
elif screenshot_data_url is None: # Ini akan terjadi jika JS mengirim null (misal user cancel atau error)
    st.warning("Tangkapan halaman dibatalkan atau tidak ada gambar yang diambil.")