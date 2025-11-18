# Treatment Plan PDF Generator

A serverless API for generating treatment plan PDFs, deployed on Vercel.

## Features

- Generate PDF treatment plans from JSON data
- Serverless architecture on Vercel
- RESTful API endpoint

## API Endpoints

### POST `/api/generate-pdf`

Generate a PDF treatment plan.

**Request Body:**
```json
{
  "title": "Treatment Plan",
  "billed_to": "Amir_",
  "treatments": [
    {
      "name": "Stem Cell Derived Exosomes",
      "note": "20 billion exosomes"
    }
  ],
  "total": "£3000"
}
```

**Response:**
- Returns PDF file as download

### GET `/api/health`

Health check endpoint.

### GET `/`

API information endpoint.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run locally:
```bash
python api/index.py
```

Or use Flask's development server:
```bash
export FLASK_APP=api/index.py
flask run
```

## Deployment to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel
```

4. For production:
```bash
vercel --prod
```

## GitHub Integration

This repository is connected to GitHub. You can also deploy via:

1. Push to GitHub
2. Import project in Vercel dashboard
3. Connect your GitHub repository
4. Vercel will auto-deploy on every push

## Notes

- Make sure `template_clean.jpg` is in the root directory if you want to use a background template
- The API accepts JSON data and returns PDF files
- All PDFs are generated in memory (no file system storage)

## Example Usage

```bash
curl -X POST https://your-app.vercel.app/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Treatment Plan",
    "billed_to": "Amir_",
    "treatments": [
      {
        "name": "Stem Cell Derived Exosomes",
        "note": "20 billion exosomes"
      }
    ],
    "total": "£3000"
  }' \
  --output treatment_plan.pdf
```

