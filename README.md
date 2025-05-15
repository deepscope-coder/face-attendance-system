🧠 Face Recognition Attendance System
This project is a full-stack face recognition-based attendance system built using:

InsightFace for face detection and embedding.

Pinecone vector database for face similarity search.

Flask for the web interface.

PostgreSQL for attendance record storage.

Integration with Roboflow for dataset management.

📸 Features
Extract frames from videos to build datasets.

Train on face embeddings using InsightFace.

Upload embeddings to Pinecone for similarity matching.

Real-time photo capture and recognition in Google Colab.

Flask-based web portal for:

Face recognition via photo.

Attendance logging (enter/exit).

View recent attendance history.

Robust handling of repeated entries and exits.

🚀 Quick Start
1. 📦 Install Dependencies
bash
Copy
Edit
pip install roboflow insightface onnxruntime faiss-cpu opencv-python-headless matplotlib scikit-learn tqdm flask sqlalchemy python-dotenv
If using Pinecone:

bash
Copy
Edit
pip install -U pinecone-client
2. 📥 Download Training Dataset from Roboflow
python
Copy
Edit
from roboflow import Roboflow

rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("YOUR_WORKSPACE").project("face-tlml4")
version = project.version(1)
dataset = version.download("folder")
3. 🧠 Extract Face Embeddings
python
Copy
Edit
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])  # or CUDAExecutionProvider for GPU
app.prepare(ctx_id=0)

# Loop through training data to extract embeddings
4. 🧠 Upload Embeddings to Pinecone
python
Copy
Edit
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="YOUR_PINECONE_API_KEY")
index_name = "face-embeddings"

# Create index if not exists
pc.create_index(
    name=index_name,
    dimension=512,
    metric="cosine",
    spec=ServerlessSpec(cloud="gcp", region="us-west1")
)

index = pc.Index(index_name)
index.upsert([...])  # Upload embeddings in batch
5. 📷 Real-Time Face Recognition in Colab
Use webcam-based photo capture and run inference:

python
Copy
Edit
from IPython.display import display, Javascript
from google.colab import output
Detect face → Get embedding → Query Pinecone → Return label and score.

6. 🌐 Flask Web App for Attendance
⚙️ Setup
Set up environment variables in .env:

env
Copy
Edit
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/face_attendance
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX_NAME=face-embeddings
Initialize the database:

bash
Copy
Edit
python initialize_db.py
▶️ Run the App
bash
Copy
Edit
python run.py
📁 Project Structure
arduino
Copy
Edit
.
├── app/
│   ├── models.py          # Attendance DB model
│   ├── routes.py          # Flask route handlers
│   ├── utils/
│   │   └── face_recognition.py  # Pinecone-based recognition
│   └── static/
│       └── captured.jpg   # Saved recognized image
├── templates/
│   ├── home.html
│   ├── recognized.html
│   └── not_recognized.html
├── config.py
├── run.py
├── initialize_db.py
├── requirements.txt
└── README.md
🗃️ Database Schema
attendance Table:
Field	Type	Description
id	Integer	Primary key
person_name	String	Detected person’s name
class_id	String	Group/class identifier
action	String	"enter" or "exit"
timestamp	DateTime	Timestamp of action
entry_time	DateTime	Entry time (nullable)
exit_time	DateTime	Exit time (nullable)
duty_duration	Interval	Time duration between entry & exit

🔐 Security Notes
Use environment variables (.env) for all secrets and keys.

Limit the number of face queries per second if using public APIs.

Enable HTTPS for production deployments.

📚 Future Improvements
Add user registration and admin panel.

Add support for mobile camera capture.

Improve recognition accuracy via face alignment.


👨‍💻 Author
Arif M.

📄 License
This project is licensed under the MIT License.