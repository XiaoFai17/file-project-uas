import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from docx import Document
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd

# Pastikan untuk mengunduh daftar stop words jika belum dilakukan
nltk.download('stopwords')

# Custom CSS styles
st.markdown(
    f"""
    <style>
    body {{
        background-color: #f5f5f5; /* Light Grey */
        font-family: Arial, sans-serif;
    }}
    .stTextInput input {{
        background-color: #ffffff; /* White */
        color: #000000; /* Black */
        border: 2px solid #cccccc; /* Light Grey */
        border-radius: 5px;
        padding: 10px;
    }}
    .stTextInput label {{
        color: #000000; /* Black */
    }}
    .stButton button {{
        background-color: #008CBA; /* Dark Blue */
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
    }}
    .stSuccess {{
        background-color: #4CAF50; /* Green */
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }}
    .stWarning {{
        background-color: #FF5722; /* Orange */
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Application Title
st.title("Kalkulator Kesamaan Teks")

# Input options
input_method = st.radio("Pilih metode input:", ("Input Teks", "Unggah File .docx"))

text1 = ""
text2 = ""

if input_method == "Input Teks":
    # Text Input
    text1 = st.text_area("Masukkan Teks 1:", "", key="text1")
    text2 = st.text_area("Masukkan Teks 2:", "", key="text2")

elif input_method == "Unggah File .docx":
    # File Upload
    uploaded_file1 = st.file_uploader("Unggah Dokumen 1 (.docx)", type="docx")
    uploaded_file2 = st.file_uploader("Unggah Dokumen 2 (.docx)", type="docx")

    if uploaded_file1 is not None:
        document1 = Document(uploaded_file1)
        text1 = "\n".join([para.text for para in document1.paragraphs])

    if uploaded_file2 is not None:
        document2 = Document(uploaded_file2)
        text2 = "\n".join([para.text for para in document2.paragraphs])

# Text Cleaning Function
def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters, numbers, titik, koma, dan tanda petik
    text = re.sub(r'[.,\'"]', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Ambil daftar stop words dari nltk
    stop_words = set(stopwords.words('indonesian'))  
    
    # Hapus stop words
    text = ' '.join(word for word in text.split() if word not in stop_words)
    
    return text

# Function to generate and display WordCloud
def generate_wordcloud(text, title):
    wordcloud = WordCloud(width=400, height=200, background_color='white').generate(text)
    
    # Display WordCloud
    plt.figure(figsize=(5, 3))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    st.pyplot(plt)

if st.button("Hitung Kesamaan"):
    if not text1 or not text2:
        st.warning("Harap masukkan kedua teks.")
    else:
        # Clean the text
        text1 = clean_text(text1)
        text2 = clean_text(text2)

        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])

        # Display TF-IDF matrix
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
        st.subheader("Matriks TF-IDF")
        st.write(tfidf_df)

        # Mengurutkan nilai TF-IDF dari yang terbesar ke terkecil
        sorted_tfidf_df = tfidf_df.T.sort_values(by=0, ascending=False)
        st.subheader("Matriks TF-IDF (Terurut)")
        st.write(sorted_tfidf_df)

        # Calculate Cosine Similarity
        cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

        # Show Result
        st.success(f"Nilai Kesamaan antara teks: {cosine_sim:.2f}")

        # Generate WordCloud for both texts
        combined_text = text1 + " " + text2
        generate_wordcloud(text1, "Visualisasi kesamaan Kata di Dokumen 1")
        generate_wordcloud(text2, "Visualisasi kesamaan Kata di Dokumen 2")
        generate_wordcloud(combined_text, "Visualisasi kesamaan Kata di Gabungan Dokumen")

        # Menampilkan kata-kata yang sama di kedua dokumen
        words1 = set(text1.split())
        words2 = set(text2.split())
        common_words = words1.intersection(words2)

        if common_words:
            st.subheader("Kata yang Sama di Kedua Dokumen")
            st.write(", ".join(common_words))
        else:
            st.warning("Tidak ada kata yang sama di kedua dokumen.")

# Text Suggestions
st.subheader("Cara Penggunaan Aplikasi")
st.write("- Gunakan kotak input teks di atas atau unggah file .docx untuk menghitung kesamaan antara dua teks.")
st.write("- Klik tombol 'Hitung Kesamaan' untuk melihat kesamaan teks ataupun dokumen.")

if __name__ == "__main__":
    st.write("Untuk menjalankan aplikasi, gunakan opsi 'Run' dari menu di sisi kiri.")