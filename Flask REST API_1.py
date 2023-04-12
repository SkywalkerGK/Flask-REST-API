#ทำงานฝั่ง Server เวลาที่ Cilent ส่งคำขอมา จะส่งข้อมูลที่อยู่ใน app.py ตอบกลับไปในรูปแบบ JSON
from flask import Flask #1.สร้าง flask
from flask_restful import Api,Resource #2.สร้าง api 3.สร้าง resource

app=Flask(__name__)
api=Api(app)

#ออกแบบ Resorce
class WeatherCity(Resource):
    def get(self,name): #HTTP Method
        return {"data":"Select : " + name}  #{"key":"value"}
    def post(self,name):
        return{"data":"Creat Resource"+name}    

#call เรียก Resorce ผ่าน api ทำให้ api มีก้อนข้อมูล
api.add_resource(WeatherCity,"/weather/<string:name>") #เส้นทางในการเข้าถึง Resourse

if __name__ == "__main__":
    app.run(debug=True)
