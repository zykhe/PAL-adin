# PAL-adin Technical Specifications

## 📋 Overview

This document provides detailed technical specifications for PAL-adin's physical embodiment, including component selections, interface protocols, and implementation details for each major system.

---

## 🏗️ Mechanical System Specifications

### Chassis & Frame

#### Structural Design
- **Material**: 6061-T6 Aluminum alloy frame with carbon fiber reinforcement
- **Dimensions**: 600mm (W) × 800mm (D) × 1200mm (H)
- **Weight**: 45kg (including all components)
- **Load Capacity**: 20kg additional payload
- **Frame Modularity**: 6-module design for easy maintenance and upgrades

#### Suspension System
- **Type**: Independent double-wishbone suspension
- **Travel**: 50mm vertical travel per wheel
- **Damping**: Adjustable hydraulic dampers
- **Spring Rate**: Progressive rate springs (2-8 N/mm)

#### Weather Protection
- **IP Rating**: IP54 (dust protected, water resistant)
- **Operating Temperature**: -10°C to 45°C
- **Humidity Tolerance**: 10-90% non-condensing

### Mobility System

#### Wheel Configuration
```yaml
wheel_system:
  type: "Mecanum"
  count: 4
  diameter: "250mm"
  width: "100mm"
  roller_angle: 45
  material: "Polyurethane with aluminum hub"
  
performance:
  max_speed: "2.0 m/s"
  acceleration: "1.5 m/s²"
  turning_radius: "0 (omnidirectional)"
  climb_angle: "15 degrees"
  ground_clearance: "80mm"
```

#### Motor Specifications
- **Motor Type**: Brushless DC (BLDC) motors
- **Power**: 400W per motor (1.6kW total)
- **Voltage**: 48V system
- **Torque**: 2.5 Nm continuous, 7.5 Nm peak
- **Encoder**: 4096 PPR incremental encoder
- **Gear Ratio**: 15:1 planetary gearbox

#### Motor Controller
- **Model**: Roboteq SBL2360
- **Interface**: CAN bus, USB, RS232
- **Current Limiting**: Programmable current limits
- **Regenerative Braking**: Yes, with energy recovery
- **Safety Features**: Over-temperature, over-current, stall detection

---

## 🧠 Computing System Architecture

### Primary Computing Unit

#### NVIDIA Jetson AGX Orin Specifications
```yaml
jetson_agx_orin:
  cpu: "Arm Cortex-A78AE (12-core)"
  gpu: "NVIDIA Ampere (2048 CUDA cores, 64 Tensor cores)"
  memory: "32GB LPDDR5"
  storage: "2TB NVMe SSD"
  ai_performance: "275 TOPS (INT8)"
  power_consumption: "15-60W"
  
interfaces:
  usb: "USB 3.2 Gen 2 (4x)"
  ethernet: "10GbE"
  display: "DisplayPort 1.4 (2x)"
  camera: "MIPI CSI-2 (6x)"
  expansion: "M.2 Key M (2x), PCIe Gen 4"
```

### Secondary Computing

#### Raspberry Pi 4B (2 units)
- **Purpose**: Sensor data preprocessing and communication
- **CPU**: ARM Cortex-A72 (4-core, 1.5GHz)
- **Memory**: 4GB LPDDR4
- **Storage**: 128GB microSD
- **Interfaces**: USB 3.0, Gigabit Ethernet, Wi-Fi, Bluetooth

### Network Architecture
```yaml
network_configuration:
  internal_network:
    type: "Gigabit Ethernet"
    topology: "Star topology"
    protocol: "TCP/IP with ROS2 DDS"
  
  external_connectivity:
    primary: "5G/4G LTE modem"
    backup: "WiFi 6E (802.11ax)"
    fallback: "Ethernet connection"
  
  security:
    vpn: "WireGuard tunnel to VPS"
    encryption: "TLS 1.3 for all communications"
    authentication: "Mutual certificate authentication"
```

---

## 👁️ Sensory System Specifications

### Vision System

#### Primary 3D Camera
- **Model**: Intel RealSense D435i
- **Resolution**: 1920×1080 @ 30fps
- **Depth Range**: 0.3m - 10m
- **Depth Accuracy**: ±2mm at 1m distance
- **Field of View**: 87° × 58°
- **Interface**: USB 3.1 Type-C

#### 360° Camera Array
```yaml
camera_array:
  count: 4
  model: "Raspberry Pi Camera Module V2"
  resolution: "3280×2464"
  fps: 30
  arrangement: "Tetrahedral configuration"
  overlap: "15 degrees between adjacent cameras"
  stitching: "Real-time OpenCV stitching"
```

#### Processing Pipeline
```python
# vision_processing.py
class VisionProcessingPipeline:
    def __init__(self):
        self.depth_camera = RealSenseD435i()
        self.camera_array = CameraArray()
        self.object_detector = YOLOv8Detector()
        self.face_recognizer = FaceRecognitionNet()
        self.stitcher = PanoramaStitcher()
    
    async def process_visual_data(self):
        """Process all visual inputs into unified perception"""
        # Get depth data
        depth_frame = await self.depth_camera.get_depth_frame()
        color_frame = await self.depth_camera.get_color_frame()
        
        # Get 360° view
        camera_images = await self.camera_array.capture_all()
        panorama = await self.stitcher.stitch_images(camera_images)
        
        # Object detection
        objects = await self.object_detector.detect(color_frame)
        
        # Face recognition
        faces = await self.face_recognizer.recognize(color_frame)
        
        return VisualPerception(
            depth=depth_frame,
            panorama=panorama,
            objects=objects,
            faces=faces,
            timestamp=datetime.utcnow()
        )
```

### Audio System

#### Microphone Array
```yaml
microphone_array:
  configuration: "Circular array (7 microphones)"
  microphone_type: "MEMS digital microphones"
  sampling_rate: "48 kHz"
  bit_depth: "24-bit"
  frequency_response: "20 Hz - 20 kHz"
  beamforming: "Digital beamforming with 8 directions"
  
audio_processing:
  noise_reduction: "Spectral subtraction + Wiener filter"
  echo_cancellation: "AEC algorithm"
  voice_activity_detection: "VAD with energy threshold"
  sound_localization: "TDOA-based localization"
  speech_recognition: "Whisper-large-v2 model"
```

#### Speaker System
- **Configuration**: 2.1 channel system (2x full-range, 1x subwoofer)
- **Power**: 20W total output
- **Frequency Response**: 80Hz - 20kHz
- **Voice Synthesis**: Coqui TTS with PAL-adin voice profile

### Tactile Sensing

#### Touch Sensors
```yaml
touch_sensors:
  type: "Capacitive touch sensors"
  locations: "Gripper fingers, arm segments, chassis"
  sensitivity: "0.1 N force resolution"
  response_time: "<10ms"
  temperature_compensation: "Yes"
  
force_feedback:
  gripper_force_sensor: "0-50N range, 0.1N resolution"
  arm_joint_torque: "Built-in motor current sensing"
  collision_detection: "Current spike detection"
```

---

## 🦾 Manipulation System Specifications

### Robotic Arm

#### Kinematic Configuration
```yaml
arm_configuration:
  degrees_of_freedom: 6
  reach: "800mm"
  payload: "5kg (recommended), 10kg (maximum)"
  repeatability: "±0.02mm"
  max_joint_speed: "180 degrees/second"
  
joint_specifications:
  joint_1: "±180 degrees (base rotation)"
  joint_2: "±90 degrees (shoulder)"
  joint_3: "±135 degrees (elbow)"
  joint_4: "±180 degrees (wrist pitch)"
  joint_5: "±180 degrees (wrist roll)"
  joint_6: "±360 degrees (wrist rotation)"
```

#### Actuator Specifications
- **Motor Type**: Brushless DC with harmonic drive
- **Gear Ratio**: 100:1 (joints 1-3), 50:1 (joints 4-6)
- **Brake**: Integrated electromagnetic brake
- **Encoder**: 20-bit absolute encoder
- **Communication**: CAN bus with real-time control

### Gripper System

#### Adaptive Gripper
```yaml
gripper_specifications:
  type: "Parallel jaw adaptive gripper"
  opening_range: "0-150mm"
  gripping_force: "0-50N (adjustable)"
  finger_length: "120mm"
  grip_speed: "100mm/s"
  
sensors:
  position: "Linear potentiometer (0.1mm resolution)"
  force: "Force sensor array (0.1N resolution)"
  slip_detection: "Tactile slip sensors"
  temperature: "Integrated temperature sensor"
```

#### Control System
```python
# manipulation_control.py
class ManipulationController:
    def __init__(self):
        self.arm_controller = ArmController()
        self.gripper_controller = GripperController()
        self.kinematics_solver = KinematicsSolver()
        self.path_planner = PathPlanner()
    
    async def move_to_pose(self, target_pose, speed=0.5):
        """Move arm to target pose with collision avoidance"""
        # Solve inverse kinematics
        joint_angles = await self.kinematics_solver.inverse_kinematics(target_pose)
        
        # Plan collision-free path
        path = await self.path_planner.plan_path(
            start=self.current_joint_angles,
            goal=joint_angles,
            speed=speed
        )
        
        # Execute trajectory
        return await self.arm_controller.execute_trajectory(path)
    
    async def grasp_object(self, object_pose, force=10.0):
        """Grasp object at specified pose with given force"""
        # Move to approach position
        approach_pose = object_pose.copy()
        approach_pose.position.z += 50  # 50mm above object
        
        await self.move_to_pose(approach_pose)
        
        # Move to grasp position
        await self.move_to_pose(object_pose, speed=0.2)
        
        # Close gripper with specified force
        await self.gripper_controller.close(force=force)
        
        # Verify grasp
        return await self.gripper_controller.verify_grasp()
```

---

## ⚡ Power System Specifications

### Battery System

#### Primary Battery Pack
```yaml
battery_pack:
  chemistry: "LiFePO4 (Lithium Iron Phosphate)"
  voltage: "48V nominal"
  capacity: "100Ah (5kWh)"
  cells: "16S configuration (16 cells in series)"
  bms: "Smart BMS with balancing and protection"
  
performance:
  continuous_current: "100A"
  peak_current: "200A (10 seconds)"
  charge_time: "4 hours (0-100%)"
  cycle_life: "2000+ cycles @ 80% DoD"
  operating_temperature: "-20°C to 60°C"
```

#### Power Distribution
```yaml
power_distribution:
  primary_voltage: "48V"
  secondary_voltages: ["12V", "5V", "3.3V"]
  
converters:
  motor_power: "48V direct from battery"
  computing_power: "48V to 12V DC-DC (500W)"
  sensor_power: "12V to 5V DC-DC (100W)"
  logic_power: "5V to 3.3V LDO regulators (50W)"
  
monitoring:
  voltage_monitoring: "All voltage rails"
  current_monitoring: "All major subsystems"
  temperature_monitoring: "Battery, motors, electronics"
  power_consumption_tracking: "Real-time logging"
```

### Charging System

#### AC Charging
- **Input**: 100-240V AC, 50/60Hz
- **Charger**: 48V 25A smart charger
- **Charging Algorithm**: CC-CV with temperature compensation
- **Safety**: Over-voltage, over-current, reverse polarity protection

#### Solar Charging Option
```yaml
solar_charging:
  panel_type: "Monocrystalline silicon"
  panel_power: "400W (2x 200W panels)"
  panel_voltage: "24V (2 panels in series)"
  charge_controller: "MPPT charge controller"
  
charging_efficiency:
  solar_to_battery: "85-90%"
  charging_time: "6-8 hours (full charge in good sun)"
  weather_compensation: "Temperature-based charging adjustment"
```

---

## 🔌 Communication & Interface Protocols

### Internal Communication

#### ROS2 Architecture
```yaml
ros2_configuration:
  version: "Humble Hawksbill"
  middleware: "Fast DDS"
  domain_id: "42 (unique for PAL-adin)"
  
node_structure:
  mobility_controller: "manages wheel motors and navigation"
  manipulation_controller: "controls arm and gripper"
  sensory_processor: "processes all sensor data"
  safety_monitor: "oversees all safety systems"
  power_manager: "manages power distribution"
  interface_bridge: "bridges ROS2 to external APIs"
  
message_types:
  geometry_msgs: "poses, transforms, vectors"
  sensor_msgs: "camera images, laser scans, IMU data"
  std_msgs: "basic data types"
  paladin_msgs: "custom PAL-adin specific messages"
```

#### CAN Bus for Motor Control
```yaml
can_bus_configuration:
  standard: "CAN 2.0B"
  bit_rate: "1 Mbps"
  termination: "120 ohm at both ends"
  
message_ids:
  motor_commands: "0x100-0x10F (4 motors)"
  motor_feedback: "0x200-0x20F (4 motors)"
  system_status: "0x300"
  emergency_stop: "0x7FF (highest priority)"
  
protocol:
  update_rate: "100 Hz for motor commands"
  error_handling: "Automatic retransmission"
  bus_off_recovery: "Automatic recovery"
```

### External Communication

#### WebSocket API
```python
# websocket_interface.py
class PALadinWebSocketInterface:
    def __init__(self):
        self.websocket_server = WebSocketServer()
        self.message_handler = MessageHandler()
        self.authenticator = Authenticator()
    
    async def handle_connection(self, websocket, path):
        """Handle incoming WebSocket connections"""
        # Authenticate connection
        if not await self.authenticator.authenticate(websocket):
            await websocket.close(code=4001, reason="Authentication failed")
            return
        
        # Handle messages
        async for message in websocket:
            try:
                response = await self.message_handler.process_message(message)
                await websocket.send(response)
            except Exception as e:
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': str(e)
                }))
    
    async def broadcast_sensor_data(self, sensor_data):
        """Broadcast sensor data to all connected clients"""
        message = {
            'type': 'sensor_data',
            'timestamp': datetime.utcnow().isoformat(),
            'data': sensor_data
        }
        await self.websocket_server.broadcast(message)
```

#### REST API for Configuration
```yaml
rest_api_endpoints:
  GET /api/status: "Get system status"
  GET /api/sensors: "Get current sensor readings"
  POST /api/commands: "Send command to PAL-adin"
  GET /api/config: "Get current configuration"
  PUT /api/config: "Update configuration"
  GET /api/logs: "Get system logs"
  
authentication:
  method: "JWT tokens"
  token_expiry: "24 hours"
  refresh_token: "7 days"
  
rate_limiting:
  requests_per_minute: 60
  burst_limit: 10
```

---

## 🛡️ Safety System Specifications

### Emergency Stop Systems

#### Hardware Emergency Stops
```yaml
emergency_stop_buttons:
  count: 4
  locations: "Front, back, left, right sides"
  type: "Mushroom-head, normally closed"
  activation_force: "5-10 N"
  response_time: "<100ms"
  
wired_emergency_stop:
  circuit: "Series-wired normally closed circuit"
  monitoring: "Continuous circuit integrity check"
  response: "Immediate motor power cutoff"
  backup_power: "Supercapacitor for guaranteed operation"
```

#### Software Emergency Stop
```python
# emergency_stop.py
class EmergencyStopSystem:
    def __init__(self):
        self.hardware_monitor = HardwareEmergencyMonitor()
        self.software_monitor = SoftwareEmergencyMonitor()
        self.voice_detector = VoiceEmergencyDetector()
        self.remote_monitor = RemoteEmergencyMonitor()
    
    async def continuous_monitoring(self):
        """Continuous emergency stop monitoring"""
        while True:
            emergency_conditions = []
            
            # Check hardware emergency stops
            if await self.hardware_monitor.check_emergency():
                emergency_conditions.append('hardware')
            
            # Check software conditions
            if await self.software_monitor.check_emergency():
                emergency_conditions.append('software')
            
            # Check voice commands
            if await self.voice_detector.check_emergency_command():
                emergency_conditions.append('voice')
            
            # Check remote emergency
            if await self.remote_monitor.check_emergency():
                emergency_conditions.append('remote')
            
            # Execute emergency stop if any condition is true
            if emergency_conditions:
                await self.execute_emergency_stop(emergency_conditions)
            
            await asyncio.sleep(0.01)  # 100Hz monitoring
    
    async def execute_emergency_stop(self, sources):
        """Execute immediate emergency stop"""
        # Cut power to motors
        await self.power_controller.cut_motor_power()
        
        # Apply brakes
        await self.brake_controller.apply_all_brakes()
        
        # Log emergency event
        await self.logger.log_emergency_event(sources)
        
        # Notify monitoring systems
        await self.notification_system.notify_emergency(sources)
```

### Collision Avoidance

#### Multi-Layer Detection
```yaml
collision_detection_layers:
  layer_1_farthest:
    sensors: ["Lidar", "360° cameras"]
    range: "5 meters"
    purpose: "Early warning and path planning"
    reaction: "Speed reduction, path replanning"
  
  layer_2_intermediate:
    sensors: ["Depth camera", "Ultrasonic sensors"]
    range: "2 meters"
    purpose: "Obstacle detection and avoidance"
    reaction: "Direction change, speed adjustment"
  
  layer_3_immediate:
    sensors: ["Bump sensors", "Current monitoring"]
    range: "Contact detection"
    purpose: "Immediate collision detection"
    reaction: "Emergency stop"
```

#### Safe Operating Envelopes
```python
# safety_envelope.py
class SafetyEnvelope:
    def __init__(self):
        self.envelope_calculator = EnvelopeCalculator()
        self.human_detector = HumanDetector()
        self.distance_monitor = DistanceMonitor()
    
    async def calculate_safe_envelope(self):
        """Calculate dynamic safe operating envelope"""
        # Detect humans in vicinity
        humans = await self.human_detector.detect_humans()
        
        # Calculate safe distances based on speed and direction
        safe_distances = {}
        for human in humans:
            distance = await self.distance_monitor.calculate_distance(human)
            safe_distance = self.calculate_required_distance(
                human.position, human.velocity, self.current_velocity
            )
            safe_distances[human.id] = safe_distance
        
        return safe_distances
    
    def calculate_required_distance(self, human_pos, human_vel, robot_vel):
        """Calculate minimum safe distance from human"""
        # Stopping distance calculation
        stopping_distance = (robot_vel ** 2) / (2 * self.max_deceleration)
        
        # Safety margin based on relative velocity
        relative_velocity = abs(robot_vel - human_vel)
        safety_margin = relative_velocity * self.reaction_time
        
        # Minimum safe distance
        return stopping_distance + safety_margin + self.minimum_distance
```

---

## 📊 Performance Monitoring & Diagnostics

### System Health Monitoring

#### Telemetry Data Collection
```yaml
telemetry_categories:
  performance_metrics:
    cpu_usage: "All computing units"
    memory_usage: "RAM and storage usage"
    gpu_utilization: "AI processing load"
    network_throughput: "Data transfer rates"
  
  power_metrics:
    battery_voltage: "Cell voltages and pack voltage"
    current_draw: "Subsystem current consumption"
    power_efficiency: "System efficiency calculations"
    charge_cycles: "Battery health tracking"
  
  mechanical_metrics:
    motor_temperatures: "All motor temperatures"
    joint_positions: "Current joint angles"
    wheel_odometry: "Distance and speed measurements"
    vibration_analysis: "Mechanical health monitoring"
  
  safety_metrics:
    emergency_stops: "Emergency stop events"
    near_misses: "Near collision events"
    safety_violations: "Safety boundary breaches"
    system_errors: "Error rates and types"
```

#### Predictive Maintenance
```python
# predictive_maintenance.py
class PredictiveMaintenance:
    def __init__(self):
        self.health_analyzer = HealthAnalyzer()
        self.failure_predictor = FailurePredictor()
        self.maintenance_scheduler = MaintenanceScheduler()
    
    async def analyze_system_health(self):
        """Analyze system health and predict maintenance needs"""
        # Collect current telemetry
        telemetry = await self.collect_telemetry()
        
        # Analyze health indicators
        health_status = await self.health_analyzer.analyze(telemetry)
        
        # Predict potential failures
        failure_predictions = await self.failure_predictor.predict(
            health_status, historical_data=self.historical_data
        )
        
        # Schedule maintenance if needed
        for prediction in failure_predictions:
            if prediction.probability > 0.7:
                await self.maintenance_scheduler.schedule_maintenance(
                    component=prediction.component,
                    urgency=prediction.urgency,
                    estimated_failure_time=prediction.time_to_failure
                )
        
        return health_status, failure_predictions
```

---

## 🔄 Software Architecture

### Control System Architecture

#### Hierarchical Control Structure
```python
# control_architecture.py
class PALadinControlSystem:
    def __init__(self):
        # High-level decision making
        self.executive_controller = ExecutiveController()
        
        # Mid-level behavior control
        self.behavior_controller = BehaviorController()
        self.task_planner = TaskPlanner()
        
        # Low-level motor control
        self.motion_controller = MotionController()
        self.manipulation_controller = ManipulationController()
        
        # Safety and monitoring
        self.safety_controller = SafetyController()
        self.monitoring_system = MonitoringSystem()
    
    async def execute_command(self, command):
        """Execute high-level command with safety oversight"""
        # Safety check first
        if not await self.safety_controller.command_safe(command):
            raise SafetyError("Command rejected by safety system")
        
        # Plan task execution
        task_plan = await self.task_planner.create_plan(command)
        
        # Execute with monitoring
        execution_result = await self.behavior_controller.execute_plan(
            task_plan, 
            monitor=self.monitoring_system
        )
        
        return execution_result
```

### State Management

#### System State Machine
```yaml
system_states:
  idle:
    description: "Waiting for commands"
    power_consumption: "Low"
    capabilities: "Monitoring, communication"
  
  active:
    description: "Executing tasks"
    power_consumption: "Medium to high"
    capabilities: "Full system capabilities"
  
  navigation:
    description: "Moving to location"
    power_consumption: "High"
    capabilities: "Mobility, obstacle avoidance"
  
  manipulation:
    description: "Interacting with objects"
    power_consumption: "Medium"
    capabilities: "Arm control, grasping"
  
  emergency_stop:
    description: "Emergency stop activated"
    power_consumption: "Minimal"
    capabilities: "Safety monitoring only"
  
  maintenance:
    description: "Maintenance mode"
    power_consumption: "Variable"
    capabilities: "Diagnostics, calibration"
  
  charging:
    description: "Charging battery"
    power_consumption: "Charging power"
    capabilities: "Monitoring, charging control"
```

---

## 📈 Testing & Validation Framework

### Automated Testing

#### Test Categories
```yaml
unit_tests:
  motor_controllers: "Motor response and accuracy"
  sensor_interfaces: "Sensor data validation"
  communication_protocols: "Message passing integrity"
  safety_systems: "Emergency response testing"
  
integration_tests:
  mobility_system: "Navigation and movement"
  manipulation_system: "Object interaction"
  sensory_fusion: "Multi-sensor integration"
  power_management: "Power system coordination"
  
field_tests:
  navigation_challenges: "Complex environments"
  manipulation_tasks: "Real-world object handling"
  human_interaction: "Safety and usability"
  endurance_testing: "Long-term operation"
```

#### Test Automation Framework
```python
# test_framework.py
class PALadinTestFramework:
    def __init__(self):
        self.test_runner = TestRunner()
        self.data_collector = TestDataCollector()
        self.report_generator = TestReportGenerator()
    
    async def run_comprehensive_tests(self):
        """Run complete test suite"""
        test_results = {}
        
        # Unit tests
        test_results['unit'] = await self.run_unit_tests()
        
        # Integration tests
        test_results['integration'] = await self.run_integration_tests()
        
        # Field tests
        test_results['field'] = await self.run_field_tests()
        
        # Generate comprehensive report
        report = await self.report_generator.generate_report(test_results)
        
        return report
    
    async def run_navigation_tests(self):
        """Test navigation capabilities"""
        test_scenarios = [
            'simple_point_to_point',
            'obstacle_avoidance',
            'dynamic_environment',
            'multi_waypoint_navigation',
            'localization_accuracy'
        ]
        
        results = {}
        for scenario in test_scenarios:
            results[scenario] = await self.test_runner.execute_test(
                category='navigation',
                scenario=scenario,
                parameters=self.get_test_parameters(scenario)
            )
        
        return results
```

---

## 📋 Component Bill of Materials

### Detailed Component List

#### Computing & Electronics
```yaml
computing_system:
  jetson_agx_orin: "$2,000"
  raspberry_pi_4b_4gb: 2 × "$75"
  nvme_ssd_2tb: "$200"
  microsd_cards: 2 × "$25"
  can_bus_interface: "$150"
  ethernet_switch: "$100"
  
power_system:
  lifepo4_battery_48v_100ah: "$1,500"
  bms_48v_100a: "$300"
  dc_dc_converters: "$400"
  charger_48v_25a: "$250"
  solar_panel_400w: "$600"
  solar_charge_controller: "$200"
  
mobility_system:
  mecanum_wheels_250mm: 4 × "$150"
  brushless_motors_400w: 4 × "$200"
  motor_controllers: 4 × "$100"
  suspension_components: "$500"
  chassis_frame: "$800"
  
manipulation_system:
  robotic_arm_6dof: "$3,000"
  adaptive_gripper: "$800"
  force_sensors: "$200"
  
sensory_system:
  realsense_d435i: "$200"
  raspberry_pi_cameras: 4 × "$30"
  rplidar_a1: "$300"
  microphone_array: "$150"
  ultrasonic_sensors: 4 × "$25"
  touch_sensors: "$100"
  
safety_system:
  emergency_stop_buttons: 4 × "$50"
  safety_light_curtains: "$400"
  backup_power_system: "$300"
  
miscellaneous:
  wiring_harnesses: "$500"
  fasteners_hardware: "$200"
  3d_printed_parts: "$300"
  tools_assembly: "$400"
  
total_estimated_cost: "$15,000-18,000"
```

---

This technical specification document provides the detailed implementation details needed to begin the physical development of PAL-adin. Each system is designed with modularity, safety, and reliability in mind while maintaining the flexibility for future upgrades and improvements.