from flask import Flask, request, jsonify, send_file
from fpdf import FPDF
import os
import io
from datetime import datetime

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        # Try to load template image, if not found, continue without it
        template_path = os.path.join(os.path.dirname(__file__), "..", "template_clean.jpg")
        if os.path.exists(template_path):
            self.image(template_path, x=0, y=0, w=210, h=297)

    def add_content(self, data):
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 51, 102)
        self.set_y(50)
        self.cell(0, 10, data["title"], ln=True, align="C")

        self.set_font("Arial", "B", 11)
        self.multi_cell(0, 6, f"Tailored for:\n")

        self.set_font("Arial", "", 11)
        self.multi_cell(0, 6, data['billed_to'])

        self.set_y(95)
        self.set_font("Arial", "B", 12)
        self.set_fill_color(225, 236, 247)
        self.set_text_color(0, 51, 102)
        self.cell(180, 9, "Included Therapies", 1, 1, "C", True)

        self.set_font("Arial", "", 11)
        self.set_text_color(0)
        for i, item in enumerate(data["treatments"], 1):
            # Ana satır (kutulu)
            self.cell(180, 8, f"{i}. {item['name']}", border=1, ln=1)
            # Eğer not varsa, alt satıra italik ve gri olarak yaz (kutusuz)
            if "note" in item and item["note"]:
                self.set_font("Arial", "I", 10)
                self.set_text_color(100)
                self.cell(180, 6, f"   {item['note']}", border=0, ln=1)
                self.set_font("Arial", "", 11)
                self.set_text_color(0)

        if data.get("total"):
            self.set_y(self.get_y() + 10)
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, f"Total Package Price: {data['total']}", ln=True, align="R")
            self.set_font("Arial", "I", 9)
            self.set_text_color(80)
            self.cell(0, 6, "Payment is done in cash", ln=True, align="R")
            self.set_text_color(0)

        self.set_font("Arial", "B", 10)
        self.cell(0, 6, "Your Medical Consultant:", ln=True, align="R")
        self.set_font("Arial", "", 10)
        self.cell(0, 6, "Yunus", ln=True, align="R")

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        required_fields = ["title", "billed_to", "treatments"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create PDF
        pdf = PDF()
        pdf.add_page()
        pdf.add_content(data)
        
        # Generate filename
        name = data["billed_to"].split("\n")[0].replace(" ", "_")
        file_name = f"treatment_plan_{name}.pdf"
        
        # Save to memory buffer
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=file_name
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Treatment Plan PDF Generator API",
        "endpoints": {
            "POST /api/generate-pdf": "Generate PDF from JSON data",
            "GET /api/health": "Health check"
        }
    }), 200

# For Vercel: Export the Flask app as the handler
# Vercel's @vercel/python will automatically wrap this as a serverless function
if __name__ == "__main__":
    app.run(debug=True)

