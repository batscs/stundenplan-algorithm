from flask_restx import fields

def __register_input_models(api):
    metadata_model = api.model('InputMetadata', {
        'days': fields.Integer(required=True, description='Number of days'),
        'timeslots': fields.Integer(required=True, description='Number of timeslots per day')
    })

    # Room model
    room_model = api.model('InputRoom', {
        'name': fields.String(required=True, description='Name of the room'),
        'capacity': fields.Integer(required=True, description='Capacity of the room'),
        'room_type': fields.String(required=True, description='Type of the room')
    })

    # Event model
    event_model = api.model('InputEvent', {
        'name': fields.String(required=True, description='Name of the event'),
        'employees': fields.List(fields.String, required=True, description='List of employees assigned to the event'),
        'participants': fields.List(fields.String, description='List of participants (optional)'),
        'size': fields.Integer(required=True, description='Number of participants in the event'),
        'weekly_blocks': fields.Integer(required=True, description='Number of weekly blocks required for the event'),
        'room_type': fields.String(required=True, description='Type of room required for the event')
    })

    constraints = fields.Raw(required=True, description="List of Constraint data")

    # Schedule input model
    stundenplan_input = api.model('Datenbasis', {
        'metadata': fields.Nested(metadata_model, required=True, description='Metadata for the schedule'),
        'rooms': fields.List(fields.Nested(room_model), required=True, description='List of rooms available'),
        'events': fields.List(fields.Nested(event_model), required=True, description='List of events to schedule'),
        'constraints': fields.Nested(api.model('InputConstraints', {
            'hard': constraints,
            'soft': constraints
        }), required=True, description='Constraints for the schedule')
    })

    return stundenplan_input

def __register_output_models(api):
    # Participants Model
    participant_model = api.model('Participant', {
        'program': fields.String(required=True, description='The program code (e.g., B_CGT)'),
        'semester': fields.Integer(required=True, description='The semester number (e.g., 4)'),
    })

    # Event Model
    event_model = api.model('Event', {
        'day': fields.Integer(required=True, description='Day of the week (e.g., 4 for Thursday)'),
        'timeslot': fields.Integer(required=True, description='Timeslot number'),
        'event': fields.String(required=True, description='Event name'),
        'room': fields.String(required=True, description='Room name or code'),
        'participants': fields.List(fields.String, required=True, description='List of participants in the event'),
    })

    constraints = fields.Raw(required=True, description="List of Constraint data")


    # Core Constraints Model
    core_constraints_model = api.model('CoreConstraints', {
        'fitness': fields.Integer(required=True, description='Fitness score for core constraints'),
        'unsatisfied': constraints,
        'satisfied': constraints,
    })

    # Constraints Model
    constraints_model = api.model('Constraints', {
        'core': fields.Nested(core_constraints_model),
        'hard': fields.Nested(api.model('HardConstraints', {
            'fitness': fields.Integer(required=True, description='Fitness score for hard constraints'),
            'unsatisfied': constraints,
            'satisfied': constraints
        })),
        'soft': fields.Nested(api.model('SoftConstraints', {
            'fitness': fields.Integer(required=True, description='Fitness score for soft constraints'),
            'unsatisfied': constraints,
            'satisfied': constraints
        })),
    })

    # Timetable Model
    stundenplan_output = api.model('Stundenplan', {
        'timetable': fields.List(fields.Nested(event_model), required=True, description='List of scheduled events'),
        'metadata': fields.Nested(api.model('Metadata', {
            'fitness': fields.Integer(required=True, description='Overall fitness score for the timetable'),
        })),
        'constraints': fields.Nested(constraints_model, required=True,
                                     description='Constraints data for the timetable'),
    })

    full_stundenplan_output = api.model('Stundenplan_Output', {
        "data": fields.Nested(stundenplan_output),
        "timestamp": fields.String(description='Timestamp ISO8601'),
        "status": fields.String(description='Status Message'),
    })

    return full_stundenplan_output

def register_models(api):
    config_model = api.model('Config', {
        'algorithm': fields.Nested(api.model('ConfigAlgorithm', {
            'generations_max': fields.Integer(required=True, description='Number of generations for the algorithm')
        })),
        'application': fields.Nested(api.model('ConfigApp', {
            'filepath_input': fields.String(required=True, description='Configuration file name'),
            'server_allowed_ips': fields.List(fields.String(required=True, description='IP Pattern'))
        }))
    })

    status_model = api.model('Status', {
        'is_running': fields.Boolean(description='Algorithm running status')
    })

    stundenplan_input = __register_input_models(api)

    stundenplan_output = __register_output_models(api)

    return {
        'config_model': config_model,
        'stundenplan_input': stundenplan_input,
        'stundenplan_output': stundenplan_output,
        'status_model': status_model
    }
