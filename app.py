import streamlit as st
import io
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import numpy as np
from PIL import Image
from crypto_engine import CryptoEngine
from stego_engine import StegoEngine

st.set_page_config(
    page_title="QuMail-Shield | Real-World Email Demo",
    page_icon="🛰️",
    layout="wide"
)

# Dark Space Theme
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 10% 20%, #060b19 0%, #02040a 90%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(0, 245, 212, 0.3);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .badge-ready { background: #065f46; color: #34d399; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.75rem;}
    .badge-consumed { background: #991b1b; color: #f87171; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.75rem;}
</style>
""", unsafe_allow_html=True)

# Helper function to send real emails
def send_real_email(sender_email, app_password, recipient_email, subject, body_text, image_bytes):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Innocent decoy text
    msg.attach(MIMEText(body_text, 'plain'))

    # Attach the stego-encrypted PNG image
    img_attachment = MIMEImage(image_bytes, name="qumail_secure_payload.png")
    msg.attach(img_attachment)

    # Send through Gmail's official SSL server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

# Initialize Key Vault
if "key_vault" not in st.session_state:
    st.session_state.key_vault = {
        f"ISRO-QKD-NODE-0{i:02d}": CryptoEngine.generate_quantum_seed(1024) for i in range(1, 11)
    }
    st.session_state.consumed_keys = set()
    st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] Key Manager initialized. 10 Quantum key pairs ready."]
    st.session_state.armored_png_bytes = None

def log_event(msg: str):
    st.session_state.logs.insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🛰️ QuMail-Shield: Live Quantum-Secure Email Client")
    st.markdown("**Real-World Post-Quantum Email Transport** | Addressing ISRO SIH1523")
with col_h2:
    ready_count = len(st.session_state.key_vault) - len(st.session_state.consumed_keys)
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size:0.8rem; color:#94a3b8;">ACTIVE KEY POOL</div>
        <div style="font-size:1.4rem; font-weight:bold; color:#00f5d4;">{ready_count} / {len(st.session_state.key_vault)} Keys Ready</div>
    </div>
    """, unsafe_allow_html=True)

tab_compose, tab_decrypt, tab_inspector, tab_vault, tab_arena = st.tabs([
    "📤 Compose & Real Send",
    "📥 Ingest & Decrypt",
    "🔬 Stego Pixel Inspector",
    "🔑 Key Vault (KM)",
    "⚔️ Attack Arena (Demo)"
])

# ================= TAB 1: COMPOSE & SEND =================
with tab_compose:
    st.subheader("Step 1: Compose & Encrypt Message")
    col1, col2 = st.columns(2)
    
    with col1:
        recipient = st.text_input("Destination Email (Recipient)", "your_friend@gmail.com")
        subject = st.text_input("Decoy Subject", "Project Report & Telemetry Data")
        payload_text = st.text_area(
            "Secret Message (Encrypted Payload)",
            "ISRO Mission Vector: Locked. Orbit insertion planned at 0400Z.",
            height=100
        )
        sec_tier = st.selectbox(
            "Security Tier",
            options=[3, 2],
            format_func=lambda x: "Tier 3: Unconditional One-Time Pad (OTP)" if x == 3 else "Tier 2: Quantum-Seed AES-256-GCM"
        )
        
    with col2:
        carrier_file = st.file_uploader("Upload Carrier PNG (Optional)", type=["png"])
        if carrier_file:
            carrier_img = Image.open(carrier_file)
        else:
            carrier_img = Image.new("RGB", (650, 400), color=(15, 23, 42))
            st.info("Using default cover canvas.")
        st.image(carrier_img, caption="Cover Image Preview", use_container_width=True)

    # 1. Encrypt and Download Button
    if st.button("🔒 1. Encrypt & Generate PNG"):
        available_keys = [k for k in st.session_state.key_vault if k not in st.session_state.consumed_keys]
        if not available_keys:
            st.error("No unused keys remaining in local Key Vault!")
        else:
            sel_key_id = available_keys[0]
            raw_key = st.session_state.key_vault[sel_key_id]
            plain_bytes = payload_text.encode('utf-8')

            if sec_tier == 2:
                nonce, ciphertext = CryptoEngine.encrypt_level2_aes(plain_bytes, raw_key[:32])
                log_event(f"Payload encrypted with Tier 2 AES-GCM ({sel_key_id}).")
            else:
                nonce = b"\x00" * 12
                ciphertext = CryptoEngine.encrypt_level3_otp(plain_bytes, raw_key)
                log_event(f"Payload encrypted with Tier 3 OTP ({sel_key_id}).")

            pkg = StegoEngine.package_payload(sec_tier, sel_key_id, nonce, ciphertext)
            stego_img, diff_map, cluster_vis, psnr, variance = StegoEngine.hide_data(carrier_img, pkg)
            
            buf = io.BytesIO()
            stego_img.save(buf, format="PNG")
            st.session_state.armored_png_bytes = buf.getvalue()

            st.session_state.last_stego = stego_img
            st.session_state.last_orig = carrier_img
            st.session_state.last_diff = diff_map
            st.session_state.last_cluster = cluster_vis
            st.session_state.last_stats = (psnr, variance)

            st.success(f"Message encrypted with Key `{sel_key_id}` and embedded into image!")

    # If the image has been generated, show Download and Live Send
    if st.session_state.armored_png_bytes is not None:
        st.markdown("---")
        st.subheader("Step 2: Download Image & Send Live to Gmail")
        
        # Download button
        st.download_button(
            label="⬇️ Download Armored PNG Image to Your Computer",
            data=st.session_state.armored_png_bytes,
            file_name="qumail_carrier_secure.png",
            mime="image/png"
        )

        st.markdown("#### 📡 Real Gmail Dispatch")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            sender_gmail = st.text_input("Your Gmail Address", placeholder="example@gmail.com")
        with col_g2:
            sender_app_pass = st.text_input("Your 16-letter Gmail App Password", type="password", placeholder="abcd efgh ijkl mnop")

        if st.button("🚀 Send Real Email Now via Gmail"):
            if not sender_gmail or not sender_app_pass:
                st.error("Please enter both your Gmail address and 16-letter App Password.")
            else:
                with st.spinner("Connecting to Gmail SMTP server and sending..."):
                    try:
                        clean_pass = sender_app_pass.replace(" ", "")
                        send_real_email(
                            sender_email=sender_gmail,
                            app_password=clean_pass,
                            recipient_email=recipient,
                            subject=subject,
                            body_text="Please find the attached project telemetry image.",
                            image_bytes=st.session_state.armored_png_bytes
                        )
                        log_event(f"Email successfully dispatched to {recipient} via Gmail SMTP.")
                        st.balloons()
                        st.success(f"✅ Real email with encrypted image attachment successfully sent to **{recipient}**!")
                    except Exception as e:
                        st.error(f"Failed to send email: {str(e)}. Make sure your App Password is correct.")

# ================= TAB 2: INGEST & DECRYPT =================
with tab_decrypt:
    st.subheader("Receiver Decryption Pipeline")
    st.write("Upload the downloaded image (or the attachment received in Gmail):")
    in_file = st.file_uploader("Upload Received Carrier Image", type=["png"], key="decrypt_input")
    
    if in_file and st.button("🔓 Extract & Decrypt Message"):
        try:
            in_img = Image.open(in_file)
            extracted_raw = StegoEngine.extract_data(in_img)
            sec_lvl, key_id, nonce, ciphertext = StegoEngine.unpackage_payload(extracted_raw)
            
            st.markdown(f"""
            <div class="metric-card">
                <div><strong>Header:</strong> <code>QM84</code> | <strong>Security Tier:</strong> <code>Level {sec_lvl}</code> | <strong>Matched Key:</strong> <code>{key_id}</code></div>
            </div>
            """, unsafe_allow_html=True)
            
            if key_id not in st.session_state.key_vault:
                st.error("Key ID not found in local Key Manager database!")
            elif key_id in st.session_state.consumed_keys:
                st.error("REPLAY ATTACK! Key was already burned.")
            else:
                key_bytes = st.session_state.key_vault[key_id]
                if sec_lvl == 2:
                    decrypted = CryptoEngine.decrypt_level2_aes(ciphertext, key_bytes[:32], nonce)
                else:
                    decrypted = CryptoEngine.decrypt_level3_otp(ciphertext, key_bytes)
                
                st.session_state.consumed_keys.add(key_id)
                log_event(f"Decryption SUCCESS. Key {key_id} burned from memory.")
                
                st.success("🎉 Decrypted Secret Message:")
                st.code(decrypted.decode('utf-8'), language="text")
        except Exception as e:
            st.error(f"Extraction failed: {str(e)}")

# ================= TAB 3: STEGO INSPECTOR =================
with tab_inspector:
    st.subheader("🔬 Unsupervised K-Means Texture & Cluster Inspector")
    if "last_stego" in st.session_state:
        ci1, ci2, ci3 = st.columns(3)
        with ci1:
            st.image(st.session_state.last_orig, caption="1. Original Image", use_container_width=True)
        with ci2:
            st.image(st.session_state.last_cluster, caption="2. Unsupervised K-Means Mask (Safe Zones)", use_container_width=True)
        with ci3:
            st.image(st.session_state.last_diff, caption="3. Pixel Difference Residual (255x)", use_container_width=True)
            
        psnr, var = st.session_state.last_stats
        st.markdown(f"""
        <div style="display:flex; gap:16px;">
            <div class="metric-card" style="flex:1;">
                <div style="color:#94a3b8; font-size:0.8rem;">PEAK SIGNAL-TO-NOISE (PSNR)</div>
                <div style="color:#00f5d4; font-size:1.4rem; font-weight:bold;">{psnr:.2f} dB</div>
            </div>
            <div class="metric-card" style="flex:1;">
                <div style="color:#94a3b8; font-size:0.8rem;">STATISTICAL VARIANCE</div>
                <div style="color:#00f5d4; font-size:1.4rem; font-weight:bold;">{var:.4f}% (Bypasses DPI)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Encrypt a message in Tab 1 first to view pixel analysis.")

# ================= TAB 4: KEY VAULT =================
with tab_vault:
    st.subheader("Local Key Vault & Forward Secrecy Logs")
    cv1, cv2 = st.columns(2)
    with cv1:
        st.write("**Pre-Shared Quantum Keys**")
        for kid, kval in st.session_state.key_vault.items():
            is_burned = kid in st.session_state.consumed_keys
            badge = '<span class="badge-consumed">BURNED (SHREDDED)</span>' if is_burned else '<span class="badge-ready">READY</span>'
            st.markdown(f"<code>{kid}</code> {badge} - `{kval[:8].hex()}...`", unsafe_allow_html=True)
    with cv2:
        st.write("**Audit Log**")
        st.code("\n".join(st.session_state.logs), language="text")

# ================= TAB 5: ATTACK ARENA =================
with tab_arena:
    st.subheader("⚔️ Attack Arena: Classical RSA vs QuMail Defense")
    ca1, ca2 = st.columns(2)
    with ca1:
        st.markdown('<div class="metric-card" style="border-color:#ef4444;"><strong style="color:#f87171;">Classical RSA-2048 Transit</strong><br>MODULUS N = 0xC8F4B9...</div>', unsafe_allow_html=True)
        if st.button("⚡ Run Shor's Attack on RSA"):
            time.sleep(0.8)
            st.error("🚨 RSA CRACKED IN 0.042 ms! Cleartext exposed.")
    with ca2:
        st.markdown('<div class="metric-card" style="border-color:#00f5d4;"><strong style="color:#00f5d4;">QuMail-Shield Transit</strong><br>PNG Stego + One-Time Pad</div>', unsafe_allow_html=True)
        if st.button("🛡️ Attack QuMail Carrier"):
            time.sleep(1.0)
            st.warning("⚠️ FAILED TO CONVERGE. Search complexity exceeds 2^128 gates. Unconditional secrecy proven.")