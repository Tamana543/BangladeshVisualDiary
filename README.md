# Visual Gallery 🇧🇩📸

A personal visual diary showcasing moments, streets, people, and everyday life through photography.  
This project is designed as a simple, emotional, and minimal static website where images speak louder than words.

Created with ❤️ by **Tamana**.

---

## 🌱 Project Purpose

This project is more than a gallery.  
It is a **visual memory archive** — capturing feelings, culture, and ordinary beauty from my life. 
The goal:
- Preserve moments visually
- Practice front-end fundamentals
- Create a space that feels personal, calm, and human


---

## 🛠️ Tech Stack

- **HTML5** – structure  
- **CSS3** – layout & styling  
- **JavaScript (Vanilla)** – image handling and interaction  
- **Git & GitHub** – version control 
- **Python** - Backend Main logic
- **Flask**  - as the web framework for handling routes and API endpoints
- **Fetch API** -  communication between the frontend and backend
- **Flask-Mail**  -  sending emails with image attachments
- **MongoDB Atlas** -  Cloud NoSQL database for permanent image metadata storage
- **Gunicorn** -  Production-grade WSGI HTTP Server
- **Render** -  Cloud platform for automated deployment (CI/CD)



No frameworks. No noise. Just the essentials.

---

## 📂 Project Structure

```
BangladeshVisualDiary/
│
├── app.py              # Flask Backend (Main Engine)
├── Procfile            # Deployment instructions for Render
├── requirements.txt    # Python dependencies
├── static/             # Assets (CSS, JS, Images, JSON animations)
│   ├── css/
│   ├── Js/
│   └── default_images/ # Uploaded photos
├── templates/          # HTML files (index, 404, email_template)
└── README.md
```

---

## 🚀 How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/BangladeshVisualDiary.git
   ```

2. Install dependencies: pip install -r requirements.txt

3. Set your environment variables (MONGO_URI, MAIL_PASSWORD).

4. Run the app: python app.py

5. Visit http://127.0.0.1:5000

No build steps. No setup stress.

---

## [live](https://bangladeshvisualdiary.onrender.com/)


## ✨ What Works Well

- Clean and readable structure
- Simple logic (easy to maintain and expand)
- Emotional concept 
- Lightweight and fast
- Live Uploads: Users can contribute photos directly from the UI.
- Automated Emails: The system sends a confirmation email with an attachment whenever a photo is uploaded.
- Persistent Storage: Data is saved in the cloud (MongoDB), so it’s never lost.



---

## 🔮 What Can Be Added to Improve This Project
1. Cloud Image Hosting (Cloudinary): Move images from the local folder to a cloud CDN so they never get deleted during redeployments.

2. User Authentication: Add a login page so only you can upload or delete photos.

3. Search & Filter: Add a search bar to find photos by the "Sender" name or keywords in the description.

- let me know more :)


## Status

👩‍💻 Completed but open for more :)

---

## Author
**Tamana&lt;ReginaJS/&gt;** 

Website Developer

---

## © Copyright

© 2026 **Tamana**  
All images and content belong to the creator.


