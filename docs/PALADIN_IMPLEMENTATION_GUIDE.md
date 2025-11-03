# PAL-adin Physical Body Implementation Guide

## 🚀 Getting Started

This guide provides practical implementation details, code examples, and configuration files to begin developing PAL-adin's physical embodiment. It's designed to be used alongside the Physical Body Plan and Technical Specifications documents.

---

## 🛠️ Development Environment Setup

### System Requirements

#### Development Machine
- **OS**: Ubuntu 22.04 LTS (recommended) or macOS 13+
- **CPU**: 8+ cores for simulation and compilation
- **RAM**: 32GB+ minimum
- **Storage**: 500GB+ SSD
- **GPU**: NVIDIA RTX 3080+ for AI development

#### Target Hardware
- **Primary Compute**: NVIDIA Jetson AGX Orin Developer Kit
- **Secondary**: Raspberry Pi 4B (2 units)
- **Development Board**: Custom STM32/Nucleo for motor control

### Software Installation

#### ROS2 Humble Installation
```bash
# Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS2 apt repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'

# Install ROS2 Humble
sudo apt update
sudo apt install ros-humble-desktop python3-argcomplete
```

#### Development Tools
```bash
# Install development tools
sudo apt install -y \
    git \
    cmake \
    build-essential \
    python3-pip \
    python3-venv \
    python3-dev \
    cppcheck \
    clang-format \
    code

# Install Python dependencies
pip3 install \
    numpy \
    scipy \
    opencv-python \
    pyyaml \
    colcon-common-extensions \
    rclpy \
    geometry-msgs \
    sensor-msgs \
    std-msgs
```

#### NVIDIA Jetson Setup
```bash
# Flash Jetson with latest JetPack
# Follow NVIDIA instructions for JetPack 5.1+

# Install ROS2 on Jetson
sudo apt update
sudo apt install ros-humble-ros-base

# Install Jetson-specific packages
sudo apt install -y \
    python3-jetson-stats \
    jetson-stats \
    tegra-tools
```

---

## 🏗️ Project Structure

### Repository Organization
```
paladin-physical/
├── README.md
├── LICENSE
├── .gitignore
├── docs/                          # Documentation
│   ├── PALADIN_PHYSICAL_BODY_PLAN.md
│   ├── PALADIN_TECHNICAL_SPECIFICATIONS.md
│   └── PALADIN_IMPLEMENTATION_GUIDE.md
├── src/                           # Source code
│   ├── paladin_core/              # Core PAL-adin software
│   │   ├── package.xml
│   │   ├── setup.py
│   │   ├── paladin_core/
│   │   │   ├── __init__.py
│   │   │   ├── executive_controller.py
│   │   │   ├── safety_controller.py
│   │   │   └── state_manager.py
│   ├── paladin_mobility/          # Mobility system
│   │   ├── package.xml
│   │   ├── setup.py
│   │   ├── paladin_mobility/
│   │   │   ├── __init__.py
│   │   │   ├── mecanum_controller.py
│   │   │   ├── navigation_stack.py
│   │   │   └── motor_interface.py
│   ├── paladin_manipulation/      # Manipulation system
│   │   ├── package.xml
│   │   ├── setup.py
│   │   ├── paladin_manipulation/
│   │   │   ├── __init__.py
│   │   │   ├── arm_controller.py
│   │   │   ├── gripper_controller.py
│   │   │   └── kinematics_solver.py
│   ├── paladin_sensing/           # Sensory systems
│   │   ├── package.xml
│   │   ├── setup.py
│   │   ├── paladin_sensing/
│   │   │   ├── __init__.py
│   │   │   ├── vision_processor.py
│   │   │   ├── audio_processor.py
│   │   │   └── sensor_fusion.py
│   ├── paladin_power/             # Power management
│   │   ├── package.xml
│   │   ├── setup.py
│   │   ├── paladin_power/
│   │   │   ├── __init__.py
│   │   │   ├── battery_monitor.py
│   │   │   ├── power_controller.py
│   │   │   └── energy_optimizer.py
│   └── paladin_interface/         # External interfaces
│       ├── package.xml
│       ├── setup.py
│       ├── paladin_interface/
│       │   ├── __init__.py
│       │   ├── websocket_server.py
│       │   ├── rest_api.py
│       │   └── digital_bridge.py
├── config/                        # Configuration files
│   ├── ros_params/
│   │   ├── mobility_params.yaml
│   │   ├── manipulation_params.yaml
│   │   ├── sensing_params.yaml
│   │   └── safety_params.yaml
│   ├── hardware_config/
│   │   ├── motor_config.yaml
│   │   ├── sensor_config.yaml
│   │   └── power_config.yaml
│   └── launch/
│       ├── paladin_bringup.launch.py
│       ├── navigation.launch.py
│       └── manipulation.launch.py
├── hardware/                      # Hardware designs
│   ├── cad/                       # CAD files
│   ├── pcb/                       # PCB designs
│   └── 3d_print/                  # 3D printable parts
├── scripts/                       # Utility scripts
│   ├── setup_environment.sh
│   ├── calibrate_sensors.py
│   ├── test_motors.py
│   └── system_check.py
├── tests/                         # Test suite
│   ├── unit_tests/
│   ├── integration_tests/
│   └── simulation_tests/
└── simulation/                    # Simulation environment
    ├── gazebo_worlds/
    ├── robot_models/
    └── test_scenarios/
```

---

## 🔧 Core System Implementation

### Executive Controller

#### Executive Controller Implementation
```python
# src/paladin_core/paladin_core/executive_controller.py
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from std_msgs.msg import String
from paladin_msgs.msg import SystemStatus, TaskCommand
from paladin_msgs.action import ExecuteTask
import asyncio
import json
from enum import Enum

class SystemState(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    NAVIGATION = "navigation"
    MANIPULATION = "manipulation"
    EMERGENCY_STOP = "emergency_stop"
    MAINTENANCE = "maintenance"
    CHARGING = "charging"

class ExecutiveController(Node):
    """High-level executive controller for PAL-adin"""
    
    def __init__(self):
        super().__init__('executive_controller')
        
        # State management
        self.current_state = SystemState.IDLE
        self.state_history = []
        
        # Action servers
        self.task_action_server = ActionServer(
            self,
            ExecuteTask,
            'execute_task',
            self.execute_task_callback
        )
        
        # Publishers
        self.status_publisher = self.create_publisher(
            SystemStatus, 'system_status', 10
        )
        self.command_publisher = self.create_publisher(
            TaskCommand, 'task_command', 10
        )
        
        # Subscribers
        self.safety_subscriber = self.create_subscription(
            String, 'safety_alerts', self.safety_callback, 10
        )
        
        # Timers
        self.status_timer = self.create_timer(
            1.0, self.publish_status
        )
        
        self.get_logger().info("Executive Controller initialized")
    
    async def execute_task_callback(self, goal_handle):
        """Execute high-level task"""
        self.get_logger().info(f"Executing task: {goal_handle.request.task_type}")
        
        # Validate task based on current state
        if not self.validate_task(goal_handle.request):
            goal_handle.abort()
            return ExecuteTask.Result(success=False, message="Task validation failed")
        
        # Change state based on task type
        new_state = self.determine_task_state(goal_handle.request.task_type)
        await self.change_state(new_state)
        
        # Execute task
        try:
            result = await self.execute_specific_task(goal_handle.request)
            goal_handle.succeed()
            return ExecuteTask.Result(success=True, message=result)
        except Exception as e:
            self.get_logger().error(f"Task execution failed: {e}")
            goal_handle.abort()
            return ExecuteTask.Result(success=False, message=str(e))
        finally:
            await self.change_state(SystemState.IDLE)
    
    def validate_task(self, task_command):
        """Validate task based on current state and system conditions"""
        # Check if task is allowed in current state
        if self.current_state == SystemState.EMERGENCY_STOP:
            return False
        
        # Check system resources
        if task_command.requires_power and not self.check_power_availability():
            return False
        
        # Check safety conditions
        if task_command.requires_movement and not self.check_movement_safety():
            return False
        
        return True
    
    def determine_task_state(self, task_type):
        """Determine appropriate system state for task type"""
        state_mapping = {
            'navigation': SystemState.NAVIGATION,
            'manipulation': SystemState.MANIPULATION,
            'charging': SystemState.CHARGING,
            'maintenance': SystemState.MAINTENANCE
        }
        return state_mapping.get(task_type, SystemState.ACTIVE)
    
    async def execute_specific_task(self, task_command):
        """Execute specific task based on type"""
        command = TaskCommand()
        command.task_type = task_command.task_type
        command.parameters = json.dumps(task_command.parameters)
        command.priority = task_command.priority
        
        # Send command to appropriate subsystem
        self.command_publisher.publish(command)
        
        # Wait for completion (simplified)
        await asyncio.sleep(1.0)
        
        return f"Task {task_command.task_type} completed successfully"
    
    async def change_state(self, new_state):
        """Change system state with proper transitions"""
        if new_state == self.current_state:
            return
        
        self.get_logger().info(f"Changing state: {self.current_state.value} -> {new_state.value}")
        
        # Log state change
        self.state_history.append({
            'from_state': self.current_state.value,
            'to_state': new_state.value,
            'timestamp': self.get_clock().now().to_msg()
        })
        
        self.current_state = new_state
        
        # Publish state change
        await self.publish_status()
    
    def safety_callback(self, msg):
        """Handle safety alerts"""
        alert_data = json.loads(msg.data)
        
        if alert_data['severity'] == 'critical':
            asyncio.create_task(self.handle_emergency_stop(alert_data))
    
    async def handle_emergency_stop(self, alert_data):
        """Handle emergency stop condition"""
        self.get_logger().error(f"Emergency stop triggered: {alert_data['message']}")
        await self.change_state(SystemState.EMERGENCY_STOP)
        
        # Send emergency stop command to all subsystems
        emergency_command = TaskCommand()
        emergency_command.task_type = 'emergency_stop'
        emergency_command.priority = 100  # Highest priority
        self.command_publisher.publish(emergency_command)
    
    def check_power_availability(self):
        """Check if sufficient power is available"""
        # Simplified check - in real implementation, query power system
        return True
    
    def check_movement_safety(self):
        """Check if movement is safe"""
        # Simplified check - in real implementation, query safety system
        return True
    
    async def publish_status(self):
        """Publish current system status"""
        status = SystemStatus()
        status.state = self.current_state.value
        status.timestamp = self.get_clock().now().to_msg()
        status.battery_level = 85.0  # Placeholder
        status.cpu_usage = 45.0     # Placeholder
        
        self.status_publisher.publish(status)

def main(args=None):
    rclpy.init(args=args)
    executive_controller = ExecutiveController()
    rclpy.spin(executive_controller)
    executive_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Safety Controller

#### Safety System Implementation
```python
# src/paladin_core/paladin_core/safety_controller.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32, String
from sensor_msgs.msg import LaserScan, Image
from geometry_msgs.msg import Twist
import numpy as np
import json
from enum import Enum

class SafetyLevel(Enum):
    SAFE = "safe"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class SafetyController(Node):
    """Comprehensive safety monitoring and control system"""
    
    def __init__(self):
        super().__init__('safety_controller')
        
        # Safety state
        self.safety_level = SafetyLevel.SAFE
        self.emergency_stop_active = False
        self.last_emergency_time = None
        
        # Safety thresholds
        self.min_obstacle_distance = 0.5  # meters
        self.max_speed = 2.0  # m/s
        self.max_angular_speed = 1.5  # rad/s
        
        # Subscribers
        self.laser_subscriber = self.create_subscription(
            LaserScan, 'laser_scan', self.laser_callback, 10
        )
        self.camera_subscriber = self.create_subscription(
            Image, 'camera_image', self.camera_callback, 10
        )
        self.emergency_button_subscriber = self.create_subscription(
            Bool, 'emergency_button', self.emergency_button_callback, 10
        )
        self.velocity_subscriber = self.create_subscription(
            Twist, 'cmd_vel', self.velocity_callback, 10
        )
        
        # Publishers
        self.safety_status_publisher = self.create_publisher(
            String, 'safety_status', 10
        )
        self.safe_velocity_publisher = self.create_publisher(
            Twist, 'safe_cmd_vel', 10
        )
        self.emergency_stop_publisher = self.create_publisher(
            Bool, 'emergency_stop', 10
        )
        
        # Timers
        self.safety_timer = self.create_timer(
            0.1, self.safety_monitoring_loop  # 10Hz
        )
        
        self.get_logger().info("Safety Controller initialized")
    
    def laser_callback(self, msg):
        """Process laser scan data for obstacle detection"""
        # Find minimum distance in scan
        ranges = np.array(msg.ranges)
        ranges = ranges[ranges > msg.range_min]  # Filter valid readings
        ranges = ranges[ranges < msg.range_max]
        
        if len(ranges) > 0:
            self.min_distance = np.min(ranges)
            self.closest_obstacle_angle = np.argmin(ranges) * msg.angle_increment + msg.angle_min
        else:
            self.min_distance = float('inf')
            self.closest_obstacle_angle = 0.0
    
    def camera_callback(self, msg):
        """Process camera data for human detection"""
        # Simplified - in real implementation, use human detection model
        self.humans_detected = False  # Placeholder
        self.human_distances = []     # Placeholder
    
    def emergency_button_callback(self, msg):
        """Handle emergency button press"""
        if msg.data and not self.emergency_stop_active:
            self.trigger_emergency_stop("Emergency button pressed")
    
    def velocity_callback(self, msg):
        """Monitor commanded velocity"""
        self.commanded_linear = msg.linear.x
        self.commanded_angular = msg.angular.z
    
    def safety_monitoring_loop(self):
        """Main safety monitoring loop"""
        # Assess current safety level
        new_safety_level = self.assess_safety_level()
        
        if new_safety_level != self.safety_level:
            self.safety_level = new_safety_level
            self.handle_safety_level_change()
        
        # Apply safety constraints to velocity
        safe_velocity = self.apply_safety_constraints()
        self.safe_velocity_publisher.publish(safe_velocity)
        
        # Publish safety status
        self.publish_safety_status()
    
    def assess_safety_level(self):
        """Assess current safety level based on all inputs"""
        if self.emergency_stop_active:
            return SafetyLevel.EMERGENCY
        
        if hasattr(self, 'min_distance') and self.min_distance < 0.3:
            return SafetyLevel.CRITICAL
        
        if hasattr(self, 'min_distance') and self.min_distance < 0.5:
            return SafetyLevel.WARNING
        
        if hasattr(self, 'humans_detected') and self.humans_detected:
            return SafetyLevel.WARNING
        
        return SafetyLevel.SAFE
    
    def handle_safety_level_change(self):
        """Handle changes in safety level"""
        self.get_logger().info(f"Safety level changed to: {self.safety_level.value}")
        
        if self.safety_level == SafetyLevel.EMERGENCY:
            self.activate_emergency_stop()
        elif self.safety_level == SafetyLevel.CRITICAL:
            self.limit_movement()
        elif self.safety_level == SafetyLevel.WARNING:
            self.reduce_speed()
    
    def apply_safety_constraints(self):
        """Apply safety constraints to commanded velocity"""
        safe_velocity = Twist()
        
        if self.safety_level == SafetyLevel.EMERGENCY:
            # Stop all movement
            safe_velocity.linear.x = 0.0
            safe_velocity.angular.z = 0.0
        
        elif self.safety_level == SafetyLevel.CRITICAL:
            # Allow only backward movement
            if hasattr(self, 'commanded_linear') and self.commanded_linear < 0:
                safe_velocity.linear.x = max(self.commanded_linear, -0.5)
            safe_velocity.angular.z = 0.0
        
        elif self.safety_level == SafetyLevel.WARNING:
            # Reduce speed based on distance to obstacles
            if hasattr(self, 'min_distance'):
                speed_factor = min(1.0, self.min_distance / 1.0)
                safe_velocity.linear.x = self.commanded_linear * speed_factor * 0.5
                safe_velocity.angular.z = self.commanded_angular * speed_factor * 0.5
        
        else:
            # Normal operation with speed limits
            if hasattr(self, 'commanded_linear'):
                safe_velocity.linear.x = np.clip(
                    self.commanded_linear, -self.max_speed, self.max_speed
                )
                safe_velocity.angular.z = np.clip(
                    self.commanded_angular, -self.max_angular_speed, self.max_angular_speed
                )
        
        return safe_velocity
    
    def trigger_emergency_stop(self, reason):
        """Trigger emergency stop"""
        self.get_logger().error(f"Emergency stop triggered: {reason}")
        self.emergency_stop_active = True
        self.last_emergency_time = self.get_clock().now()
        
        # Publish emergency stop signal
        emergency_msg = Bool()
        emergency_msg.data = True
        self.emergency_stop_publisher.publish(emergency_msg)
    
    def activate_emergency_stop(self):
        """Activate emergency stop procedures"""
        # Already handled in trigger_emergency_stop
        pass
    
    def limit_movement(self):
        """Limit movement in critical situations"""
        # Handled in apply_safety_constraints
        pass
    
    def reduce_speed(self):
        """Reduce speed in warning situations"""
        # Handled in apply_safety_constraints
        pass
    
    def publish_safety_status(self):
        """Publish current safety status"""
        status = {
            'safety_level': self.safety_level.value,
            'emergency_stop_active': self.emergency_stop_active,
            'min_obstacle_distance': getattr(self, 'min_distance', float('inf')),
            'humans_detected': getattr(self, 'humans_detected', False),
            'timestamp': self.get_clock().now().to_msg()
        }
        
        status_msg = String()
        status_msg.data = json.dumps(status)
        self.safety_status_publisher.publish(status_msg)

def main(args=None):
    rclpy.init(args=args)
    safety_controller = SafetyController()
    rclpy.spin(safety_controller)
    safety_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 🚗 Mobility System Implementation

### Mecanum Wheel Controller

#### Mobility Controller Implementation
```python
# src/paladin_mobility/paladin_mobility/mecanum_controller.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Quaternion
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
import numpy as np
import math

class MecanumController(Node):
    """Mecanum wheel kinematics controller"""
    
    def __init__(self):
        super().__init__('mecanum_controller')
        
        # Robot parameters
        self.wheel_radius = 0.125  # meters
        self.robot_length = 0.6    # meters (wheelbase length)
        self.robot_width = 0.5     # meters (track width)
        
        # Wheel positions (front-left, front-right, back-left, back-right)
        self.wheel_positions = [
            [self.robot_length/2, self.robot_width/2],   # FL
            [self.robot_length/2, -self.robot_width/2],  # FR
            [-self.robot_length/2, self.robot_width/2],  # BL
            [-self.robot_length/2, -self.robot_width/2]  # BR
        ]
        
        # Current odometry
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.last_time = self.get_clock().now()
        
        # Subscribers
        self.velocity_subscriber = self.create_subscription(
            Twist, 'safe_cmd_vel', self.velocity_callback, 10
        )
        
        # Publishers
        self.motor_speed_publishers = []
        for i in range(4):
            publisher = self.create_publisher(
                Float32, f'motor_{i}_speed', 10
            )
            self.motor_speed_publishers.append(publisher)
        
        self.odometry_publisher = self.create_publisher(
            Odometry, 'odom', 10
        )
        
        # Timer for odometry update
        self.odometry_timer = self.create_timer(
            0.1, self.update_odometry  # 10Hz
        )
        
        self.get_logger().info("Mecanum Controller initialized")
    
    def velocity_callback(self, msg):
        """Convert velocity command to wheel speeds"""
        # Extract velocity components
        vx = msg.linear.x   # Forward velocity
        vy = msg.linear.y   # Lateral velocity
        omega = msg.angular.z  # Angular velocity
        
        # Calculate wheel speeds using mecanum kinematics
        wheel_speeds = self.calculate_wheel_speeds(vx, vy, omega)
        
        # Publish wheel speeds
        for i, speed in enumerate(wheel_speeds):
            speed_msg = Float32()
            speed_msg.data = speed
            self.motor_speed_publishers[i].publish(speed_msg)
    
    def calculate_wheel_speeds(self, vx, vy, omega):
        """Calculate individual wheel speeds from robot velocity"""
        wheel_speeds = []
        
        for i, (lx, ly) in enumerate(self.wheel_positions):
            # Mecanum wheel kinematics
            # Different wheel roller angles for different wheels
            if i == 0:  # Front-left
                roller_angle = math.pi / 4
            elif i == 1:  # Front-right
                roller_angle = -math.pi / 4
            elif i == 2:  # Back-left
                roller_angle = -math.pi / 4
            else:  # Back-right
                roller_angle = math.pi / 4
            
            # Calculate wheel velocity
            wheel_velocity = (
                vx * math.cos(roller_angle) +
                vy * math.sin(roller_angle) +
                omega * (lx * math.sin(roller_angle) - ly * math.cos(roller_angle))
            )
            
            # Convert linear velocity to angular velocity (rad/s)
            wheel_angular_velocity = wheel_velocity / self.wheel_radius
            
            wheel_speeds.append(wheel_angular_velocity)
        
        return wheel_speeds
    
    def update_odometry(self):
        """Update robot odometry based on wheel speeds"""
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        
        # Get current wheel speeds (simplified - in real implementation, read from encoders)
        # For now, assume we have wheel angular velocities
        wheel_angular_velocities = [0.0, 0.0, 0.0, 0.0]  # Placeholder
        
        # Calculate robot velocities from wheel speeds
        vx, vy, omega = self.calculate_robot_velocity(wheel_angular_velocities)
        
        # Update position
        self.x += vx * dt * math.cos(self.theta) - vy * dt * math.sin(self.theta)
        self.y += vx * dt * math.sin(self.theta) + vy * dt * math.cos(self.theta)
        self.theta += omega * dt
        
        # Normalize angle
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))
        
        # Publish odometry
        self.publish_odometry(current_time, vx, vy, omega)
        
        self.last_time = current_time
    
    def calculate_robot_velocity(self, wheel_angular_velocities):
        """Calculate robot velocity from wheel angular velocities"""
        # Convert angular velocities to linear velocities
        wheel_linear_velocities = [
            omega * self.wheel_radius for omega in wheel_angular_velocities
        ]
        
        # Inverse kinematics matrix for mecanum wheels
        # This is a simplified version - real implementation would use proper matrix operations
        vx = (wheel_linear_velocities[0] + wheel_linear_velocities[1] + 
              wheel_linear_velocities[2] + wheel_linear_velocities[3]) / 4.0
        
        vy = (-wheel_linear_velocities[0] + wheel_linear_velocities[1] + 
               wheel_linear_velocities[2] - wheel_linear_velocities[3]) / 4.0
        
        omega = (-wheel_linear_velocities[0] + wheel_linear_velocities[1] - 
                 wheel_linear_velocities[2] + wheel_linear_velocities[3]) / (4.0 * self.robot_length)
        
        return vx, vy, omega
    
    def publish_odometry(self, current_time, vx, vy, omega):
        """Publish odometry message"""
        odometry = Odometry()
        odometry.header.stamp = current_time.to_msg()
        odometry.header.frame_id = "odom"
        odometry.child_frame_id = "base_link"
        
        # Position
        odometry.pose.pose.position.x = self.x
        odometry.pose.pose.position.y = self.y
        odometry.pose.pose.position.z = 0.0
        
        # Orientation
        quaternion = Quaternion()
        quaternion.x = 0.0
        quaternion.y = 0.0
        quaternion.z = math.sin(self.theta / 2.0)
        quaternion.w = math.cos(self.theta / 2.0)
        odometry.pose.pose.orientation = quaternion
        
        # Velocity
        odometry.twist.twist.linear.x = vx
        odometry.twist.twist.linear.y = vy
        odometry.twist.twist.angular.z = omega
        
        self.odometry_publisher.publish(odometry)

def main(args=None):
    rclpy.init(args=args)
    mecanum_controller = MecanumController()
    rclpy.spin(mecanum_controller)
    mecanum_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 📡 Communication Interface Implementation

### WebSocket Server

#### WebSocket Interface Implementation
```python
# src/paladin_interface/paladin_interface/websocket_server.py
import asyncio
import websockets
import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from paladin_msgs.msg import SystemStatus
import threading
import jwt
from datetime import datetime, timedelta

class PALadinWebSocketServer(Node):
    """WebSocket server for PAL-adin external communication"""
    
    def __init__(self):
        super().__init__('websocket_server')
        
        # WebSocket configuration
        self.host = '0.0.0.0'
        self.port = 8765
        self.clients = set()
        self.authenticated_clients = set()
        
        # JWT configuration
        self.jwt_secret = 'your-secret-key-change-in-production'
        self.token_expiry = timedelta(hours=24)
        
        # ROS2 publishers
        self.command_publisher = self.create_publisher(
            String, 'external_commands', 10
        )
        
        # ROS2 subscribers
        self.status_subscriber = self.create_subscription(
            SystemStatus, 'system_status', self.status_callback, 10
        )
        
        # Start WebSocket server in separate thread
        self.websocket_thread = threading.Thread(
            target=self.run_websocket_server,
            daemon=True
        )
        self.websocket_thread.start()
        
        self.get_logger().info("WebSocket Server initialized")
    
    def run_websocket_server(self):
        """Run WebSocket server"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        start_server = websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        loop.run_until_complete(start_server)
        loop.run_forever()
    
    async def handle_client(self, websocket, path):
        """Handle new WebSocket client connection"""
        self.clients.add(websocket)
        self.get_logger().info(f"Client connected: {websocket.remote_address}")
        
        try:
            async for message in websocket:
                await self.process_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.discard(websocket)
            self.authenticated_clients.discard(websocket)
            self.get_logger().info(f"Client disconnected: {websocket.remote_address}")
    
    async def process_message(self, websocket, message):
        """Process incoming message from client"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'authenticate':
                await self.handle_authentication(websocket, data)
            elif message_type == 'command':
                await self.handle_command(websocket, data)
            elif message_type == 'get_status':
                await self.handle_status_request(websocket)
            else:
                await self.send_error(websocket, "Unknown message type")
        
        except json.JSONDecodeError:
            await self.send_error(websocket, "Invalid JSON")
        except Exception as e:
            await self.send_error(websocket, str(e))
    
    async def handle_authentication(self, websocket, data):
        """Handle client authentication"""
        username = data.get('username')
        password = data.get('password')
        
        # Simple authentication - in production, use proper user database
        if username == 'paladin_user' and password == 'secure_password':
            # Generate JWT token
            token = self.generate_token(username)
            
            response = {
                'type': 'auth_response',
                'success': True,
                'token': token
            }
            
            await websocket.send(json.dumps(response))
            self.authenticated_clients.add(websocket)
            self.get_logger().info(f"Client authenticated: {websocket.remote_address}")
        else:
            response = {
                'type': 'auth_response',
                'success': False,
                'message': 'Invalid credentials'
            }
            await websocket.send(json.dumps(response))
    
    async def handle_command(self, websocket, data):
        """Handle command from authenticated client"""
        if websocket not in self.authenticated_clients:
            await self.send_error(websocket, "Not authenticated")
            return
        
        command = data.get('command')
        parameters = data.get('parameters', {})
        
        # Send command to ROS2 system
        command_msg = String()
        command_msg.data = json.dumps({
            'command': command,
            'parameters': parameters,
            'source': 'websocket',
            'timestamp': datetime.utcnow().isoformat()
        })
        
        self.command_publisher.publish(command_msg)
        
        # Send acknowledgment
        response = {
            'type': 'command_response',
            'success': True,
            'message': f"Command '{command}' sent to PAL-adin"
        }
        await websocket.send(json.dumps(response))
    
    async def handle_status_request(self, websocket):
        """Handle status request from client"""
        if websocket not in self.authenticated_clients:
            await self.send_error(websocket, "Not authenticated")
            return
        
        # Get current system status
        status = {
            'type': 'status_update',
            'timestamp': datetime.utcnow().isoformat(),
            'system_state': 'active',  # Placeholder
            'battery_level': 85.0,     # Placeholder
            'cpu_usage': 45.0,        # Placeholder
            'connected_clients': len(self.authenticated_clients)
        }
        
        await websocket.send(json.dumps(status))
    
    async def send_error(self, websocket, error_message):
        """Send error message to client"""
        error_response = {
            'type': 'error',
            'message': error_message
        }
        await websocket.send(json.dumps(error_response))
    
    def generate_token(self, username):
        """Generate JWT token for authenticated user"""
        payload = {
            'username': username,
            'exp': datetime.utcnow() + self.token_expiry,
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def status_callback(self, msg):
        """Handle system status updates"""
        # Broadcast status to all authenticated clients
        status_data = {
            'type': 'status_update',
            'timestamp': msg.timestamp.sec,
            'system_state': msg.state,
            'battery_level': msg.battery_level,
            'cpu_usage': msg.cpu_usage
        }
        
        asyncio.run_coroutine_threadsafe(
            self.broadcast_to_clients(status_data),
            asyncio.get_event_loop()
        )
    
    async def broadcast_to_clients(self, data):
        """Broadcast message to all authenticated clients"""
        if not self.authenticated_clients:
            return
        
        message = json.dumps(data)
        disconnected_clients = set()
        
        for client in self.authenticated_clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.authenticated_clients -= disconnected_clients

def main(args=None):
    rclpy.init(args=args)
    websocket_server = PALadinWebSocketServer()
    rclpy.spin(websocket_server)
    websocket_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## ⚙️ Configuration Files

### ROS2 Parameters

#### Mobility Parameters
```yaml
# config/ros_params/mobility_params.yaml
/mecanum_controller:
  ros__parameters:
    wheel_radius: 0.125  # meters
    robot_length: 0.6    # meters
    robot_width: 0.5     # meters
    max_linear_speed: 2.0  # m/s
    max_angular_speed: 1.5  # rad/s
    wheel_base: 0.4      # meters
    track_width: 0.5     # meters

/safety_controller:
  ros__parameters:
    min_obstacle_distance: 0.5  # meters
    critical_distance: 0.3      # meters
    max_speed: 2.0              # m/s
    max_angular_speed: 1.5      # rad/s
    emergency_stop_timeout: 5.0  # seconds
```

#### Manipulation Parameters
```yaml
# config/ros_params/manipulation_params.yaml
/arm_controller:
  ros__parameters:
    max_joint_speeds: [1.0, 1.0, 1.0, 2.0, 2.0, 3.0]  # rad/s
    max_joint_accelerations: [1.0, 1.0, 1.0, 2.0, 2.0, 3.0]  # rad/s²
    joint_limits:
      min: [-3.14, -1.57, -1.57, -3.14, -3.14, -3.14]  # radians
      max: [3.14, 1.57, 1.57, 3.14, 3.14, 3.14]  # radians

/gripper_controller:
  ros__parameters:
    max_opening: 0.15  # meters
    max_force: 50.0    # Newtons
    grasp_force: 10.0  # Newtons
    approach_distance: 0.1  # meters
```

### Launch Files

#### Main Launch File
```python
# config/launch/paladin_bringup.launch.py
import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os

def generate_launch_description():
    # Declare launch arguments
    config_dir = LaunchConfiguration('config_dir')
    
    return LaunchDescription([
        # Launch arguments
        DeclareLaunchArgument(
            'config_dir',
            default_value=os.path.join(
                os.getenv('PALADIN_DIR', ''),
                'config', 'ros_params'
            ),
            description='Path to configuration directory'
        ),
        
        # Executive controller
        Node(
            package='paladin_core',
            executable='executive_controller',
            name='executive_controller',
            output='screen',
            parameters=[os.path.join(config_dir, 'system_params.yaml')]
        ),
        
        # Safety controller
        Node(
            package='paladin_core',
            executable='safety_controller',
            name='safety_controller',
            output='screen',
            parameters=[os.path.join(config_dir, 'safety_params.yaml')]
        ),
        
        # Mobility controller
        Node(
            package='paladin_mobility',
            executable='mecanum_controller',
            name='mecanum_controller',
            output='screen',
            parameters=[os.path.join(config_dir, 'mobility_params.yaml')]
        ),
        
        # Manipulation controller
        Node(
            package='paladin_manipulation',
            executable='arm_controller',
            name='arm_controller',
            output='screen',
            parameters=[os.path.join(config_dir, 'manipulation_params.yaml')]
        ),
        
        # WebSocket server
        Node(
            package='paladin_interface',
            executable='websocket_server',
            name='websocket_server',
            output='screen'
        ),
    ])
```

---

## 🧪 Testing Framework

### Unit Tests

#### Safety Controller Tests
```python
# tests/unit_tests/test_safety_controller.py
import unittest
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32
from geometry_msgs.msg import Twist
from paladin_core.safety_controller import SafetyController, SafetyLevel
import time

class TestSafetyController(unittest.TestCase):
    """Test cases for Safety Controller"""
    
    @classmethod
    def setUpClass(cls):
        rclpy.init()
    
    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()
    
    def setUp(self):
        self.safety_controller = SafetyController()
        self.test_node = Node('test_node')
        
        # Test publishers
        self.emergency_button_publisher = self.test_node.create_publisher(
            Bool, 'emergency_button', 10
        )
        self.velocity_publisher = self.test_node.create_publisher(
            Twist, 'cmd_vel', 10
        )
        
        # Test subscribers
        self.safe_velocity_subscriber = self.test_node.create_subscription(
            Twist, 'safe_cmd_vel', self.velocity_callback, 10
        )
        self.emergency_stop_subscriber = self.test_node.create_subscription(
            Bool, 'emergency_stop', self.emergency_stop_callback, 10
        )
        
        self.received_velocity = None
        self.received_emergency_stop = None
    
    def tearDown(self):
        self.safety_controller.destroy_node()
        self.test_node.destroy_node()
    
    def velocity_callback(self, msg):
        self.received_velocity = msg
    
    def emergency_stop_callback(self, msg):
        self.received_emergency_stop = msg.data
    
    def test_emergency_button_trigger(self):
        """Test emergency button triggers emergency stop"""
        # Publish emergency button press
        emergency_msg = Bool()
        emergency_msg.data = True
        self.emergency_button_publisher.publish(emergency_msg)
        
        # Wait for processing
        time.sleep(0.2)
        rclpy.spin_once(self.safety_controller)
        
        # Check emergency stop was triggered
        self.assertEqual(self.safety_controller.safety_level, SafetyLevel.EMERGENCY)
        self.assertTrue(self.safety_controller.emergency_stop_active)
    
    def test_velocity_limiting(self):
        """Test velocity is limited to safe values"""
        # Publish high velocity command
        velocity_msg = Twist()
        velocity_msg.linear.x = 10.0  # Exceeds max speed
        velocity_msg.angular.z = 5.0  # Exceeds max angular speed
        self.velocity_publisher.publish(velocity_msg)
        
        # Wait for processing
        time.sleep(0.2)
        rclpy.spin_once(self.safety_controller)
        
        # Check velocity was limited
        if self.received_velocity:
            self.assertLessEqual(abs(self.received_velocity.linear.x), 2.0)
            self.assertLessEqual(abs(self.received_velocity.angular.z), 1.5)

if __name__ == '__main__':
    unittest.main()
```

---

## 🚀 Deployment Scripts

### System Setup Script
```bash
#!/bin/bash
# scripts/setup_environment.sh

set -e

echo "🚀 Setting up PAL-adin development environment..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Don't run this script as root"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install ROS2 Humble
echo "🤖 Installing ROS2 Humble..."
if ! command -v ros2 &> /dev/null; then
    sudo apt install software-properties-common -y
    sudo add-apt-repository universe -y
    sudo apt update && sudo apt install curl -y
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
    sudo sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
    sudo apt update
    sudo apt install ros-humble-desktop python3-argcomplete -y
else
    echo "✅ ROS2 Humble already installed"
fi

# Install development tools
echo "🛠️ Installing development tools..."
sudo apt install -y \
    git \
    cmake \
    build-essential \
    python3-pip \
    python3-venv \
    python3-dev \
    cppcheck \
    clang-format \
    code

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip3 install --user \
    numpy \
    scipy \
    opencv-python \
    pyyaml \
    colcon-common-extensions \
    rclpy \
    geometry-msgs \
    sensor-msgs \
    std-msgs

# Setup ROS2 environment
echo "🔧 Setting up ROS2 environment..."
if ! grep -q "source /opt/ros/humble/setup.bash" ~/.bashrc; then
    echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
fi

# Create workspace directory
echo "📁 Creating PAL-adin workspace..."
PALADIN_DIR="$HOME/paladin-physical"
if [ ! -d "$PALADIN_DIR" ]; then
    mkdir -p "$PALADIN_DIR/src"
    cd "$PALADIN_DIR"
    
    # Initialize colcon workspace
    colcon build --symlink-install
    
    echo "export PALADIN_DIR=$PALADIN_DIR" >> ~/.bashrc
    echo "source $PALADIN_DIR/install/setup.bash" >> ~/.bashrc
else
    echo "✅ PAL-adin workspace already exists"
fi

# Install udev rules for USB devices
echo "🔌 Setting up USB device rules..."
sudo tee /etc/udev/rules.d/99-paladin-usb.rules > /dev/null <<EOF
# PAL-adin USB devices
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", ATTRS{idProduct=="2303", MODE="0666"
EOF

sudo udevadm control --reload-rules && sudo udevadm trigger

echo "✅ PAL-adin development environment setup complete!"
echo "🔄 Please run: source ~/.bashrc"
echo "🚀 Then navigate to: cd \$PALADIN_DIR"
```

---

This implementation guide provides the practical foundation for beginning PAL-adin's physical body development. The code examples, configuration files, and setup scripts give you everything needed to start building the core systems that will bring PAL-adin to physical reality.

The modular approach allows you to develop and test each system independently before integrating them into the complete physical embodiment.