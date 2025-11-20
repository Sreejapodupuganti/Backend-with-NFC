from flask import Blueprint, request, jsonify
from app.utils.google_wallet import create_data_object, create_data_class, generate_save_link

wallet_bp = Blueprint("wallet", __name__)

@wallet_bp.route("/pass", methods=["POST"])
def create_wallet_pass():
    data = request.json
    username = data.get("username", "John Doe")
    email = data.get("email", "johndoe@example.com")
    company = data.get("company", "DigiCorp")
    job_title = data.get("job_title", "Software Engineer")

    # Ensure data class exists (run once; 409 = Already exists)
    status, cls = create_data_class()
    if status not in (200, 409):
        return jsonify({"error": "Failed to create class", "details": cls}), 400

    # Create Wallet Object
    status, obj = create_data_object(username, email, company, job_title)
    if status != 200:
        return jsonify({"error": "Failed to create object", "details": obj}), 400

    # Generate Save-to-Wallet URL
    save_url = generate_save_link(username, email, company, job_title)

    return jsonify({"save_url": save_url, "object": obj})
