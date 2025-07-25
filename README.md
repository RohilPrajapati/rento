# Rento — Simple Electricity Billing Recording App

Rento is a minimal viable product (MVP) web app built with Django, designed to record and manage electricity billing for rentees. The app allows billing management, tracking payments on a monthly basis with Nepali calendar support.

---

## Features & Progress

- **User Authentication**  
  - Basic Django login/logout system to secure the app.

- **Rentee Management**  
  - Add and list rentees (people living in the household).

- **Billing Records**  
  - Create and view electricity billing records per rentee.  
  - Display months using the Nepali Bikram Sambat calendar.

- **Pagination**  
  - Pagination added for rentee list to handle multiple entries easily.

---

This app helps a single household track their electricity usage and payments for different rentees, with simple login protection and easy data management.


---

## TODO

- [ ] Develop reports/dashboard summarizing billing data for better insights.
- [ ] if posible create resuable component for pagination and tables

---

## User Stories

- As a user, I want to see which months a rentee has already paid for in the billing form, so I don’t create duplicate records.
- As a user, I want to generate reports that summarize electricity billing data, such as total consumption or unpaid bills.

---

## Installation & Setup (Optional)

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
4. Run migrations:  
   ```bash
   python manage.py migrate
5. Create a superuser to access the admin panel:  
   ```bash
   python manage.py createsuperuser
6. Start the development server:  
   ```bash
   python manage.py runserver
