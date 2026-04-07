import base64
import os
import cv2
import numpy as np
from deepface import DeepFace
from config import ETALON_PATH, FACE_THRESHOLD, MODEL_NAME

def save_and_verify(base64_data, user_id):
    try:
        # 1. Rasmni base64'dan o'qish
        header, encoded = base64_data.split(",", 1)
        data = base64.b64decode(encoded)
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 2. Rasm mavjudligini tekshirish (Qorong'u ekran yoki xato uchun)
        if img is None: return False, 1.0, "⚠️ Suwret qabıllanbadı. Qayta urınıń."

        # 3. Rasm sifatini va yuzni aniqlashni tekshirish (Liveness Detection elementlari)
        # DeepFace enforce_detection orqali yuz bormi-yo'qligini aniqlaydi.
        try:
            temp_filename = f"temp_{user_id}.jpg"
            cv2.imwrite(temp_filename, img)
            
            # 4. Solishtirish (Verification)
            result = DeepFace.verify(img1_path=temp_filename, 
                                     img2_path=ETALON_PATH, 
                                     model_name=MODEL_NAME, 
                                     enforce_detection=True) # Yuz bormi-yo'qligini qat'iy tekshirish
            
            dist = result['distance']
            verified = dist <= FACE_THRESHOLD # 90% o'xshashlik
            
            if os.path.exists(temp_filename): os.remove(temp_filename)
            
            if verified:
                return True, dist, "✅ Shaxs tastıqlandı!"
            else:
                return False, dist, "❌ Júz uqsas emes!"
                
        except Exception as e:
            if os.path.exists(temp_filename): os.remove(temp_filename)
            return False, 1.0, "⚠️ Júzińiz kórınbedı. Jarıq orında turıp qaytadan urınıń."
            
    except Exception as e:
        return False, 1.0, f"⚠️ Qáte: {str(e)}"