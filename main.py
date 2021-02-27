from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
import requests

app =  Flask(__name__)
api =  Api(app=app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  True
db =  SQLAlchemy(app)

""" REUEST TO API TO RETRIEVE ALL SPACE SHIPS and save them in ships list"""
request =  requests.get(url = "https://swapi.dev/api/starships/").json()["results"]
sorted_by_hyperdrive =  [ship for ship in sorted(request, key =  lambda x:x["hyperdrive_rating"], reverse=False)]
ships = [{"name": ship["name"], "rating": float(ship["hyperdrive_rating"])} for ship in sorted_by_hyperdrive]

""" Database Model of Spaceship Creation """
class Starship(db.Model):
    id =  db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(100), unique =  True, nullable =  False, )
    rating =  db.Column(db.Float, unique = False, nullable =  False)

    def __repr__(self):
        """ Representation of the Model"""
        return f"Ship Name: {self.name} Hyperdrive Rating: {self.rating} "



resource_fields = {
    "id" : fields.String,
    "name":  fields.String,
    "rating":  fields.String
}

""" Below are the methods of fetching, creating , updating and  deleting the records of DATABASE through API"""
class Application(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result =  Starship.query.filter_by(id= id).first()
        if result:
            return result, 200
        else:
            abort(404, message = "Not Found Any Starship with that id :(")



    @marshal_with(resource_fields)
    def put(self, id):
        put_args = reqparse.RequestParser()
        put_args.add_argument("name", help="Name is required", required=True, type=str)
        put_args.add_argument("rating", help="Rating is required", required=True, type=float)
        args =  put_args.parse_args()
        result = Starship.query.filter_by(id =  id).first()
        if result:
            abort(409, message="Starship already exists with that id")
        ship =  Starship(id =  id, name =  args["name"], rating =  args["rating"])
        db.session.add(ship)
        db.session.commit()
        return ship[id], 201

    def patch(self, id):
        patch_args = reqparse.RequestParser()
        patch_args.add_argument("name", help="Name is required",  type=str)
        patch_args.add_argument("rating", help="Rating is required",  type=float)
        result = Starship.query.filter_by(id =  id).first()
        args =  patch_args.parse_args()
        if not result:
            abort(404, message="Does not exist ship with that id")
        else:
            if args["name"]:
                Starship.name =  args["name"]
            if args["rating"]:
                Starship.rating =  args["rating"]
            db.session.commit()
            return {"Message" :  "Updated", "id" :  id, "name" :  args["name"], "rating":  args["rating"]}

    def delete(self, id):
        result =  Starship.query.filter_by(id =  id).first_or_404()
        db.session.delete(result)
        db.session.commit()
        return {
            "message" : "Data has been successfully deleted"
        }





api.add_resource(Application, "/ships/<int:id>")
if __name__ == '__main__':
    app.run(debug =  True)
