import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [markdown, setMarkdown] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMarkdown("");
    setError("");
  };

  const handleConvert = async () => {
    if (!file) {
      setError("Please choose a PDF file first!");
      return;
    }

    setLoading(true);
    setError("");
    setMarkdown("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMarkdown(data.markdown);
        downloadMarkdown(data.markdown);
      } else {
        setError(data.error || "Conversion failed.");
      }
    } catch (err) {
      setError("Server not reachable. Please check Flask backend.");
    } finally {
      setLoading(false);
    }
  };

  const downloadMarkdown = (text) => {
    const blob = new Blob([text], { type: "text/markdown" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${file.name.replace(".pdf", "")}.md`;
    link.click();
  };

  const styles = {
    body: {
      backgroundColor: "#0f172a",
      color: "white",
      fontFamily: "Inter, sans-serif",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      margin: 0,
    },
    container: {
      textAlign: "center",
      background: "#1e293b",
      padding: "40px",
      borderRadius: "16px",
      boxShadow: "0 0 25px rgba(0, 0, 0, 0.2)",
      width: "450px",
    },
    button: {
      backgroundColor: "#3b82f6",
      color: "white",
      border: "none",
      padding: "10px 25px",
      borderRadius: "8px",
      cursor: "pointer",
      transition: "0.3s ease",
      fontSize: "16px",
    },
    disabledButton: {
      backgroundColor: "gray",
      cursor: "not-allowed",
    },
    error: {
      color: "#ef4444",
      marginTop: "15px",
    },
    textarea: {
      width: "100%",
      backgroundColor: "#0f172a",
      color: "#e2e8f0",
      border: "1px solid #334155",
      borderRadius: "8px",
      padding: "10px",
      fontSize: "14px",
      resize: "none",
    },
    footer: {
      marginTop: "25px",
      fontSize: "12px",
      color: "#94a3b8",
    },
  };

  return (
    <div style={styles.body}>
      <div style={styles.container}>
        <h1>PDF to Markdown</h1>

        <input type="file" accept=".pdf" onChange={handleFileChange} />

        <div style={{ marginTop: "20px" }}>
          <button
            onClick={handleConvert}
            disabled={loading}
            style={{
              ...styles.button,
              ...(loading ? styles.disabledButton : {}),
            }}
          >
            {loading ? "Converting..." : "Convert"}
          </button>
        </div>

        {error && <p style={styles.error}>{error}</p>}

        {markdown && (
          <div style={{ marginTop: "30px", textAlign: "left" }}>
            <h3>Converted Markdown:</h3>
            <textarea value={markdown} readOnly rows={15} style={styles.textarea}></textarea>
          </div>
        )}

        <footer style={styles.footer}>Made with ❤️ using React × Flask</footer>
      </div>
    </div>
  );
}

export default App;
