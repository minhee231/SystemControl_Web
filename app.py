from flask import Flask, request, render_template, jsonify
import json

class Student:
    def __init__(self, name):
        self.name = name
        self.check_status = False

class JsonContorl:
    def __init__(self):
        with open("check_status.json", "r", encoding='utf-8') as file:
            self.json_data = json.load(file)

    def read_student_file(self):
        with open("student_name.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()

        return [line.strip() for line in lines]
    
    def create_student_status_json(self):
        student_info = {}
        count = 1
        student_names = self.read_student_file()

        for student_name in student_names:
            student_obj = Student(student_name)
            student_info[str(count)] = {"name" : student_obj.name, "check_status" : student_obj.check_status}
            count += 1
            #print(student_info)
        return student_info
    
    def save_json(self):
        with open("check_status.json","w",encoding='utf-8') as file:
            file.write(json.dumps(self.json_data, ensure_ascii=False, indent=4))

    def add_assignment(self, title):
        assignment_len = len(self.json_data)
        assignment_number = f"assignment{str(assignment_len+1)}" 
        self.json_data[assignment_number] = {"title" : title, "student_info" : self.create_student_status_json()}

        self.save_json()

    def delete_assignment(self):
        del self.json_data[f"assignment{len(self.json_data)}"]
        self.save_json()

    def update_check_status(self,assignment_number, student_number,status):
    
        self.json_data[assignment_number]["student_info"][student_number]["check_status"] = status
        self.save_json()


app = Flask(__name__)
ctrl_json = JsonContorl()
_password = "adminpassword"

@app.route("/", methods=["GET", "POST"])
def index():
    ctrl_json = JsonContorl()
    return render_template("index.html", json_obj = ctrl_json)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html")


@app.route("/update_status", methods=["POST"])
def update_status():
    ctrl_json = JsonContorl()
    data = request.json
    assignment_id = data["assignment_id"]
    student_id = data["student_id"]
    checked = data["checked"]
    #print(assignment_id,student_id,checked)
    ctrl_json.update_check_status(assignment_id, student_id, checked)
    return jsonify({"success": True})

@app.route("/delete_assignment", methods=["POST"])
def delete_assignment():
    ctrl_json = JsonContorl()
    data = request.json
    password = data.get("password")
    if password != _password:
        print("비번 틀리다....!")
        return
    
    ctrl_json.delete_assignment()
    print("헤헥 과제 삭제 성고오옹")
    return
    
@app.route("/add_assignment", methods=["POST"])
def add_assignment():
    ctrl_json = JsonContorl()
    data = request.json
    title = data.get("title")
    password = data.get("password")

    if password != _password:
        return jsonify({"success": False, "message": "패스워드가 올바르지 않습니다."})

    ctrl_json.add_assignment(title)
    return jsonify({"success": True, "message": "과제가 성공적으로 추가되었습니다."})

if __name__ == "__main__":
    app.run(debug=True)

