#ทำงานฝั่ง Server เวลาที่ Cilent ส่งคำขอมา จะส่งข้อมูลที่อยู่ใน app.py ตอบกลับไปในรูปแบบ JSON  POST !!!
from flask import Flask #1.สร้าง flask
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields #2.สร้าง api 3.สร้าง resource
from flask_sqlalchemy import SQLAlchemy,Model

app=Flask(__name__)

#database
db=SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
api=Api(app)


class CityModel(db.Model):   #ดึงคุณสมบัติจากตัวแปร db เวลาสร้างโมเดลขึ้นมาจะจัดเก็บใน database.db
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    temp=db.Column(db.String(100),nullable=False)
    weather=db.Column(db.String(100),nullable=False)
    people=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"City(name={name},temp={temp},weather={weather},people={people})"

db.create_all()  

#Request Parser
#การเพิ่มข้อมูล
city_add_args=reqparse.RequestParser() 
city_add_args.add_argument("name",type=str,required=True,help="กรุณาป้อนชื่อจังหวัด")
city_add_args.add_argument("temp",type=str,required=True,help="กรุณาป้อนอุณหภูมิ")
city_add_args.add_argument("weather",type=str,required=True,help="กรุณาป้อนสภาพอากาศ")
city_add_args.add_argument("people",type=str,required=True,help="กรุณาป้อนจำนวนประชากร")

#การอัพเดตข้อมูล
city_update_args=reqparse.RequestParser()
city_update_args.add_argument("name",type=str,help="กรุณาป้อนชื่อจังหวัดที่ต้องการแก้ไข")
city_update_args.add_argument("temp",type=str,help="กรุณาป้อนอุณหภูมิที่ต้องการแก้ไข")
city_update_args.add_argument("weather",type=str,help="กรุณาป้อนสภาพอากาศที่ต้องการแก้ไข")
city_update_args.add_argument("people",type=str,help="กรุณาป้อนจำนวนประชากรที่ต้องการแก้ไข")

#ระบุ / นิยาม resource_field
resource_field={ 
    "id":fields.Integer,
    "name":fields.String,
    "temp":fields.String,
    "weather":fields.String,
    "people":fields.String
}

#ออกแบบ Resorce
class WeatherCity(Resource):

    @marshal_with(resource_field)
    def get(self,city_id): #HTTP Method
        result=CityModel.query.filter_by(id = city_id).first() #ค้นหาข้อมูลผ่าน CityModel จาก cityID ค่าที่ส่งเข้ามาทำงาน
        if not result: #validate request
            abort(404,message = "ไม่พบข้อมูลที่คุณร้องขอ")
        return result

    @marshal_with(resource_field)
    def post(self,city_id):
        result=CityModel.query.filter_by(id = city_id).first()
        if result:
            abort(409,message="รหัสจังหวัดนี้เคยบันทึกไปแล้ว ลองเปลี่ยนหมายเลขดูนะครับ")
        args=city_add_args.parse_args()
        city=CityModel(id=city_id,name=args["name"],temp=args["temp"],weather=args["weather"],people=args["people"]) #จับคู่ Data ให้เข้ากับคอลัม
        db.session.add(city)
        db.session.commit()
        return city,201  

    @marshal_with(resource_field)
    def patch(self,city_id): #ค้นข้อมูลจังหวัดเก่าก่อน ถ้าไม่เจอ
        args=city_update_args.parse_args()
        result=CityModel.query.filter_by(id = city_id).first()
        if not result:
            abort(409,message="ไม่พบข้อมูลจังหวัดที่จะแก้ไข")
        if args["name"]:
            result.name=args["name"]  #result.name = chonburi => args["name"] = ชลบุรี  
        if args["temp"]:
            result.temp=args["temp"]
        if args["weather"]:
            result.weather=args["weather"]        
        if args["people"]:
            result.people=args["people"]        
        db.session.commit()
        return result        


#call เรียก Resorce ผ่าน api ทำให้ api มีก้อนข้อมูล
api.add_resource(WeatherCity,"/weather/<int:city_id>") #เส้นทางในการเข้าถึง Resourse

if __name__ == "__main__":
    app.run(debug=True)
