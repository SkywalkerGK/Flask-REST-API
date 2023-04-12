#ทำงานฝั่ง Server เวลาที่ Cilent ส่งคำขอมา จะส่งข้อมูลที่อยู่ใน app.py ตอบกลับไปในรูปแบบ JSON  POST !!!
from flask import Flask #1.สร้าง flask
from flask_restful import Api,Resource,abort,reqparse #2.สร้าง api 3.สร้าง resource
from flask_sqlalchemy import SQLAlchemy,Model

app=Flask(__name__)

#database
db=SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db" #สร้างไฟล์ database.db
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
city_add_args=reqparse.RequestParser()
city_add_args.add_argument("name",type=str,required=True,help="กรุณาป้อนชื่อจังหวัดเป็นข้อความ")
city_add_args.add_argument("temp",type=str,required=True,help="กรุณาป้อนอุณหภูมิเป็นข้อความ")
city_add_args.add_argument("weather",type=str,required=True,help="กรุณาป้อนสภาพอากาศเป็นข้อความ")
city_add_args.add_argument("people",type=str,required=True,help="กรุณาป้อนจำนวนประชากรเป็นข้อความ")

mycity={
    "chonburi":{"name":"ชลบุรี","weather":"อากาศร้อนอบอ้าว","people":1500},
    "rayong":{"name":"ระยอง","weather":"ฝนตก","people":2000},
    "bangkok":{"name":"กรุงเทพ","weather":"หนาว","people":5000},
}

#validate request
"""
def notFoundCity(city_id):
    if city_id not in mycity:
        abort(404,message = "ไม่พบข้อมูลที่คุณร้องขอ")
"""
def notFoundNameCity(name):
    if name not in mycity:
        abort(404,message = "ไม่พบข้อมูลที่คุณร้องขอ")        


#ออกแบบ Resorce
class WeatherCity(Resource):
    def get(self,name): #HTTP Method
        notFoundNameCity(name)
        return mycity[name]  #{"key":"value"}

    def post(self,name):
        args=city_add_args.parse_args()
        return args   

#call เรียก Resorce ผ่าน api ทำให้ api มีก้อนข้อมูล
api.add_resource(WeatherCity,"/weather/<string:name>") #เส้นทางในการเข้าถึง Resourse

if __name__ == "__main__":
    app.run(debug=True)
