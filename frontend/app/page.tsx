'use client';
import { useState, useRef } from 'react';

export default function Home() {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<{ label: string; score: number } | null>(null);
  const resultRef = useRef<HTMLDivElement>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
    }
  };

  const handleSubmit = async () => {
    if (!image) return;

    const formData = new FormData();
    formData.append('file', image);

    const res = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      body: formData,
    });

    const data = await res.json();
    setResult(data);
    setTimeout(() => {
      resultRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  return (
    <main style={{
      padding: '2rem',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      background: '#f9f9f9',
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold', marginBottom: '1rem' }}>
        🐱 ロン / サン 判定アプリ
      </h1>

      <label htmlFor="file-upload" style={{
        display: 'inline-block',
        padding: '0.5rem 1rem',
        backgroundColor: '#e0e0e0',
        borderRadius: '5px',
        cursor: 'pointer',
        fontWeight: 'bold',
        marginBottom: '1rem'
      }}>
        画像を選択 📷
      </label>
      <input
        id="file-upload"
        type="file"
        accept="image/*"
        onChange={handleChange}
        style={{ display: 'none' }}
      />

      {preview && (
        <div style={{ position: 'relative', marginTop: '1rem' }}>
          <img
            src={preview}
            alt="preview"
            width={250}
            style={{
              border: '2px solid #ccc',
              borderRadius: '8px',
              boxShadow: '0 2px 6px rgba(0, 0, 0, 0.1)'
            }}
          />
          <button
            onClick={() => {
              setImage(null);
              setPreview(null);
              setResult(null);
            }}
            style={{
              position: 'absolute',
              top: 5,
              right: 5,
              background: '#fff',
              border: '1px solid #ccc',
              borderRadius: '50%',
              width: '24px',
              height: '24px',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
          >
            ×
          </button>
        </div>
      )}

      <div style={{ marginTop: '1.5rem' }}>
        <button
          onClick={handleSubmit}
          style={{
            padding: '0.5rem 1.5rem',
            backgroundColor: '#4f46e5',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '1rem',
            fontWeight: 'bold'
          }}
          onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#4338ca')}
          onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#4f46e5')}
        >
          判定する
        </button>
      </div>

      {result && (
        <div ref={resultRef} style={{
          marginTop: '2rem',
          padding: '1rem',
          backgroundColor: '#e8f0fe',
          border: '1px solid #90caf9',
          borderRadius: '8px',
          textAlign: 'center',
          width: '100%',
          maxWidth: '300px'
        }}>
          <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
            結果: {result.label === 'lon' ? 'ロン' : 'サン'}
          </p>
          <p style={{ marginTop: '0.5rem' }}>
            （約{Math.round((result.label === 'lon' ? 1 - result.score : result.score) * 100)}% の確信）
          </p>
        </div>
      )}
    </main>
  );
}