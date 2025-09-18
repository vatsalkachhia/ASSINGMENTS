from core.agentic_system import app


sample_input = {'schema_version': '1.0',
    'message_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    'trace_id': 'a4f1c2b0-9f5d-4e1b-8a1d-1234567890ab',
    'created_at': '2025-09-17T03:12:45Z',
    'panel_id': 'PANEL-000123',
    'defect_type': 'orange_peel',
    'issue_critical': False,
    'work_order': {'order_id': 'WO-20250917-0001', 'vin': '1HGCM82633A004352'},
    'source': {
        'edge_id': 'edge-42',
        'camera_id': 'cam-7',
        'model_version': 'v2.4.1'},
    'environment': {
        'temperature_c': 16.5,
        'humidity_pct': 40.0,
        'spray_pressure_bar': 2.0
        },
    'image': {
            'image_id': 'b7e23ec2-3c4a-4b9f-8f6a-111111111111',
            'uri': 's3://inspection-bucket/2025/09/17/panel000123_cam7_1.jpg',
            'camera_pose': {'translation_mm': [1200.0, 450.0, 300.0],
            'rotation_rpy_deg': [0.0, -2.5, 90.0],
            'extrinsics_matrix': [[0.0, -1.0, 0.0, 1200.0],
                [1.0, 0.0, 0.0, 450.0],
                [0.0, 0.0, 1.0, 300.0],
                [0.0, 0.0, 0.0, 1.0]]},
            'timestamp': '2025-09-17T03:12:30Z'
    },
    'processing_latency_ms': 124,
    'reasoning_layer_messages': [],
    'reasoning_layer_output': ' ',
    'action_layer_messages': [],
    'action_layer_output': ""}


if __name__ == "__main__":
    result = app.invoke(sample_input)


