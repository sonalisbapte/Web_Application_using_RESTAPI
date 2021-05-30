import sqlite3
from flask_restful import Resource, reqparse 
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help='This field can not be left blank !')
       
        
    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'},404

    def post(self,name):
        if ItemModel.find_by_name(name):
           return {'message': 'An item with name {} already exists.'.format(name)} ,400
        
        data= Item.parser.parse_args()

        #data=request.get_json()  # silent=True, force = True two parameters ehich we can set to avoid the error of jso
        item= ItemModel(name,data['price']) 

        try:
            item.insert()
        except:
            return {'message':'An error accured'},500 # internal server error
        #items.append(item)
        connection=sqlite3.connect('data.db')
        return item.json(),201


    
    def delete(self,name):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="DELETE FROM items WHERE name=?"
        result=cursor.execute(query,(name,))
        connection.commit()
        connection.close()
        return {'Message': "Item Deleted..!!"}

    def put(self,name):
        data= Item.parser.parse_args()
        item=ItemModel.find_by_name(name)
        updated_item=ItemModel(name,data['price']) 
        if item is None:
            try:
                updated_item.insert()
            except:
                return {'Message':"AN error occured inserting item "},500
        else:
            try:
                updated_item.update() # now item is a dict which has an inbuuild update method # taking entire json pyload
            except:
                return {'Message':"AN error occured updation item"},500
        return updated_item.json() 
 # only sum of the elements can be passed in through the json payload using reqparse
    

class ItemList(Resource):
    def get(self):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="SELECT * FROM items"
        result=cursor.execute(query)
        items=[]
        for row in result:
            items.append({'name':row[0],'price':row[1]})
        connection.close()
        return {'items':items}
    
