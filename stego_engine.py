import struct
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

MAGIC_HEADER = b"QM84"

class StegoEngine:
    @staticmethod
    def package_payload(sec_level: int, key_id: str, nonce: bytes, payload: bytes) -> bytes:
        """Binary Packet Envelope."""
        key_id_bytes = key_id.encode('utf-8')
        header = struct.pack(
            f">4sBB{len(key_id_bytes)}sB{len(nonce)}sI",
            MAGIC_HEADER,
            sec_level,
            len(key_id_bytes),
            key_id_bytes,
            len(nonce),
            nonce,
            len(payload)
        )
        return header + payload

    @staticmethod
    def unpackage_payload(raw_bytes: bytes):
        """Extracts envelope components."""
        if not raw_bytes.startswith(MAGIC_HEADER):
            raise ValueError("No genuine QM84 quantum signature found in carrier!")
        
        offset = 4
        sec_level, k_len = struct.unpack_from(">BB", raw_bytes, offset)
        offset += 2
        
        key_id = raw_bytes[offset:offset+k_len].decode('utf-8')
        offset += k_len
        
        n_len = struct.unpack_from(">B", raw_bytes, offset)[0]
        offset += 1
        
        nonce = raw_bytes[offset:offset+n_len]
        offset += n_len
        
        p_len = struct.unpack_from(">I", raw_bytes, offset)[0]
        offset += 4
        
        payload = raw_bytes[offset:offset+p_len]
        return sec_level, key_id, nonce, payload

    @staticmethod
    def extract_unsupervised_feature_mask(arr: np.ndarray) -> np.ndarray:
        """
        UNSUPERVISED LEARNING CORE (MSB Invariant):
        Uses Most Significant Bits (0xFE) to extract gradient features.
        Guarantees cover and stego produce identical clusters.
        """
        arr_msb = arr & np.uint8(0xFE)
        gray = np.mean(arr_msb, axis=2)
        
        gy, gx = np.gradient(gray)
        grad_mag = np.sqrt(gx**2 + gy**2)
        features = grad_mag.flatten().reshape(-1, 1)
        
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=3)
        cluster_labels = kmeans.fit_predict(features)
        
        high_texture_cluster = np.argmax(kmeans.cluster_centers_)
        mask = (cluster_labels == high_texture_cluster).astype(np.uint8)
        return mask.reshape(gray.shape)

    @staticmethod
    def hide_data(cover_img: Image.Image, raw_payload: bytes):
        """Embeds data into pixels selected by Unsupervised K-Means."""
        img = cover_img.convert("RGB")
        orig_arr = np.array(img, dtype=np.uint8)
        flat_orig = orig_arr.flatten()
        
        unsup_mask = StegoEngine.extract_unsupervised_feature_mask(orig_arr)
        flat_mask = np.repeat(unsup_mask.flatten(), 3)
        allowed_indices = np.where(flat_mask == 1)[0]
        
        total_data = struct.pack(">I", len(raw_payload)) + raw_payload
        bits = np.unpackbits(np.frombuffer(total_data, dtype=np.uint8))

        if len(bits) > len(flat_orig):
            raise ValueError(f"Message too long for this image! Needs {len(bits)} bits.")

        if len(bits) > len(allowed_indices):
            allowed_indices = np.arange(len(flat_orig))

        flat_stego = flat_orig.copy()
        target_indices = allowed_indices[:len(bits)]
        
        # FIX: Explicit uint8 bitwise masking with 0xFE (254) to prevent negative overflow
        flat_stego[target_indices] = (flat_stego[target_indices] & np.uint8(0xFE)) | bits.astype(np.uint8)
        
        stego_arr = flat_stego.reshape(orig_arr.shape)

        # Residual Metrics
        diff = np.abs(orig_arr.astype(int) - stego_arr.astype(int)).astype(np.uint8)
        diff_heatmap = diff * 255
        
        psnr = 10 * np.log10((255 ** 2) / (np.mean((orig_arr - stego_arr) ** 2) + 1e-10))
        variance = (np.sum(diff) / orig_arr.size) * 100
        cluster_vis = (unsup_mask * 255).astype(np.uint8)

        return Image.fromarray(stego_arr), diff_heatmap, cluster_vis, psnr, variance

    @staticmethod
    def extract_data(stego_img: Image.Image) -> bytes:
        """Extracts embedded payload using MSB-Invariant K-Means."""
        img = stego_img.convert("RGB")
        arr = np.array(img, dtype=np.uint8)
        flat_arr = arr.flatten()
        
        unsup_mask = StegoEngine.extract_unsupervised_feature_mask(arr)
        flat_mask = np.repeat(unsup_mask.flatten(), 3)
        allowed_indices = np.where(flat_mask == 1)[0]

        if len(allowed_indices) < 32:
            allowed_indices = np.arange(len(flat_arr))

        len_indices = allowed_indices[:32]
        len_bits = flat_arr[len_indices] & np.uint8(1)
        len_bytes = np.packbits(len_bits).tobytes()
        total_len = struct.unpack(">I", len_bytes)[0]

        total_bits_count = (4 + total_len) * 8
        if len(allowed_indices) < total_bits_count:
            allowed_indices = np.arange(len(flat_arr))
            
        data_indices = allowed_indices[:total_bits_count]
        all_bits = flat_arr[data_indices] & np.uint8(1)
        extracted_bytes = np.packbits(all_bits).tobytes()

        return extracted_bytes[4:]