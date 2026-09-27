QuMail-Shield — Quantum-Secure Email Client with ML Steganography

QuMail-Shield is a quantum-resilient, steganographic email platform engineered for ISRO (SIH1523). It enables secure end-to-end payload transmission over standard Gmail SMTP infrastructure without requiring network changes by embedding encrypted data inside high-texture image regions using Machine Learning.

🔒 System Architecture

Three-Tier Cryptographic Engine: Integrates AES-256-GCM authenticated encryption with One-Time Pad (OTP) logic for maximum data confidentiality.

Unsupervised ML Steganography: Employs a K-Means clustering algorithm to analyze cover images (PNG) and identify high-texture regions, ensuring embedded payloads remain invisible to network scanners.

Forward Secrecy Key Manager: Local daemon scripts enforce forward secrecy by shredding encryption keys immediately after single-use consumption.

Streamlit Dashboard: An intuitive dashboard providing seamless key management, payload embedding, and direct Gmail SMTP dispatch workflows.

📁 Repository Structure

QuMail-Shield/
├── crypto/              # AES-256-GCM & OTP encryption modules
├── stego_ml/            # K-Means texture analysis & image steganography engine
├── key_manager/         # Key Manager daemons & key-shredding logic
├── app.py               # Main Streamlit dashboard interface
├── requirements.txt     # Python dependencies
├── .gitignore           # Ignored files, keys, and virtual environments
└── README.txt           # Repository documentation

🛠️ Tech Stack & Dependencies

Language: Python 3.x

Machine Learning: Scikit-Learn (Unsupervised K-Means)

Cryptography: PyCryptodome / Cryptography (AES-256-GCM, OTP)

User Interface: Streamlit

Protocols: Gmail SMTP / MIME Messaging

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/YOUR_USERNAME/QuMail-Shield.git
cd QuMail-Shield

2. Set Up Virtual Environment & Install Dependencies

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

3. Launch the Application

streamlit run app.py

👤 Author

Jaiganapathi Senthil Bhuvaneswari

Computer Science & Engineering Student @ Sathyabama Institute of Science & Technology
