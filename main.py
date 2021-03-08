import logging
from json import JSONDecodeError

from models import Contact
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from uvicorn.main import run
from starlette import status

from tortoise.contrib.starlette import register_tortoise

# logging.basicConfig(level=logging.DEBUG)

app = Starlette()


@app.route("/contacts", methods=["GET"])
async def get_contacts(_: Request) -> JSONResponse:
    contacts = await Contact.all()

    res = []
    for contact in contacts:
        res.append({"id": contact.id, "name": contact.name, "phone": contact.phone})

    return JSONResponse(content=res)


@app.route("/contacts", methods=["POST"])
async def create_contact(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
        name = payload["name"]
        phone = payload["phone"]
    except JSONDecodeError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "cannot parse request body"})
    except KeyError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": "name and phone fields are required"})

    if not str(phone).isnumeric():
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": "please make sure number consists of numbers only"})

    contact = await Contact.create(name=name, phone=phone)

    return JSONResponse(content={"id": contact.id, "name": contact.name, "phone": contact.phone},
                        status_code=status.HTTP_201_CREATED)


@app.route("/contacts/{id}", methods=["GET"])
async def get_contact(request):
    contact_id = request.path_params['id']
    contact = await Contact.get_or_none(id=contact_id)

    if contact is None:
        return JSONResponse({
            "error":
                f"No contact found with id = {contact_id}"
        }, status_code=status.HTTP_404_NOT_FOUND)

    return JSONResponse(content={"id": contact.id, "name": contact.name, "phone": contact.phone})


@app.route("/contacts/{id}", methods=["DELETE"])
async def delete_contact(request):
    contact_id = request.path_params['id']
    contact = await Contact.get_or_none(id=contact_id)

    if contact is None:
        return JSONResponse({
            "error":
                f"No contact found with id = {contact_id}"
        }, status_code=status.HTTP_404_NOT_FOUND)

    await contact.delete()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


@app.route("/contacts/{id}", methods=["PATCH", "UPDATE"])
async def update_contact(request):
    contact_id = request.path_params['id']

    try:
        payload = await request.json()
        if not bool(payload):
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "please provide at least one field"})
    except JSONDecodeError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "cannot parse request body"})

    contact = await Contact.get_or_none(id=contact_id)

    if contact is None:
        return JSONResponse({
            "error":
                f"No contact found with id = {contact_id}"
        }, status_code=status.HTTP_404_NOT_FOUND)

    name = payload.get("name")
    phone = payload.get("phone")

    if name is not None:
        contact.name = name
    if phone is not None:
        if not str(phone).isnumeric():
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                content={"error": "please make sure number consists of numbers only"})
        contact.phone = phone

    await contact.save()

    return JSONResponse(content={"id": contact.id, "name": contact.name, "phone": contact.phone},
                        status_code=status.HTTP_200_OK)


register_tortoise(
    app, db_url="sqlite://db.sqlite3", modules={"models": ["models"]}, generate_schemas=True
)

if __name__ == "__main__":
    run(app)
