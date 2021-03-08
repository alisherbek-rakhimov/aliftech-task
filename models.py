from tortoise import fields, models


class Contact(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    phone = fields.IntField()

    def __str__(self) -> str:
        return f"Contact {self.name}: {self.phone}"
