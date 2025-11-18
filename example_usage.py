"""
Example script to test the PDF generation API locally or remotely
"""
import requests
import json

# For local testing, use: http://localhost:5000
# For Vercel deployment, use: https://your-app.vercel.app
API_URL = "http://localhost:5000/api/generate-pdf"

# Example data
data = {
    "title": "Treatment Plan",
    "billed_to": "Amir_",
    "treatments": [
        {
            "name": "Stem Cell Derived Exosomes",
            "note": "20 billion exosomes"
        },
    ],
    "total": "£3000"
}

def test_api():
    """Test the PDF generation API"""
    try:
        response = requests.post(
            API_URL,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # Save the PDF
            filename = f"treatment_plan_{data['billed_to'].replace(' ', '_')}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ PDF created successfully: {filename}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running.")
        print("   Run: python api/index.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()

