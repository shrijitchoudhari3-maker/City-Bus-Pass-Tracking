# 🚌 CITYPULSE — Smart City Bus Pass & Tracking System

### 🚀 Transforming Everyday Public Transportation into a Smarter, Faster & More Connected Experience.

**CityPulse** is a smart, web-based public transportation management platform designed to simplify the way passengers access bus services. It brings digital bus passes, intelligent route discovery, QR-based pass verification, simulated GPS tracking, delay notifications, and administrative reporting together in one unified application.

Built using **Python and Streamlit**, CityPulse aims to reduce manual processes, improve passenger convenience, and demonstrate how technology can make public transportation more accessible, efficient, and transparent.

> **One Platform. Smarter Mobility. Better Journeys.**

---

## 🌟 Project Overview

Imagine applying for a bus pass without standing in a queue, checking your pass digitally instead of carrying a physical card, and viewing a bus's estimated arrival information from one platform.

That's the idea behind **CityPulse**.

The system provides separate passenger and administrative functionality. Passengers can register, log in, explore routes, apply for digital passes, and view their pass information. QR-based verification helps demonstrate pass authentication, while a simulated bus-tracking module displays bus movement, status, and estimated arrival information.

Administrators can manage records and access reports through a centralized dashboard.

---

## ✨ Key Features

### 🔐 1. Secure User Authentication
- User registration and login.
- Account-based access to application features.
- Input validation and error handling.
- Separate passenger and administrator functionality.

### 🗺️ 2. Smart Bus Route Discovery
- Search available bus routes.
- View route information and journey details.
- Explore route options before applying for a pass.

### 🎫 3. Digital Bus Pass Generation
- Apply for a digital bus pass.
- Select a route and validity period.
- View the calculated pass price before generation.
- Support for 7-day, 30-day, and 90-day passes.
- View generated passes in the My Bus Passes section.
- Store the final pass amount with the pass record.

### 💰 4. Intelligent Pass Pricing
- Route-based fare calculation.
- Different pricing according to pass duration.
- Suggested discounts for longer validity periods.
- Transparent price preview before pass generation.
- Saved pricing information available with the generated pass.

### 📱 5. QR Code Pass Validation
- QR-based digital pass verification.
- Demonstration of valid pass validation.
- Detection of expired passes.
- Handling of invalid pass information.

### 📍 6. Smart Bus Tracking — Simulated GPS
- Display simulated bus locations.
- Visualize bus movement on the tracking interface.
- Show Running, Stopped, and Offline statuses.
- Display estimated arrival time (ETA).
- Show last-updated tracking information.
- Automatic refresh for tracking updates.

**Note:** The current version uses simulated GPS data to demonstrate bus movement and tracking functionality. Actual vehicle GPS integration through Firebase and driver-device location sharing is planned as a future enhancement.

### 🔔 7. Delay Alerts & Notifications
- Display simulated bus delay notifications.
- Inform passengers about possible service delays.
- Demonstrate how a notification system can improve passenger awareness.

### 📊 8. Admin Dashboard & Reporting
- Administrative access to application records.
- Manage and review digital bus pass records.
- View system-related reports.
- Support centralized monitoring of application data.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web application |
| SQLite | Database management |
| Pandas | Data handling and analysis |
| QR Code | Digital pass verification |
| GPS Simulation | Demonstration of bus tracking |
| Git & GitHub | Version control and collaboration |
| Pytest | Automated testing |

---

## 🏗️ System Architecture

The application follows a simple modular architecture:

```text
              PASSENGER / ADMIN
                      |
                      ▼
              STREAMLIT INTERFACE
                      |
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     AUTHENTICATION  ROUTES   DIGITAL PASSES
          |           |           |
          └───────────┼───────────┘
                      |
                      ▼
               APPLICATION LOGIC
                      |
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
   QR VALIDATION  BUS TRACKING   DELAY ALERTS
       |              |              |
       └──────────────┼──────────────┘
                      |
                      ▼
                 SQLITE DATABASE
                      |
                      ▼
              ADMIN & REPORTING
```

---

## ⚙️ Installation & Setup

Follow these steps to run CityPulse on your local machine.

### Step 1: Clone the Repository

```bash
git clone https://github.com/shrijitchoudhari3-maker/City-Bus-Pass-And-Tracking-System.git
```

### Step 2: Open the Project Folder

```bash
cd City-Bus-Pass-And-Tracking-System
```

### Step 3: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python -m streamlit run app.py
```

### Step 6: Open in Your Browser

```text
http://localhost:8501
```

The CityPulse application should now be running locally.

---

## 🧪 Testing & Quality Assurance

The project includes testing and validation activities designed to check important application workflows.

| Test Case | Expected Result |
|---|---|
| User registration | Account created with valid details |
| User login | Authorized login succeeds |
| Route search | Relevant route information displayed |
| Digital pass generation | Pass generated with correct pricing |
| Valid QR pass | Pass accepted |
| Expired QR pass | Expired status displayed |
| Invalid QR pass | Invalid status displayed |
| Bus tracking | Simulated location and status displayed |
| Delay notification | Simulated delay information displayed |

Run automated tests, if the test suite is included:

```bash
python -m pytest -v
```

---

## 🔄 Agile Development Methodology

CityPulse is developed using an Agile-inspired workflow.

The project work is organized into three proposed development sprints:

- **Sprint 1 — Foundation:** Requirements, authentication, database setup, and route discovery.
- **Sprint 2 — Digital Services:** Digital passes, route-based pricing, and QR verification.
- **Sprint 3 — Smart Mobility:** Simulated GPS tracking, ETA, delay alerts, admin reporting, testing, and deployment.

Project activities are organized using Trello, with tasks, acceptance criteria, and a shared Definition of Done.

---

## 🔮 Future Enhancements

CityPulse has been designed with opportunities for further development:

- 📡 Real-time vehicle GPS integration using Firebase Realtime Database.
- 📱 Driver-side mobile application for sharing live bus coordinates.
- 🧠 AI-powered arrival time prediction.
- 🔔 Push notifications for route changes and delays.
- 💳 Online payment gateway integration.
- ☁️ Cloud database integration for reliable persistent storage.
- 📈 Advanced passenger analytics and reporting.
- 🌐 Multi-city and multi-operator support.

---

## 🎯 Project Objectives

- Digitize the traditional bus pass application process.
- Make route information easier to access.
- Demonstrate QR-based digital pass verification.
- Improve passenger awareness through tracking and delay information.
- Simplify administrative monitoring and reporting.
- Explore how software technologies can support smarter public transportation.

---

## 👨‍💻 Development & Project Information

**Project Name:** CityPulse — Smart City Bus Pass & Tracking System

**Project Domain:** Smart Transportation / Web Application Development

**Development Type:** Academic Software Development Project

**Framework:** Streamlit

**Language:** Python

**Version Control:** GitHub

**Project Management:** Trello

---

## 💡 Why CityPulse?

Public transportation is an essential part of urban life, but traditional processes can be time-consuming and inconvenient.

CityPulse explores how digital technology can bring multiple transportation services into one accessible platform.

From digital bus passes to QR verification and simulated bus tracking, the project demonstrates a practical approach to building a more connected public transportation experience.

**The vision is simple: make every journey smarter, every pass digital, and every passenger better informed.**

---

### ⭐ If you find this project interesting, consider giving the repository a star!

**Built with Python, powered by innovation, and designed for smarter mobility.**

`#Python` `#Streamlit` `#SmartTransportation` `#DigitalBusPass` `#GPS` `#QRValidation` `#AgileDevelopment` `#SoftwareEngineering`

Streamlit URL: https://city-bus-pass-tracking-nyzsrxdxebv3ftpyt3bxvv.streamlit.app/
