from flask import Flask, jsonify, request, render_template

from models.task_list import TaskList

app = Flask(__name__)
task_list = TaskList()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state")
def get_state():
    return jsonify(task_list.state())


@app.route("/api/add", methods=["POST"])
def add_task():
    data = request.get_json(force=True)
    title = data.get("title", "Untitled task").strip() or "Untitled task"
    priority = data.get("priority", "medium")
    task_list.add_task(title, priority)
    return jsonify(task_list.state())


@app.route("/api/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    task_list.toggle_task(task_id)
    return jsonify(task_list.state())


@app.route("/api/remove/<int:task_id>", methods=["POST"])
def remove_task(task_id):
    task_list.remove_task(task_id)
    return jsonify(task_list.state())


@app.route("/api/move_to/<int:task_id>/<int:target_index>", methods=["POST"])
def move_task(task_id, target_index):
    task_list.move_task_to(task_id, target_index)
    return jsonify(task_list.state())


@app.route("/api/clear_completed", methods=["POST"])
def clear_completed():
    task_list.clear_completed()
    return jsonify(task_list.state())


@app.route("/api/traverse")
def traverse():
    return jsonify({"order": task_list.traversal_order()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
