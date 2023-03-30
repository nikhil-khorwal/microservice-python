
from api.base import get_db
from api.model import ProductTable
class Events:
  def __init__(self):
    Session = get_db()  
    self.session = Session()

  async def create_order(self,event):
    try:
      product = self.session.query(ProductTable).filter(ProductTable.id==event.value.get("product_id")).one()
      product.stock = product.stock-event.value.get("quantity")
      self.session.commit()
      print("order created")
    except Exception as e:
      print("Error : ",e)