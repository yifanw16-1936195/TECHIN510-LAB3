# TECHIN 510 Lab 3: Data Storage with Python

## Author: Yifan Wang

## Hosted Link

[Promptbase](https://techin510-lab-3-yifanwang.streamlit.app/)

## Overview

This lab involves creating a web app using Streamlit and PostgreSQL to manage ChatGPT prompts effectively. Users can create, retrieve, update, delete, and search for prompts in a database, making it a robust tool for managing and reusing ChatGPT prompts.

## Features

- **CRUD Operations**: Users can create, read, update, and delete prompts, allowing full management of content.
- **Search Functionality**: Prompts can be searched by title or content, making it easy to find relevant entries quickly.
- **Sorting and Filtering**: Users can sort prompts by date and filter them by favorites or date ranges (today, this week, this month, this year).
- **Favorite System**: Prompts can be marked as favorites, enabling users to quickly access preferred entries.
- **Responsive UI**: Using Streamlit, the app provides a responsive and intuitive user interface for interacting with prompt data.

## Reflections

1. **Database Integration and Management**: Integrating PostgreSQL with Python required proper configuration and understanding of database operations, ensuring robust data management capabilities.
2. **Form Validation and Error Handling**: Implementing form validation in Streamlit helped in maintaining data integrity and enhancing user experience. Learning to manage errors effectively, especially related to database connectivity, was crucial.
3. **Enhancing UX with Advanced Features**: Adding features like sorting, filtering, and marking favorites involved more complex SQL queries and Streamlit functionalities. These features significantly improved the usability and functionality of the app.
4. **Environmental Variables for Security**: Using `.env` files to manage sensitive information like database URLs helped in securing the app's configuration settings.
