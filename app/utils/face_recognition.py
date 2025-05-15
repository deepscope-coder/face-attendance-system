import cv2
import numpy as np
from insightface.app import FaceAnalysis
from pinecone import Pinecone
from config import Config

CLASS_NAMES = {
    '01': 'ARIFUL MALLICK',
    '02': 'NANDANA MUKHERJEE',
    '03': 'SURAJIT MISHRA',
    '04': 'ATANU MANNA',
    '05': 'SWAGATA NANDA',
    '06': 'SHADAN ALAM'
}

class FaceRecognizer:
    def __init__(self):
        self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        self.index = self.pc.Index(
            host=Config.PINECONE_INDEX_HOST,
            name=Config.PINECONE_INDEX_NAME
        )
        self.app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
        self.app.prepare(ctx_id=0)
        self.accuracy_threshold = 0.65  # 75% threshold

    def recognize_face(self, face_embedding):
        try:
            query_result = self.index.query(
                vector=face_embedding.tolist(),
                top_k=1,
                include_metadata=True
            )
            
            if not query_result["matches"]:
                return {"status": "no_match", "message": "No match found in database", "score": 0.0}
            
            match = query_result["matches"][0]
            if match["score"] >= self.accuracy_threshold:
                class_id = match["metadata"]["label"]
                full_name = CLASS_NAMES.get(class_id, "Unknown")
                return {
                    "status": "success",
                    "class_id": class_id,
                    "name": full_name,
                    "score": float(match["score"])
                }
            else:
                return {
                    "status": "low_confidence",
                    "message": "Sorry, you are not in our system (low confidence)",
                    "score": float(match["score"])
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Recognition error: {str(e)}",
                "score": 0.0
            }

    def capture_and_recognize(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return {
                    "status": "error",
                    "message": "Failed to open camera",
                    "score": 0.0
                }

            print("📷 Press SPACE to capture | Press ESC to exit")

            while True:
                ret, frame = cap.read()
                if not ret:
                    return {
                        "status": "error",
                        "message": "Failed to read from camera",
                        "score": 0.0
                    }

                cv2.imshow("Webcam - Face Recognition", frame)

                key = cv2.waitKey(1)
                if key % 256 == 27:  # ESC pressed
                    return {
                        "status": "canceled",
                        "message": "Recognition canceled",
                        "score": 0.0
                    }
                elif key % 256 == 32:  # SPACE pressed
                    print("📸 Captured image. Processing...")
                    faces = self.app.get(frame)
                    if not faces:
                        return {
                            "status": "no_face",
                            "message": "No face detected",
                            "score": 0.0
                        }
                    
                    emb = faces[0].embedding
                    result = self.recognize_face(emb)
                    
                    if result["status"] == "success":
                        # Draw bounding box and save image
                        bbox = faces[0].bbox.astype(int)
                        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
                        cv2.putText(frame, 
                                   f"{result['name']} ({result['score']:.2f})", 
                                   (bbox[0], bbox[1] - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        cv2.imwrite('app/static/captured.jpg', frame)
                    
                    return result

        finally:
            if 'cap' in locals():
                cap.release()
            cv2.destroyAllWindows()