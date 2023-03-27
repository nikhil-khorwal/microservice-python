
from api.base import get_db
from api.model import ProductTable
class Events:

  @staticmethod
  async def create_order(event):
    try:
      print(event.value)
      Session = get_db()
      session = Session()
      product = session.query(ProductTable).filter(ProductTable.id==event.value.get("product_id")).one()
      product.stock = product.stock-event.value.get("quantity")
      session.commit()
      print("order created")
    except Exception as e:
      print("Error : ",e)