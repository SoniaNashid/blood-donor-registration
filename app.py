from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import datetime

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://def274753:AYjwoqKnriIE33Ea@cluster0.birbk7x.mongodb.net/bs1001?retryWrites=true&w=majority"
mongo = PyMongo(app)
donors_collection = mongo.db.donors

def days_since(date_str):
    if not date_str:
        return 9999
    last_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return (datetime.datetime.now() - last_date).days

def blood_compatibility(recipient, donor):
    compatible = {
        "A+": ["A+", "A-", "O+", "O-"],
        "A-": ["A-", "O-"],
        "B+": ["B+", "B-", "O+", "O-"],
        "B-": ["B-", "O-"],
        "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        "AB-": ["A-", "B-", "AB-", "O-"],
        "O+": ["O+", "O-"],
        "O-": ["O-"]
    }
    return donor in compatible.get(recipient, [])

def calculate_score(donor, req_blood, req_zip):
    score = 100
    if donor["blood_group"] == req_blood:
        score += 50
    if donor.get("zip") == req_zip:
        score += 30

    if donor.get("zip", "").startswith("208"):  # Maryland
        score += 40
    elif donor.get("zip", "").startswith("111"):  # New York
        score += 10

    if days_since(donor.get("last_donation", "")) >= 56:
        score += 20
    return score

@app.route("/")
def home():
    return jsonify({"msg": "Welcome to the Blood Donor API"})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    required_fields = ["name", "email", "phone", "blood_group", "zip", "last_donation"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    donor = {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "blood_group": data["blood_group"],
        "zip": data["zip"],
        "last_donation": data["last_donation"]
    }
    donors_collection.insert_one(donor)
    return jsonify({"msg": "Donor registered successfully"}), 201

@app.route("/search-donors", methods=["GET"])
def search_donors():
    blood_needed = request.args.get("blood")
    zip_needed = request.args.get("zip")
    results = []

    for donor in donors_collection.find():
        if not blood_compatibility(blood_needed, donor["blood_group"]):
            continue
        if days_since(donor.get("last_donation", "")) < 56:
            continue
        donor["score"] = calculate_score(donor, blood_needed, zip_needed)
        donor["_id"] = str(donor["_id"])
        results.append(donor)

    results.sort(key=lambda x: x["score"], reverse=True)
    return jsonify({"matches": results})

@app.route("/delete/<id>", methods=["DELETE"])
def delete_donor(id):
    result = donors_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({"msg": "Donor deleted"}), 200
    else:
        return jsonify({"error": "Donor not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)

