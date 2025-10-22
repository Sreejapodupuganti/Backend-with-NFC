from flask import Blueprint, request, jsonify
from app.utils.google_wallet import create_generic_object, create_generic_class, generate_save_url

wallet_bp = Blueprint("wallet", __name__)

@wallet_bp.route("/pass", methods=["POST"])
def create_wallet_pass():
    data = request.json
    handle = data.get("handle", "johndoe")
    title = data.get("title", "John Doe")
    designation = data.get("designation", "Software Engineer")
    company = data.get("company", "DigiCorp")
    link = f"{data.get('link', 'https://google.com/')}"

    # Create Wallet Object
    obj = create_generic_object(handle, title, designation, company, link)

    object_id = obj.get("id")

    if not object_id:
        return jsonify({"error": "Failed to create object", "details": obj}), 400

    # Generate Save-to-Wallet URL
    save_url = generate_save_url(object_id)

    return jsonify({
        "save_url": save_url,
        "object": obj
    })