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
            # Payment note (optional)
            if data.get("payment_note"):
                self.set_font("Arial", "I", 9)
                self.set_text_color(80)
                self.cell(0, 6, data["payment_note"], ln=True, align="R")
                self.set_text_color(0)

        # Medical Consultant (optional)
        if data.get("consultant_name"):
            self.set_font("Arial", "B", 10)
            self.cell(0, 6, "Your Medical Consultant:", ln=True, align="R")
            self.set_font("Arial", "", 10)
            self.cell(0, 6, data["consultant_name"], ln=True, align="R")

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
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Treatment Plan PDF Generator</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 2em;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 600;
            }
            input[type="text"], textarea {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            .treatment-item {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 15px;
                border: 1px solid #e0e0e0;
            }
            .treatment-item h3 {
                font-size: 14px;
                color: #666;
                margin-bottom: 10px;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                width: 100%;
                margin-top: 10px;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            button:active {
                transform: translateY(0);
            }
            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .btn-add {
                background: #28a745;
                margin-top: 0;
                margin-bottom: 15px;
            }
            .btn-remove {
                background: #dc3545;
                padding: 8px 16px;
                font-size: 14px;
                width: auto;
                margin-top: 10px;
            }
            .message {
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                display: none;
            }
            .message.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .message.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 Treatment Plan PDF Generator</h1>
            <p class="subtitle">Generate professional treatment plan PDFs</p>
            
            <div id="message" class="message"></div>
            
            <form id="pdfForm">
                <div class="form-group">
                    <label for="title">Title</label>
                    <input type="text" id="title" name="title" value="Treatment Plan" required>
                </div>
                
                <div class="form-group">
                    <label for="billed_to">Billed To</label>
                    <input type="text" id="billed_to" name="billed_to" placeholder="Enter patient name" required>
                </div>
                
                <div class="form-group">
                    <label>Treatments</label>
                    <div id="treatments">
                        <div class="treatment-item">
                            <h3>Treatment 1</h3>
                            <input type="text" class="treatment-name" placeholder="Treatment name" required>
                            <input type="text" class="treatment-note" placeholder="Note (optional)" style="margin-top: 10px;">
                        </div>
                    </div>
                    <button type="button" class="btn-add" onclick="addTreatment()">+ Add Treatment</button>
                </div>
                
                <div class="form-group">
                    <label for="total">Total Price</label>
                    <input type="text" id="total" name="total" placeholder="e.g., £3000">
                </div>
                
                <div class="form-group">
                    <label for="payment_note">Payment Note (Optional)</label>
                    <input type="text" id="payment_note" name="payment_note" placeholder="e.g., Payment is done in cash">
                </div>
                
                <div class="form-group">
                    <label for="consultant_name">Medical Consultant Name (Optional)</label>
                    <input type="text" id="consultant_name" name="consultant_name" placeholder="e.g., Yunus">
                </div>
                
                <button type="submit" id="generateBtn">Generate PDF</button>
            </form>
        </div>
        
        <script>
            function addTreatment() {
                const container = document.getElementById('treatments');
                const count = container.children.length + 1;
                const div = document.createElement('div');
                div.className = 'treatment-item';
                div.innerHTML = `
                    <h3>Treatment ${count}</h3>
                    <input type="text" class="treatment-name" placeholder="Treatment name" required>
                    <input type="text" class="treatment-note" placeholder="Note (optional)" style="margin-top: 10px;">
                    <button type="button" class="btn-remove" onclick="removeTreatment(this)">Remove</button>
                `;
                container.appendChild(div);
            }
            
            function removeTreatment(btn) {
                if (document.getElementById('treatments').children.length > 1) {
                    btn.parentElement.remove();
                } else {
                    showMessage('At least one treatment is required', 'error');
                }
            }
            
            function showMessage(text, type) {
                const msg = document.getElementById('message');
                msg.textContent = text;
                msg.className = 'message ' + type;
                msg.style.display = 'block';
                setTimeout(() => {
                    msg.style.display = 'none';
                }, 5000);
            }
            
            document.getElementById('pdfForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const btn = document.getElementById('generateBtn');
                btn.disabled = true;
                btn.textContent = 'Generating...';
                
                // Collect form data
                const treatments = [];
                document.querySelectorAll('.treatment-item').forEach(item => {
                    const name = item.querySelector('.treatment-name').value;
                    const note = item.querySelector('.treatment-note').value;
                    if (name) {
                        treatments.push({
                            name: name,
                            note: note || undefined
                        });
                    }
                });
                
                const data = {
                    title: document.getElementById('title').value,
                    billed_to: document.getElementById('billed_to').value,
                    treatments: treatments,
                    total: document.getElementById('total').value || undefined,
                    payment_note: document.getElementById('payment_note').value || undefined,
                    consultant_name: document.getElementById('consultant_name').value || undefined
                };
                
                try {
                    const response = await fetch('/api/generate-pdf', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `treatment_plan_${data.billed_to.replace(' ', '_')}.pdf`;
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        document.body.removeChild(a);
                        showMessage('PDF generated successfully!', 'success');
                    } else {
                        const error = await response.json();
                        showMessage('Error: ' + (error.error || 'Failed to generate PDF'), 'error');
                    }
                } catch (error) {
                    showMessage('Error: ' + error.message, 'error');
                } finally {
                    btn.disabled = false;
                    btn.textContent = 'Generate PDF';
                }
            });
        </script>
    </body>
    </html>
    """
    return html

# For Vercel: Export the Flask app as the handler
# Vercel's @vercel/python will automatically wrap this as a serverless function
if __name__ == "__main__":
    app.run(debug=True)

