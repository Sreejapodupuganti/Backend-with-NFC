@wallet_bp.route("/pass", methods=["POST"])
def create_wallet_pass():
    data = request.json
    username = data.get("username", "John Doe")
    email = data.get("email", "johndoe@example.com")
    company = data.get("company", "DigiCorp")
    job_title = data.get("job_title", "Software Engineer")

    # Create Wallet Object
    status, obj = create_data_object(username, email, company, job_title)
    if status != 200:
        return {"error": "Failed to create object", "details": obj}, 400

    # Generate Save-to-Wallet URL
    save_url = generate_save_link(username, email, company, job_title)

    return {"save_url": save_url, "object": obj}
