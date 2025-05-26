from flask import Flask, flash, url_for, redirect, render_template, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages
DATA_FILE = "feedback.json"

# Ensure feedback file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        new_feedback = {
            "name": name,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        with open(DATA_FILE, "r+") as f:
            feedbacks = json.load(f)
            feedbacks.append(new_feedback)  
            f.seek(0)
            f.truncate()
            json.dump(feedbacks, f, indent=4)

        flash("Thank you for your feedback!")
        return redirect(url_for('home'))

    # GET
    with open(DATA_FILE, "r") as f:
        feedbacks = json.load(f)
    avg_rating = round(sum(int(fb['rating']) for fb in feedbacks) / len(feedbacks), 2) if feedbacks else 0
    return render_template("index.html", feedbacks=feedbacks, avg_rating=avg_rating)

@app.route('/update', methods=['PUT'])
def update_feedback():
    data = request.json
    name_to_update = data.get("name")
    new_comment = data.get("comment")
    new_rating = data.get("rating")

    with open(DATA_FILE, "r+") as f:
        feedbacks = json.load(f)
        for fb in feedbacks:
            if fb["name"].lower() == name_to_update.lower():
                if new_comment:
                    fb["comment"] = new_comment
                if new_rating:
                    fb["rating"] = new_rating
                fb["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                break
        f.seek(0)
        f.truncate()
        json.dump(feedbacks, f, indent=4)

    return jsonify({"message": "Feedback updated"})

@app.route('/delete', methods=['DELETE'])
def delete_feedback():
    data = request.json
    name_to_delete = data.get("name")

    with open(DATA_FILE, "r+") as f:
        feedbacks = json.load(f)
        feedbacks = [fb for fb in feedbacks if fb["name"].lower() != name_to_delete.lower()]
        f.seek(0)
        f.truncate()
        json.dump(feedbacks, f, indent=4)

    return jsonify({"message": "Feedback deleted"})

@app.route('/health', methods=['HEAD'])
def health_check():
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
