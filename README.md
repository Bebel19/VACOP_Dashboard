# VACOP - Open-Source, Plug & Play Connected Autonomous Vehicle

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)
[![Français](https://img.shields.io/badge/lang-Français-red.svg)](README.fr.md)

The **VACOP** project (**Open-Source, Plug & Play Connected Autonomous Vehicle**) aims to develop a connected autonomous navigation platform on the autOCampus campus at IRIT. The goal is to enable the vehicle to navigate safely within a controlled environment, while providing real-time supervision and control through a dedicated web interface and a private 5G infrastructure.

This project is part of IRIT’s research and experimentation activities in autonomous mobility, as well as the SRI 2026 engineering program.

---

## Main Features

The VACOP system is designed around four main modules:

* **Localization and State Estimation:**
    * Centimeter-level geolocation accuracy (2–3 cm) using an RTK GNSS receiver (u-blox ZED-F9P).
    * Robust data fusion using an Extended Kalman Filter, combining GNSS and odometry data from Hall-effect sensors to maintain position estimation even in case of GNSS signal loss.

* **Perception and Environment Understanding:**
    * SLAM mapping and continuous localization using a 3D LiDAR sensor (Robosense Helios 16P).
    * Detection and classification of static and dynamic obstacles, such as pedestrians and vehicles, through LiDAR and camera data fusion (RGB and RGB-D).
    * Generation of a dynamic costmap for navigation.

* **Trajectory Planning:**
    * Global planning to compute the optimal route toward a target destination.
    * Local planning for real-time obstacle avoidance and risk-aware adaptation, including collision and pedestrian-related risks.
    * Closed-loop control of actuators, including motors, steering, and braking.

* **Communication and Supervision Interface:**
    * Web-based supervision interface built with React and Flask for remote control and visualization.
    * **Autonomous Mode:** Mission planning, either immediate or scheduled, by selecting a destination on the map.
    * **Teleoperation Mode:** Remote manual control of the vehicle using a gamepad.
    * **Real-Time Visualization:** Display of video streams, vehicle position, logs, and obstacle maps.

---

## System Architecture

The architecture is built on **ROS 2** and organized around three main components, connected through a private 5G network.

1. **Vehicle — Onboard System:**
    * **Main computing unit:** NVIDIA Jetson Orin NX for sensor fusion, perception, and planning.
    * **Sensors:** LiDAR, RGB/RGB-D cameras, RTK GNSS, Hall-effect sensors for odometry.
    * **Communication:** Telit 5G module for telemetry and NTRIP corrections.
    * **Low-level control:** Raspberry Pi and SOLO MEGA motor controllers.

2. **Servers — IRIT Infrastructure:**
    * **Backend (C2):** A **Flask** application handling business logic, the REST API, WebSockets for real-time data, and authentication.
    * **Database (C2):** **PostgreSQL** for storing users, missions, and log history.
    * **Deployment:** The entire supervision stack (C1 + C2) is containerized with **Docker**.

3. **Client — Operator Interface:**
    * **Frontend (C1):** A secure **React** web interface using HTTPS, allowing the operator to supervise and control the vehicle.
    * **Protocols:** HTTPS, WebSocket, and WebRTC for video streaming.
