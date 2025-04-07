import re
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask import send_file
from io import BytesIO

# --- App Setup ---

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PARIAHistGRAU'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# --- Database Model ---

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sequence_input = db.Column(db.Text, nullable=False)
    results_json = db.Column(db.Text)
    error = db.Column(db.Text)

    def __repr__(self):
        return f"<Analysis(id={self.id}, timestamp='{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}')>"

# --- Core Logic ---

def is_valid_dna(sequence):
    if not sequence:
        return True
    return bool(re.fullmatch(r"[ATCGatcg\s]+", sequence))

def find_pam_sites(sequence):
    if not sequence:
        return [], "Please enter a DNA sequence."
    if not is_valid_dna(sequence):
        return [], "Invalid DNA sequence. Please use only A, T, C, and G characters."

    sequence_cleaned = sequence.upper().replace(" ", "").replace("\n", "")

    if not sequence_cleaned:
        return [], "Please enter a valid DNA sequence (it became empty after removing whitespace)."

    pam_pattern = r"(?=([ATCG]{20}[ATCG]GG))"
    matches = list(re.finditer(pam_pattern, sequence_cleaned))

    results = []
    for i, match in enumerate(matches, 1):
        full_match = match.group(1)
        guide = full_match[:20]
        pam = full_match[20:]
        position = match.start() + 1

        gc_content = 0
        if guide:
            gc_content = (guide.count("G") + guide.count("C")) / len(guide) * 100

        results.append({
            'id': i,
            'position': position,
            'guide': guide,
            'pam': pam,
            'gc_content': f"{gc_content:.1f}"
        })

    return results, None

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    sequence_input = ''
    results = None
    error = None

    if request.method == 'POST':
        sequence_input = request.form.get('sequence', '').strip()
        results, error = find_pam_sites(sequence_input)

        analysis = Analysis(sequence_input=sequence_input, results_json=json.dumps(results) if results else None, error=error)
        db.session.add(analysis)
        db.session.commit()

        session['results'] = results
        session['error'] = error
        return redirect(url_for('index') + '?submitted=true')
        
    if 'results' in session:
        results = session.pop('results')
    if 'error' in session:
        error = session.pop('error')

    return render_template(
        'index.html',
        sequence_input=sequence_input,
        results=results,
        error=error
    )

@app.route('/history')
def history():
    analyses = Analysis.query.order_by(Analysis.timestamp.desc()).all()
    return render_template('history.html', analyses=analyses)

@app.route('/new_session', methods=['POST'])
def new_session():
    clear_history = request.args.get('clear_history') == 'True'
    if clear_history:
        db.session.query(Analysis).delete()
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/export_analysis/<int:analysis_id>')
def export_analysis(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    export_data = {
        'timestamp': analysis.timestamp.isoformat(),
        'input_sequence': analysis.sequence_input,
        'results': json.loads(analysis.results_json) if analysis.results_json else None,
        'error': analysis.error
    }
    filename = f"analysis_{analysis_id}_{analysis.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
    file_like = BytesIO(json.dumps(export_data, indent=4).encode('utf-8'))
    return send_file(
        file_like,
        as_attachment=True,
        download_name=filename,
        mimetype='application/json'
    )

# --- Run App ---

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)