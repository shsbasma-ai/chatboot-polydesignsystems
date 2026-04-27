from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = "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"  # 🔴 REMPLACE ICI PAR TA VRAIE CLÉ

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        print("📨 Message reçu:", user_message)
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.3-70b-versatile',  
                'messages': [
                    {
                        'role': 'system',
                        'content': "Tu es l'assistant de Polydesign Systems, entreprise marocaine automobile."
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ]
            },
            timeout=30
        )
        
        print("📡 Status code:", response.status_code)
        print("📄 Réponse brute:", response.text[:300])
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({'reply': reply})
        else:
            return jsonify({'reply': f"Erreur {response.status_code}: {response.text}"}), 500
            
    except Exception as e:
        print("💥 Erreur:", str(e))
        return jsonify({'reply': f"Erreur: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)