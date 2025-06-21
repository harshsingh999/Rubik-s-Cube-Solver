from flask import Flask, request, jsonify
from flask_cors import CORS
import kociemba

app = Flask(__name__)
CORS(app)

COLOR_TO_FACE = {
    "#FFFFFF": "U", "#FFD500": "D", "#B90000": "F",
    "#FF5900": "B", "#0045AD": "L", "#009B48": "R"
}

@app.route('/solve', methods=['POST'])
def solve_cube():
    data = request.json
    if not data or 'cube_state' not in data:
        return jsonify({"error": "Missing cube_state in request"}), 400

    try:
        cube_state = data['cube_state']
        facelet_str = ""

        for face in ['top', 'right', 'front', 'bottom', 'left', 'back']:
            stickers = cube_state.get(face, [])
            if len(stickers) != 9:
                return jsonify({"error": f"Face {face} must have 9 stickers"}), 400
            for color in stickers:
                facelet = COLOR_TO_FACE.get(color)
                if not facelet:
                    return jsonify({"error": f"Invalid color {color} on face {face}"}), 400
                facelet_str += facelet

        if len(facelet_str) != 54:
            return jsonify({"error": "Cube string must be 54 characters"}), 400

        solution = kociemba.solve(facelet_str)
        return jsonify({"solution": solution})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)
