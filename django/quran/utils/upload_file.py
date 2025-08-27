def upload_file(file, company_id, user_id, name, folder):
    from django.conf import settings

    import requests
    import json

    url = settings.REPO_UPLOAD_URL
    headers = {"key": settings.SECRET_KEY}
    form_data = {
        "form_data": json.dumps(
            {
                "company_id": company_id,
                "user_id": user_id,
                "name": name,
                "folder": folder,
            }
        )
    }
    files = {"file": file}
    response = requests.post(url, headers=headers, data=form_data, files=files)
    if response.status_code == 200:
        src = response.json().get("src")
        return src

    return None
