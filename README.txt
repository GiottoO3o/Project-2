### Health and Fitness App

1. Overview
Welcome to the Health and Fitness App! This application is designed to help users manage their fitness routines, schedule personal training sessions, join group fitness classes, track their health metrics, manage equipment, and handle billing and payments.

2. Features
1) User Management:
- Members: Users can sign up as members to access various features of the app.
- Trainers: Certified trainers can register and offer personal training sessions and group fitness classes.

2) Booking and Scheduling:
- Personal Training Sessions: Members can schedule one-on-one training sessions with certified trainers.
- Group Fitness Classes: Members can sign up for group fitness classes led by trainers.

3) Health Tracking:
- Fitness Metrics: Users can track their weight, exercise routines, and other health metrics over time.

4) Equipment Management:
- Equipment Status: Admins can manage the status of equipment, marking them as available or in use.

5) Billing and Payments:
- Billing: Members receive bills for their booked sessions and classes.
- Payments: Members can make payments for their bills through the app



## Setup Instructions

### 1. PostgreSQL Database Setup

#### 1.1 Installation

- Download and install PostgreSQL from the official website: [PostgreSQL Downloads](https://www.postgresql.org/download/).


## 1.2 PostgreSQL Server Setup

To start the PostgreSQL server, follow these steps:

1. Open Command Prompt as administrator.
2. Navigate to the PostgreSQL installation directory:

    ```shell
    cd C:\Program Files\PostgreSQL\{version}\bin
    ```

3. Type the following command to start the server:

    ```shell
    pg_ctl.exe -D "../data" start 
   
    ```

4. Once the server has started, open the pgAdmin4 panel and add a server using the default credentials:

    - Username: postgres
    - Password: fast



Youtube link: https://youtu.be/yLdf_YUlEdY
