# DataSure React Frontend

Professional React frontend for the DataSure data validation platform.

## Tech Stack

- **React 18** - UI Library
- **TypeScript** - Type Safety
- **Vite** - Build Tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **React Dropzone** - File Upload

## Setup

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
cd backend
python main.py
# or
uvicorn main:app --reload --port 8000
```

### 4. Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

### 5. Open the Application

Navigate to `http://localhost:5173` in your browser.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.tsx           # App header
│   │   ├── ConfigSection.tsx    # Project/Report/Environment inputs
│   │   ├── FileUpload.tsx       # Drag & drop file upload
│   │   ├── ValidationResults.tsx # Results display
│   │   └── ExportSection.tsx    # Excel export button
│   ├── App.tsx                  # Main application
│   ├── types.ts                 # TypeScript interfaces
│   ├── main.tsx                 # Entry point
│   └── index.css                # Tailwind styles
├── index.html
├── package.json
├── tailwind.config.js
├── vite.config.ts
└── tsconfig.json
```

## Features

- Professional, modern UI design
- Drag & drop file upload
- Real-time validation results
- Color-coded status indicators
- Detailed breakdown of all validation checks
- Excel report export
- Responsive design for all screen sizes

## API Endpoints

The frontend communicates with the FastAPI backend:

- `POST /api/validate` - Run validation on uploaded files
- `POST /api/export-excel` - Generate and download Excel report
- `GET /api/health` - Health check endpoint
