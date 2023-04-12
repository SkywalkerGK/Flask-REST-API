#ทำงานฝั่ง Server เวลาที่ Cilent ส่งคำขอมา จะส่งข้อมูลที่อยู่ใน app.py ตอบกลับไปในรูปแบบ JSON
from flask import Flask #1.สร้าง flask
from flask_restful import Api,Resource,abort #2.สร้าง api 3.สร้าง resource

app=Flask(__name__)
api=Api(app)

mycity={
    1:{"name":"ชลบุรี","weather":"อากาศร้อนอบอ้าว","people":1500},
    2:{"name":"ระยอง","weather":"ฝนตก","people":2000},
    3:{"name":"กรุงเทพ","weather":"หนาว","people":5000},
}

#validate request
def notFoundCity(city_id):
    if city_id not in mycity:
        abort(404,message = "ไม่พบข้อมูลที่คุณร้องขอ")

#ออกแบบ Resorce
class WeatherCity(Resource):
    def get(self,city_id): #HTTP Method
        notFoundCity(city_id)
        return mycity[city_id]  #{"key":"value"}
    def post(self,name):
        return{"data":"Creat Resource"+name}    

#call เรียก Resorce ผ่าน api ทำให้ api มีก้อนข้อมูล
api.add_resource(WeatherCity,"/weather/<int:city_id>") #เส้นทางในการเข้าถึง Resourse

if __name__ == "__main__":
    app.run(debug=True)
