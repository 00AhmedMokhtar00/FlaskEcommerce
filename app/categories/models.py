from flask import url_for

from app.models import db

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def get_all_objects(cls):
        return cls.query.all()

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create_category(cls, request_form):
        cat = cls(**request_form)

        db.session.add(cat)
        db.session.commit()
        return cat

    @classmethod
    def get_specific_category(cls, id):
        return  cls.query.get_or_404(id)

    @classmethod
    def edit_category(cls, id, new_data):
        category = cls.query.get(id)

        for key, value in new_data.items():
            setattr(category, key, value)
        db.session.commit()
        return category

    @classmethod
    def delete_category(cls, id):
        category = cls.query.get(id)
        db.session.delete(category)
        db.session.commit()

    @property
    def get_show_url(self):
        return  url_for('categories.show', id=self.id)
    @property
    def get_update_url(self):
        return  url_for('categories.update', id=self.id)
    @property
    def get_delete_url(self):
        return  url_for('categories.delete', id=self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }