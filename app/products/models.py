from flask import url_for

from app.models import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime,server_onupdate=db.func.now(), server_default=db.func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship('Category', backref='products', foreign_keys=[category_id])


    @classmethod
    def get_all_objects(cls):
        return cls.query.all()

    def save_product(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def create_product(cls, request_form, image=None):
        prd = cls(**request_form)
        prd.image = image

        db.session.add(prd)
        db.session.commit()
        return prd

    @classmethod
    def get_specific_product(cls, id):
        return  cls.query.get_or_404(id)

    @classmethod
    def edit_product(cls, id, new_data, new_image=None):
        product = cls.query.get(id)
        if not product:
            return None

        if new_image:
            product.image = new_image

        for key, value in new_data.items():
            setattr(product, key, value)

        db.session.commit()
        return product

    @classmethod
    def delete_product(cls, id):
        product = cls.query.get(id)
        db.session.delete(product)
        db.session.commit()

    @property
    def get_image_url(self):
        return url_for('static', filename=f'uploads/projects/{self.image}')

    @property
    def get_show_url(self):
        return  url_for('products.show', id=self.id)
    @property
    def get_update_url(self):
        return  url_for('products.update', id=self.id)
    @property
    def get_delete_url(self):
        return  url_for('products.delete', id=self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'category_id': self.category_id
        }