from fastapi import APIRouter,Depends,status
from api.base import get_db
from api.model import ProductTable,product_model
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


products = APIRouter()

@products.get("/")
async def get_all_products(Session = Depends(get_db)):
    session = Session()
    res = session.query(ProductTable).all()
    return res

@products.get("/{product_id}")
async def get_all_products(product_id:int, Session = Depends(get_db)):
    session = Session()
    res = session.query(ProductTable).filter(ProductTable.id == product_id).first()
    
    if(res is None):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message":"product not found"})
    
    return res

@products.post("/")
async def create_product(data:product_model, Session = Depends(get_db)):
    print(data)
    session = Session()
    new_product = ProductTable(
        title=data.title,
        desc= data.desc,
        price=data.price,
        discount_percentage=data.discount_percentage,
        gst_percentage=data.gst_percentage,
        stock=data.stock)
    session.add(new_product)
    session.commit()

    return JSONResponse(content={"message":"product add sucessfully"}, status_code=status.HTTP_201_CREATED)