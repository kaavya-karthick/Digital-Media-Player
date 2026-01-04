# 🎵 Digital Media Player (Flask)

A modern **web-based Digital Media Player** developed using **Flask, SQLite, HTML, CSS, and JavaScript**.  
The application enables users to upload audio files, automatically organize them into albums, mark favourites, and enjoy an interactive audio playback experience with waveform visualization.

This project demonstrates **full-stack web development**, **media handling**, and **audio processing** using web technologies.

---

## 📌 Project Motivation

Traditional music players are either desktop-based or complex streaming platforms.  
This project aims to build a **lightweight, browser-based music player** that:
- Works without external APIs
- Stores music locally on the server
- Provides a modern and smooth user interface
- Helps students understand real-world media application design

---

## 🧩 System Architecture Overview

The application follows a **client–server architecture**:

1. **Client (Browser)**  
   - Displays UI  
   - Handles user interactions  
   - Plays audio using HTML5 Audio & Web Audio API  

2. **Flask Server**  
   - Handles routing and authentication  
   - Processes uploads  
   - Communicates with the database  

3. **Database (SQLite)**  
   - Stores users, songs, albums, and favourites  

4. **File Storage**  
   - Stores actual audio files on the server filesystem  

---

## ✨ Key Features (Detailed)

### 🔐 User Authentication
- Secure login system
- Prevents unauthorized access
- Enables user-specific libraries and favourites

---

### 🎶 Audio Upload & Management
- Supports `.mp3` audio files
- Files are uploaded via HTTP POST
- Stored securely on the server
- Metadata saved in the database

---

### 📁 Automatic Album Creation
Albums are created dynamically using **folder-based logic**.

#### How it Works:
- The system scans the upload directory
- Folder names are treated as album names
- All songs inside the same folder belong to one album

- uploads/
├── Leo/
│ ├── Badass.mp3
│ └── Naa Ready.mp3
├── Vikram/
│ └── Rolex.mp3

➡ Albums **Leo** and **Vikram** are generated automatically.

---

### ▶ Music Playback Controls
- Play / Pause
- Next / Previous
- Single-song loop
- Real-time playback updates

Playback uses:
- HTML5 `<audio>` element
- JavaScript for control logic

---

### 🌊 Audio-Reactive Waveform
- Built using **Web Audio API**
- Audio frequencies are analyzed in real-time
- Visual waveform reacts to sound intensity
- Enhances user experience and aesthetics

---

### 🔊 Volume Control & Persistence
- Volume slider allows real-time adjustment
- Volume level is stored locally
- Restored automatically on next visit

---

### ❤ Favourites System
- Users can mark songs as favourites
- Favourite data stored in database
- Provides quick access to liked songs

---

## 🗂 Database Design (In Detail)

### Tables Used

#### `users`
- Stores login credentials
- Manages authentication

#### `songs`
- Song title
- File path
- Album association
- Upload timestamp

#### `albums`
- Album name
- Auto-generated entries

#### `favourites`
- Many-to-many relationship between users and songs

---

## ⚙ Installation & Execution

### Step 1: Clone Repository
```bash
git clone <your-repository-url>
cd Digital_Media_Player
- Albums are created automatically in the database

#### Example:
