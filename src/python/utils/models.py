from flask_restx import fields

def __register_input_models(api):
    constraint_model = api.model('InputConstraint', {
        'id': fields.String(required=True, description='Constraint ID'),
        'type': fields.String(required=True, description='Constraint Type'),
        'owner': fields.String(required=True, description='Constraint Owner'),
        'inverted': fields.Boolean(description="Constraint inverted?"),
        "fields": fields.Raw(description="Additional fields for constraint-type specific information")
    })

    timeslot_model = api.model('InputTimeslot', {
        'day': fields.Integer(required=True, description='Day'),
        'timeslot': fields.Integer(required=True, description='Timeslot'),
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

    constraints = fields.List(fields.Nested(constraint_model))

    # Schedule input model
    stundenplan_input = api.model('Datenbasis', {
        'timeslots': fields.List(fields.Nested(timeslot_model), required=True, description='List of timeslots available'),
        'rooms': fields.List(fields.Nested(room_model), required=True, description='List of rooms available'),
        'events': fields.List(fields.Nested(event_model), required=True, description='List of events to schedule'),
        'constraints': fields.Nested(api.model('InputConstraints', {
            'hard': constraints,
            'soft': constraints
        }), required=True, description='Constraints for the schedule')
    })

    return stundenplan_input

def __register_output_models(api):
    constraint_model = api.model('OutputConstraint', {
        'id': fields.String(required=True, description='Constraint ID'),
        'type': fields.String(required=True, description='Constraint Type'),
        'owner': fields.String(required=True, description='Constraint Owner'),
        'inverted': fields.Boolean(description="Constraint inverted?"),
        "fields": fields.Raw(description="Additional fields for constraint-type specific information")
    })

    core_constraint_model = api.model('CoreConstraints', {
        'employee_conflicts': fields.Integer(required=True, description='Count of Constraints'),
        'student_conflicts': fields.Integer(required=True, description='Count of Constraints'),
        'room_capacity': fields.Integer(required=True, description='Count of Constraints'),
        'room_type': fields.Integer(required=True, description='Count of Constraints'),
    })

    # Event Model
    event_model = api.model('Event', {
        'day': fields.Integer(required=True, description='Day of the week (e.g., 4 for Thursday)'),
        'timeslot': fields.Integer(required=True, description='Timeslot number'),
        'event': fields.String(required=True, description='Event name'),
        'room': fields.String(required=True, description='Room name or code'),
        'participants': fields.List(fields.String, required=True, description='List of participants in the event'),
    })

    constraints = fields.List(fields.Nested(constraint_model))

    # Core Constraints Model
    core_constraints_model = api.model('WrappedCoreConstraints', {
        'fitness': fields.Integer(required=True, description='Fitness score for core constraints'),
        'unsatisfied': fields.Nested(core_constraint_model),
        'satisfied': fields.Nested(core_constraint_model),
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
            'runtime': fields.String(required=True, description='Runtime of the algorithm in seconds'),
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
