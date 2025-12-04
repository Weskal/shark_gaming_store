from ..models.product import Product

def get_all_products():
    return Product.query.order_by(Product.id.asc()).all()