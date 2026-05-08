from cnc_app.models import Machine, Tool, Operator, FailureReason


def run():

    print("Seeding database...")

    # Machines
    m1, _ = Machine.objects.get_or_create(
        machine_code="VF2-01",
        defaults={
            "machine_name": "Haas VF-2",
            "location": "Shop Floor A"
        }
    )

    m2, _ = Machine.objects.get_or_create(
        machine_code="NLX-02",
        defaults={
            "machine_name": "DMG Mori NLX",
            "location": "Shop Floor B"
        }
    )

    # Operators
    Operator.objects.get_or_create(
        employee_id="EMP101",
        defaults={
            "name": "Rahul Patil",
            "shift": "Day"
        }
    )

    Operator.objects.get_or_create(
        employee_id="EMP102",
        defaults={
            "name": "Sneha Kulkarni",
            "shift": "Night"
        }
    )

    # Tools
    Tool.objects.get_or_create(
        tool_code="T001",
        defaults={
            "tool_name": "Carbide End Mill",
            "expected_life": 10000,
            "machine": m1
        }
    )

    Tool.objects.get_or_create(
        tool_code="T002",
        defaults={
            "tool_name": "Drill Bit",
            "expected_life": 7000,
            "machine": m2
        }
    )

    Tool.objects.get_or_create(
        tool_code="T003",
        defaults={
            "tool_name": "Face Mill Cutter",
            "expected_life": 12000,
            "machine": m1
        }
    )

    # Failure reasons
    FailureReason.objects.get_or_create(reason="Tool Wear")
    FailureReason.objects.get_or_create(reason="Machine Vibration")
    FailureReason.objects.get_or_create(reason="Incorrect Feed Rate")
    FailureReason.objects.get_or_create(reason="Material Hardness")

    print("Data inserted successfully!")