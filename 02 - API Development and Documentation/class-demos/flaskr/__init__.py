from flask import Flask, abort, jsonify, request
from models import setup_db, Plant
from flask_cors import CORS


# This is a function that will be called automatically when the app run
def create_app(test_config=None):
    app = Flask(__name__)

    setup_db(app)
    CORS(app)

    # @app.after_request
    # def after_request(response):
    # response.headers.add('Access-Control-Allow-Headers',
    #  'Content-Type, Authorization')
    # response.headers.add('Access-Control-Allow-Methods',
    #  'GET, POST, PATCH, DELETE, OPTIONS')

    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to Plants API!'})

    @app.route('/plants', methods=['GET', 'POST'])
    def get_plants():
        if request.method == 'GET':
            # Implement pagination
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * 10
            end = start + 10

            plants = Plant.query.all()
            formatted_plants = [plant.format() for plant in plants]

            return jsonify({
                'success': True,
                'plants': formatted_plants[start:end],
                'length': len(formatted_plants),
            })
        else:
            plant_name = request.form.get('name')
            print(plant_name)

            new_plant = Plant(
                name="Rice Plant",
                scientific_name="Oriza Sertiva",
                is_poisonous=False,
                primary_color="Off white"
            )

            print(request)

            new_plant.insert()

            return jsonify(new_plant.format())

    @app.route('/plants/<int:plant_id>')
    def get_individual_plant(plant_id):
        plant = Plant.query.get(plant_id)

        if (plant is None):
            abort(404)
            # return jsonify({'message': 'Plant not found'})

        return jsonify({
            'success': True,
            'plant': plant.format(),
        })

    return app
