DROP SCHEMA IF EXISTS lincolngroup1$leave_system;
CREATE SCHEMA lincolngroup1$leave_system;
USE lincolngroup1$leave_system;


CREATE TABLE roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(20) NOT NULL
);


CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    user_name VARCHAR(30) NOT NULL,
    pwd VARCHAR(512) NOT NULL,
    salt VARCHAR(128) NULL,
    token VARCHAR(32) NULL,
    is_active BOOLEAN DEFAULT 1,
    CONSTRAINT user_role_role_id_fk FOREIGN KEY (role_id)
        REFERENCES roles (role_id)
);


CREATE TABLE department (
    dept_code VARCHAR(10) PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);


CREATE TABLE employee (
    emp_id INT PRIMARY KEY UNIQUE,
    dept_code VARCHAR(10) NOT NULL,
    title VARCHAR(30) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    joined_date DATE NOT NULL,
    position_title VARCHAR(30) NOT NULL,
    position_start_date DATE NOT NULL,
    email VARCHAR(30) NOT NULL,
    report_to INT NULL,
    approval_manager INT NULL,
    CONSTRAINT employee_user_user_id_fk FOREIGN KEY (emp_id)
        REFERENCES users (user_id),
    CONSTRAINT employee_department_dept_code_fk FOREIGN KEY (dept_code)
        REFERENCES department (dept_code),
    CONSTRAINT report_to_fk FOREIGN KEY (report_to)
        REFERENCES employee (emp_id),
    CONSTRAINT approval_fk FOREIGN KEY (approval_manager)
        REFERENCES employee (emp_id)
);

CREATE TABLE holiday (
    holiday_id INT AUTO_INCREMENT PRIMARY KEY,
    holiday_name VARCHAR(30) NOT NULL,
    holiday_year INT NOT NULL,
    holiday_month INT NOT NULL,
    holiday_day INT NOT NULL,
    edit_by INT NOT NULL,
    edit_date DATETIME NOT NULL,
    is_active BOOLEAN NOT NULL,
    CONSTRAINT holiday_employee_emp_id_fk FOREIGN KEY (edit_by)
        REFERENCES employee (emp_id)
);



CREATE TABLE leave_type (
    leave_code VARCHAR(10) PRIMARY KEY,
    leave_name VARCHAR(30) NOT NULL,
    leave_per_year DECIMAL(10 , 2 ) DEFAULT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);


CREATE TABLE request_status (
    status_id INT AUTO_INCREMENT PRIMARY KEY,
    status_name VARCHAR(20) NOT NULL
);


CREATE TABLE leave_request (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    leave_code VARCHAR(10) NOT NULL,
    emp_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status_id INT NOT NULL,
    used BOOLEAN NOT NULL,
    note VARCHAR(100) NULL,
    created_on DATETIME NOT NULL,
    CONSTRAINT leave_request_employee_emp_id_fk FOREIGN KEY (emp_id)
        REFERENCES employee (emp_id),
    CONSTRAINT leave_request_leave_type_leave_type_id_fk FOREIGN KEY (leave_code)
        REFERENCES leave_type (leave_code),
    CONSTRAINT leave_request_request_status_status_id_fk FOREIGN KEY (status_id)
        REFERENCES request_status (status_id)
);


CREATE TABLE leave_decision (
    request_id INT,
    decision_made_by INT NOT NULL,
    decision_created_on DATETIME NOT NULL,
    status_id INT NOT NULL,
    comment VARCHAR(100) NULL,
    PRIMARY KEY (request_id , decision_created_on),
    CONSTRAINT leave_decision_employee_emp_id_fk FOREIGN KEY (decision_made_by)
        REFERENCES employee (emp_id),
    CONSTRAINT leave_decision_leave_request_request_id_fk FOREIGN KEY (request_id)
        REFERENCES leave_request (request_id),
    CONSTRAINT leave_decision_request_status_status_id_fk FOREIGN KEY (status_id)
        REFERENCES request_status (status_id)
);


CREATE TABLE leave_balance (
    emp_id INT,
    al_balance DECIMAL(10 , 2 ) NOT NULL,
    sl_balance DECIMAL(10 , 2 ) NOT NULL,
    updated_on DATETIME NOT NULL,
    PRIMARY KEY (emp_id , updated_on),
    CONSTRAINT leave_balance_employee_emp_id_fk FOREIGN KEY (emp_id)
        REFERENCES employee (emp_id)
);

CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    recipient_id INT NOT NULL,
    request_id INT NOT NULL,
    message VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_status BOOLEAN DEFAULT FALSE,
    CONSTRAINT notifications_employee_sender_id_fk FOREIGN KEY (sender_id)
        REFERENCES employee (emp_id),
    CONSTRAINT notifications_employee_recipient_id_fk FOREIGN KEY (recipient_id)
        REFERENCES employee (emp_id),
    CONSTRAINT notifications_leave_request_request_id_fk FOREIGN KEY (request_id)
        REFERENCES leave_request (request_id)
);



INSERT INTO department (dept_code, dept_name) VALUES
('DCS', 'Department of Corporate Services'),
('DEM', 'Department of Environmental Management'),
('DWEMB', 'Department of Wine, Food and Molecular Biosciences'),
('DPMC', 'Department of Pest-Management and Conservation'),
('DTSS', 'Department of Tourism, Sport and Society'),
('DFBS','Department of Financial and Business Systems'),
('DLMS', 'Department of Land Management and Systems'),
('DGVCT', 'Department of Global Value Chains and Trade');

INSERT INTO roles (role_name) VALUES
('Employee'),
('Approval Manager'),
('Admin');




INSERT INTO users (user_id, role_id, user_name, pwd, salt, token, is_active) VALUES
(1, 2, 'lily.brown@lincoln.ac.nz', 'ejohohoew9', null, null, 1),
(2, 2, 'david.green@lincoln.ac.nz', 'dkhh80&5', null, null, 1),
(3, 3, 'chris.epke@lincoln.ac.nz', 'greo087%', null, null, 1),
(4, 3, 'john.smith@lincoln.ac.nz', 'bieiowo0@', null, null, 1),
(5, 3, 'emily.johnson@lincoln.ac.nz', 'siweolz@1', null, null, 1),
(6, 1, 'michael.davis@lincoln.ac.nz', 'iwieooi$2', null, null, 1),
(7, 1, 'sophia.wilson@lincoln.ac.nz', 'hwoaap#8', null, null, 1),
(8, 1, 'daniel.taylor@lincoln.ac.nz', 'kowgagzu%3', null, null, 1),
(9, 2, 'olivia.anderson@lincoln.ac.nz', 'aewioh45#', null, null, 1),
(10, 1, 'matthew.thomas@lincoln.ac.nz', 'koea95@^', null, null, 1),
(11, 1, 'chloe.roberts@lincoln.ac.nz', 'jlko68!$', null, null, 1),
(12, 1, 'ethan.clark@lincoln.ac.nz', 'geaopq&4', null, null, 1),
(13, 2, 'emma.walker@lincoln.ac.nz', 'kaweu78^%', null, null, 1),
(14, 1, 'james.hill@lincoln.ac.nz', 'dhaepo@5', null, null, 1),
(15, 1, 'mia.baker@lincoln.ac.nz', 'wieho02#$', null, null, 1),
(16, 2, 'abigail.parker@lincoln.ac.nz', 'kie34&^*', null, null, 1),
(17, 1, 'benjamin.carter@lincoln.ac.nz', 'hjaep86@$', null, null, 1),
(18, 1, 'grace.turner@lincoln.ac.nz', 'aleiop$7!', null, null, 1),
(19, 1, 'henry.cooper@lincoln.ac.nz', 'weio43&^', null, null, 1),
(20, 1, 'sofia.lewis@lincoln.ac.nz', 'qweap92@$', null, null, 1),
(21, 1, 'jacob.gonzalez@lincoln.ac.nz', 'eipok43#*', null, null, 1),
(22, 1, 'ava.hernandez@lincoln.ac.nz', 'alop92@&$', null, null, 1),
(23, 2, 'william.parker@lincoln.ac.nz', 'aeiop29@&', null, null, 1),
(24, 2, 'samantha.carter@lincoln.ac.nz', 'kiop34^*', null, null, 1),
(25, 2, 'joseph.cooper@lincoln.ac.nz', 'oapq92&^', null, null, 1),
(26, 2, 'natalie.ross@lincoln.ac.nz', 'kwoi85@#$', null, null, 1),
(27, 1, 'jonathan.roberts@lincoln.ac.nz', 'lkhg76#$', null, null, 1),
(28, 1, 'isabella.wright@lincoln.ac.nz', 'poiuy63*$', null, null, 1),
(29, 1, 'joshua.jackson@lincoln.ac.nz', 'qazws19@#', null, null, 1),
(30, 1, 'sophie.turner@lincoln.ac.nz', 'mnbvc27^*', null, null, 1),
(31, 1, 'daniel.lee@lincoln.ac.nz', 'zxcvb51&^', null, null, 1),
(32, 1, 'mila.gonzalez@lincoln.ac.nz', 'asdfg93@#$', null, null, 1),
(33, 1, 'david.hernandez@lincoln.ac.nz', 'hjklp25^*', null, null, 1),
(34, 1, 'avery.cooper@lincoln.ac.nz', 'ertyu38@#$', null, null, 1);

INSERT INTO employee (emp_id, dept_code, title, first_name, last_name, gender, joined_date, position_title, position_start_date, email, report_to, approval_manager) VALUES
(1, 'DCS', 'Doctor', 'Lily', 'Brown', 'Female', '2020-05-01', 'Vice-Chancellor', '2020-05-01', 'lily.brown@lincoln.ac.nz', null, null),
(2, 'DCS', 'Mr', 'David', 'Green', 'Male', '2017-07-03', 'Finance Director', '2018-05-07', 'david.green@lincoln.ac.nz', 1, null),
(3, 'DCS', 'Mr', 'Chris', 'Epke', 'Male', '2014-07-03', 'HR Director', '2014-07-03', 'chris.epke@lincoln.ac.nz', 1, null),
(4, 'DCS', 'Doctor', 'John', 'Smith', 'Male', '2019-03-15', 'HR Director', '2019-03-15', 'john.smith@lincoln.ac.nz', 1, 3),
(5, 'DCS', 'Ms', 'Emily', 'Johnson', 'Female', '2016-09-10', 'Technology Director', '2016-09-10', 'emily.johnson@lincoln.ac.nz', 1, 4),
(6, 'DCS', 'Mr', 'Michael', 'Davis', 'Male', '2018-02-28', 'Technology Employee', '2018-02-28', 'michael.davis@lincoln.ac.nz', 5, 5),
(7, 'DCS', 'Ms', 'Sophia', 'Wilson', 'Female', '2020-11-20', 'Finance Employee', '2020-11-20', 'sophia.wilson@lincoln.ac.nz', 2, 2),
(8, 'DCS', 'Mr', 'Daniel', 'Taylor', 'Male', '2015-06-12', 'HR Employee', '2015-06-12', 'daniel.taylor@lincoln.ac.nz', 4, 4),
(9, 'DLMS', 'Doctor', 'Olivia', 'Anderson', 'Female', '2017-12-09', 'Professor', '2018-01-05', 'olivia.anderson@lincoln.ac.nz', 3, 3),
(10, 'DLMS', 'Mr', 'Matthew', 'Thomas', 'Male', '2016-04-25', 'Lecturer', '2016-04-25', 'matthew.thomas@lincoln.ac.nz', 9, 9),
(11, 'DLMS', 'Ms', 'Chloe', 'Roberts', 'Female', '2018-08-18', 'Tutor', '2018-08-18', 'chloe.roberts@lincoln.ac.nz', 10, 9),
(12, 'DLMS', 'Mr', 'Ethan', 'Clark', 'Male', '2021-01-07', 'Tutor', '2021-01-07', 'ethan.clark@lincoln.ac.nz', 10, 9),
(13, 'DEM', 'Professor', 'Emma', 'Walker', 'Female', '2019-05-03', 'Professor', '2019-05-03', 'emma.walker@lincoln.ac.nz', 3, 3),
(14, 'DEM', 'Mr', 'James', 'Hill', 'Male', '2017-10-28', 'Lecturer', '2018-01-02', 'james.hill@lincoln.ac.nz', 13, 13),
(15, 'DEM', 'Ms', 'Mia', 'Baker', 'Female', '2016-08-14', 'Tutor', '2016-08-14', 'mia.baker@lincoln.ac.nz', 14, 13),
(16, 'DFBS', 'Professor', 'Abigail', 'Parker', 'Female', '2019-09-22', 'Professor', '2019-09-22', 'abigail.parker@lincoln.ac.nz', 3, 3),
(17, 'DFBS', 'Mr', 'Benjamin', 'Carter', 'Male', '2018-12-17', 'Lecturer', '2018-12-17', 'benjamin.carter@lincoln.ac.nz', 16, 16),
(18, 'DFBS', 'Ms', 'Grace', 'Turner', 'Female', '2021-04-11', 'Lecturer', '2021-04-11', 'grace.turner@lincoln.ac.nz', 16, 16),
(19, 'DFBS', 'Mr', 'Henry', 'Cooper', 'Male', '2017-11-08', 'Tutor', '2017-11-08', 'henry.cooper@lincoln.ac.nz', 17, 16),
(20, 'DFBS', 'Ms', 'Sofia', 'Lewis', 'Female', '2016-07-01', 'Tutor', '2016-07-01', 'sofia.lewis@lincoln.ac.nz', 17, 16),
(21, 'DFBS', 'Mr', 'Jacob', 'Gonzalez', 'Male', '2019-02-14', 'Tutor', '2019-02-14', 'jacob.gonzalez@lincoln.ac.nz', 18, 16),
(22, 'DFBS', 'Ms', 'Ava', 'Hernandez', 'Female', '2017-10-09', 'Tutor', '2017-10-09', 'ava.hernandez@lincoln.ac.nz', 18, 16),
(23, 'DWEMB', 'Professor', 'William', 'Parker', 'Male', '2017-05-14', 'Professor', '2017-05-14', 'william.parker@lincoln.ac.nz', 3, 3),
(24, 'DPMC', 'Professor', 'Samantha', 'Carter', 'Female', '2019-01-11', 'Professor', '2019-01-11', 'samantha.carter@lincoln.ac.nz', 3, 3),
(25, 'DTSS', 'Professor', 'Joseph', 'Cooper', 'Male', '2018-11-28', 'Professor', '2018-11-28', 'joseph.cooper@lincoln.ac.nz', 3, 3),
(26, 'DGVCT', 'Professor', 'Natalie', 'Ross', 'Female', '2017-08-07', 'Professor', '2017-08-07', 'natalie.ross@lincoln.ac.nz', 3, 3),
(27, 'DWEMB', 'Mr', 'Jonathan', 'Roberts', 'Male', '2020-03-02', 'Lecturer', '2020-03-02', 'jonathan.roberts@lincoln.ac.nz', 23, 23),
(28, 'DPMC', 'Ms', 'Isabella', 'Wright', 'Female', '2017-12-08', 'Lecturer', '2017-12-08', 'isabella.wright@lincoln.ac.nz', 24, 24),
(29, 'DTSS', 'Mr', 'Joshua', 'Jackson', 'Male', '2021-01-19', 'Lecturer', '2021-01-19', 'joshua.jackson@lincoln.ac.nz', 25, 25),
(30, 'DGVCT', 'Ms', 'Sophie', 'Turner', 'Female', '2018-06-14', 'Lecturer', '2018-06-14', 'sophie.turner@lincoln.ac.nz', 26, 26),
(31, 'DWEMB', 'Mr', 'Daniel', 'Lee', 'Male', '2017-09-02', 'Tutor', '2017-09-02', 'daniel.lee@lincoln.ac.nz', 27, 23),
(32, 'DPMC', 'Ms', 'Mila', 'Gonzalez', 'Female', '2022-03-19', 'Tutor', '2022-03-19', 'mila.gonzalez@lincoln.ac.nz', 28, 24),
(33, 'DTSS', 'Mr', 'David', 'Hernandez', 'Male', '2019-07-28', 'Tutor', '2019-07-28', 'david.hernandez@lincoln.ac.nz', 29, 25),
(34, 'DGVCT', 'Ms', 'Avery', 'Cooper', 'Female', '2016-10-05', 'Tutor', '2016-10-05', 'avery.cooper@lincoln.ac.nz', 30, 26);


UPDATE employee
SET
    approval_manager = 2
WHERE
    emp_id = 1;

UPDATE employee
SET
    approval_manager = 4
WHERE
    emp_id = 2;

UPDATE employee
SET
    approval_manager = 4
WHERE
    emp_id = 3;

INSERT INTO holiday (holiday_id, holiday_name, holiday_year, holiday_month, holiday_day, edit_by, edit_date, is_active) VALUES
(1, 'New Year', 2022, 1, 1, 6, '2022-11-08 21:26:13', 1),
(2, 'Day After New Year', 2022, 1, 2, 6, '2022-11-08 21:26:13', 1),
(3, 'Observed New Year', 2022, 1, 3, 6, '2022-11-08 21:26:13', 1),
(4, 'Observed Day After New Year', 2022, 1, 4, 6, '2022-11-08 21:26:13', 1),
(5, 'Waitangi Day', 2022, 2, 6, 6, '2022-11-08 21:26:13', 1),
(6, 'Obeserved Waitangi Day', 2022, 2, 7, 6, '2022-11-08 21:26:13', 1),
(7, 'Good Friday', 2022, 4, 15, 6, '2022-11-08 21:26:13', 1),
(8, 'Easter Monday', 2022, 4, 18, 6, '2022-11-08 21:26:13', 1),
(9, 'ANZAC Day', 2022, 4, 25, 6, '2022-11-08 21:26:13', 1),
(10, 'Queen\'s Birthday', 2022, 6, 6, 6, '2022-11-08 21:26:13', 0),
(11, 'Matariki', 2022, 6, 24, 6, '2022-11-08 21:26:13', 1),
(12, 'Labour Day', 2022, 10, 24, 6, '2022-11-08 21:26:13', 1),
(13, 'Christmas Day', 2022, 12, 25, 6, '2023-01-08 21:26:13', 1),
(14, 'Boxing Day', 2022, 12, 26, 6, '2023-01-08 21:26:13', 1),
(15, 'Observed Christmas Day', 2022, 12, 27, 6, '2023-01-08 21:26:13', 1),
(16, 'New Year', 2023, 1, 1, 6, '2023-05-08 21:26:13', 1),
(17, 'Day After New Year', 2023, 1, 2, 6, '2023-05-08 21:26:13', 1),
(18, 'Observed New Year ', 2023, 1, 3, 6, '2023-05-08 21:26:13', 1),
(19, 'Waitangi Day', 2023, 2, 6, 6, '2023-05-08 21:26:13', 1),
(20, 'Good Friday', 2023, 4, 7, 6, '2023-05-08 21:26:13', 1),
(21, 'Easter Monday', 2023, 4, 10, 6, '2023-05-08 21:26:13', 1),
(22, 'ANZAC Day', 2023, 4, 25, 6, '2023-05-08 21:26:13', 1),
(23, 'King\'s Birthday', 2023, 6, 5, 6, '2022-11-08 21:26:13', 1),
(24, 'Matariki', 2023, 7, 14, 6, '2022-11-08 21:26:13', 1),
(25, 'Labour Day', 2023, 10, 23, 6, '2022-11-08 21:26:13', 1),
(26, 'Chrismas Day', 2023, 12, 25, 6, '2022-11-08 21:26:13', 1),
(27, 'Boxing Day', 2023, 12, 26, 6, '2022-11-08 21:26:13', 1),

(28, 'New Year', 2024, 1, 1, 6, '2022-11-08 21:26:13', 1),
(29, 'Day After New Year', 2024, 1, 2, 6, '2022-11-08 21:26:13', 1),
(30, 'Waitangi Day', 2024, 2, 6, 6, '2022-11-08 21:26:13', 1),
(31, 'Good Friday', 2024, 3, 29, 6, '2022-11-08 21:26:13', 1),
(32, 'Easter Monday', 2024, 4, 1, 6, '2022-11-08 21:26:13', 1),
(33, 'ANZAC Day', 2024, 4, 25, 6, '2022-11-08 21:26:13', 1),
(34, 'King\'s Birthday', 2024, 6, 3, 6, '2022-11-08 21:26:13', 1),
(35, 'Matariki', 2024, 6, 28, 6, '2022-11-08 21:26:13', 1),
(36, 'Labour Day', 2024, 10, 28, 6, '2022-11-08 21:26:13', 1),
(37, 'Christmas Day', 2024, 12, 25, 6, '2022-11-08 21:26:13', 1),
(38, 'Boxing Day', 2024, 12, 26, 6, '2022-11-08 21:26:13', 1);




INSERT INTO leave_type (leave_code, leave_name, leave_per_year) VALUES
('AL', 'Annual Leave', 225),
('BL', 'Bereavement Leave', null),
('PL', 'Parental Leave', null),
('SFL', 'Sick Family Leave', null),
('SL', 'Sick Leave', 37.5),
('SLnoP', 'Special Leave without Pay', null),
('SLwP', 'Special leave with Pay', null);


INSERT INTO request_status (status_name) VALUES
('Unsubmitted'),
('Submitted'),
('Approved'),
('Rejected'),
('Deleted'),
('Cancelled');

INSERT INTO leave_request (request_id, created_on, leave_code, emp_id, start_date, end_date, status_id, used, note) VALUES
(1, '2014-12-12 09:45:00', 'AL', 3, '2014-12-15', '2014-12-19', 3, 1, null),
(2, '2015-01-26 11:10:00', 'AL', 3, '2015-01-27', '2015-01-27', 3, 1, null),
(3, '2015-03-09 13:25:00', 'AL', 3, '2015-03-10', '2015-03-12', 3, 1, null),
(4, '2017-08-11 11:45:00', 'AL', 3, '2017-08-14', '2017-08-18', 3, 1, null),
(5, '2018-01-30 13:30:00', 'AL', 3, '2018-01-31', '2018-01-31', 3, 1, null),
(6, '2019-12-13 11:15:00', 'AL', 3, '2019-12-16', '2019-12-20', 3, 1, null),
(7, '2020-01-27 13:30:00', 'AL', 3, '2020-01-28', '2020-01-28', 3, 1, null),
(8, '2020-03-09 15:45:00', 'AL', 3, '2020-03-10', '2020-03-12', 3, 1, null),
(9, '2020-03-24 14:00:00', 'AL', 9, '2020-03-25', '2020-03-27', 3, 1, null),
(10, '2020-05-06 09:00:00', 'AL', 9, '2020-05-07', '2020-05-08', 3, 1, null),
(11, '2020-06-16 11:30:00', 'AL', 9, '2020-06-17', '2020-06-17', 3, 1, null),
(12, '2020-11-05 14:00:00', 'AL', 11, '2020-11-06', '2020-11-06', 3, 1, null),
(13, '2020-12-17 09:00:00', 'AL', 11, '2020-12-18', '2020-12-18', 3, 1, null),
(14, '2021-01-28 11:30:00', 'AL', 11, '2021-01-29', '2021-01-29', 3, 1, null),
(15, '2021-05-10 09:00:00', 'AL', 9, '2021-05-11', '2021-05-11', 3, 1, null),
(16, '2021-06-21 11:30:00', 'AL', 9, '2021-06-22', '2021-06-24', 3, 1, null),
(17, '2022-08-04 15:35:24', 'BL', 15, '2022-08-08', '2022-08-08', 3, 1, null),
(18, '2022-09-08 09:00:01', 'BL', 16, '2022-09-12', '2022-09-12', 3, 1, null),
(19, '2022-09-19 16:35:00', 'AL', 3, '2022-09-20', '2022-09-20', 3, 1, null),
(20, '2022-10-13 11:25:37', 'AL', 17, '2022-10-18', '2022-10-22', 3, 1, null),
(21, '2022-10-28 09:00:00', 'AL', 3, '2022-10-31', '2022-10-31', 3, 1, null),
(22, '2022-11-03 14:00:00', 'AL', 11, '2022-11-04', '2022-11-04', 3, 1, null),
(23, '2022-11-17 13:50:14', 'SL', 18, '2022-11-20', '2022-11-21', 3, 1, null),
(24, '2022-12-09 11:15:00', 'AL', 3, '2022-12-12', '2022-12-16', 3, 1, null),
(25, '2022-12-15 09:00:00', 'AL', 11, '2022-12-16', '2022-12-16', 3, 1, null),
(26, '2022-12-22 16:15:50', 'AL', 19, '2022-12-28', '2022-12-29', 3, 1, null),
(27, '2023-01-23 13:30:00', 'AL', 3, '2023-01-24', '2023-01-24', 3, 1, null),
(28, '2023-01-26 10:40:27', 'SL', 20, '2023-01-29', '2023-01-31', 3, 1, null),
(29, '2023-03-18 14:55:58', 'SL', 11, '2023-03-21', '2023-03-23', 3, 1, null),
(30, '2023-04-03 12:05:45', 'SL', 1, '2023-04-05', '2023-04-05', 3, 1, null),
(31, '2023-04-12 09:40:20', 'AL', 10, '2024-03-15', '2024-03-17', 4, 0, null),
(32, '2023-04-15 16:30:10', 'AL', 4, '2023-07-20', '2023-07-21', 3, 0, null),
(33, '2023-04-20 11:45:52', 'AL', 4, '2023-08-23', '2023-08-25', 3, 0, null),
(34, '2023-04-22 10:20:35', 'AL', 12, '2023-04-25', '2023-04-29', 3, 1, null),
(35, '2023-04-25 14:20:18', 'AL', 6, '2023-10-02', '2023-10-06', 3, 0, null),
(36, '2023-04-30 08:55:37', 'AL', 7, '2023-11-06', '2023-11-10', 3, 0, null),
(37, '2023-04-30 12:10:48', 'SFL', 14, '2023-07-05', '2023-07-09', 3, 0, null),
(38, '2023-05-04 10:10:05', 'SL', 8, '2023-12-08', '2023-12-08', 3, 0, null),
(39, '2023-05-07 08:45:11', 'SL', 13, '2023-06-01', '2023-06-03', 3, 0, null),
(40, '2023-05-08 15:25:42', 'AL', 9, '2024-01-15', '2024-01-19', 3, 0, null),
(41, '2023-05-09 09:15:32', 'AL', 9, '2023-07-12', '2023-07-12', 3, 0, null),
(42, '2023-05-09 09:19:35', 'AL', 9, '2023-07-19', '2023-07-19', 3, 0, null);

INSERT INTO leave_decision (request_id, decision_made_by, decision_created_on, status_id, comment) VALUES
(1, 4, '2014-12-12 10:50:00', 3, null),
(2, 4, '2015-01-26 16:00:00', 3, null),
(3, 4, '2015-03-09 21:02:00', 3, null),
(4, 4, '2017-08-11 12:45:00', 3, null),
(5, 4, '2018-01-30 18:00:00', 3, null),
(6, 4, '2019-12-13 15:00:00', 3, null),
(7, 4, '2020-01-27 16:09:00', 3, null),
(8, 4, '2020-03-09 18:00:00', 3, null),
(9, 3, '2020-03-24 17:09:00', 3, null),
(10, 3, '2020-05-06 11:00:00', 3, null),
(11, 3, '2020-06-16 16:25:00', 3, null),
(12, 9, '2020-11-05 16:00:00', 3, null),
(13, 9, '2020-12-17 10:00:00', 3, null),
(14, 9, '2021-01-28 14:00:00', 3, null),
(15, 3, '2021-05-10 18:00:00', 3, null),
(16, 3, '2021-06-21 15:56:00', 3, null),
(17, 13, '2022-08-04 18:45:00', 3, null),
(18, 3, '2022-09-08 17:00:00', 3, null),
(19, 4, '2022-09-19 18:06:00', 3, null),
(20, 16, '2022-10-13 15:00:00', 3, null),
(21, 4, '2022-10-28 11:00:00', 3, null),
(22, 9, '2022-11-03 16:27:00', 3, null),
(23, 16, '2022-11-17 16:09:00', 3, null),
(24, 4, '2022-12-09 16:00:00', 3, null),
(25, 9, '2022-12-15 11:00:00', 3, null),
(26, 16, '2022-12-22 18:06:00', 3, null),
(27, 4, '2023-01-23 18:00:00', 3, null),
(28, 16, '2023-01-26 14:00:00', 3, null),
(29, 9, '2023-03-18 19:00:00', 3, null),
(30, 2, '2023-04-03 15:00:00', 3, null),
(31, 9, '2023-04-12 11:00:00', 4, 'Company anniversary day, please choose another date,thanks.'),
(32, 3, '2023-04-15 19:20:00', 3, null),
(33, 3, '2023-04-20 17:00:00', 3, null),
(34, 9, '2023-04-22 11:00:00', 3, null),
(35, 5, '2023-04-25 17:35:00', 3, null),
(36, 2, '2023-04-30 11:00:00', 3, null),
(37, 13, '2023-04-30 13:00:00', 3, null),
(38, 4, '2023-05-04 16:30:00', 3, null),
(39, 3, '2023-05-10 09:00:00', 3, null),
(40, 3, '2023-05-11 13:00:00', 3, null),
(41, 3, '2023-05-12 11:00:00', 3, null),
(42, 3, '2023-05-09 16:00:00', 3, null);



-- INSERT INTO leave_balance (emp_id, al_balance, sl_balance, updated_on) VALUES
-- (1, 150.00, 30.00, '2023-05-01 09:30:00'),
-- (2, 157.50, 37.50, '2023-05-01 09:30:00'),
-- (3, 97.50, 37.50, '2023-05-01 09:30:00'),
-- (4, 180.00, 37.50, '2023-05-01 09:30:00'),
-- (5, 105.00, 37.50, '2023-05-01 09:30:00'),
-- (6, 105.00, 37.50, '2023-05-01 09:30:00'),
-- (7, 82.50, 37.50, '2023-05-01 09:30:00'),
-- (8, 262.50, 30.00, '2023-05-01 09:30:00'),
-- (9, 240.00, 37.50, '2023-05-01 09:30:00'),
-- (10, 97.50, 37.50, '2023-05-01 09:30:00'),
-- (11, 135.00, 15.00, '2023-05-01 09:30:00'),
-- (12, 255.00, 37.50, '2023-05-01 09:30:00'),
-- (13, 262.50, 37.50, '2023-05-01 09:30:00'),
-- (14, 240.00, 37.50, '2023-05-01 09:30:00'),
-- (15, 90.00, 37.50, '2023-05-01 09:30:00'),
-- (16, 82.50, 37.50, '2023-05-01 09:30:00'),
-- (17, 210.00, 37.50, '2023-05-01 09:30:00'),
-- (18, 90.00, 22.50, '2023-05-01 09:30:00'),
-- (19, 232.50, 37.50, '2023-05-01 09:30:00'),
-- (20, 262.50, 15.00, '2023-05-01 09:30:00'),
-- (21, 127.50, 37.50, '2023-05-01 09:30:00'),
-- (22, 142.50, 37.50, '2023-05-01 09:30:00'),
-- (23, 150.00, 37.50, '2023-05-01 09:30:00'),
-- (24, 112.50, 37.50, '2023-05-01 09:30:00'),
-- (25, 105.00, 37.50, '2023-05-01 09:30:00'),
-- (26, 105.00, 37.50, '2023-05-01 09:30:00'),
-- (27, 150.00, 37.50, '2023-05-01 09:30:00'),
-- (28, 255.00, 37.50, '2023-05-01 09:30:00'),
-- (29, 255.00, 37.50, '2023-05-01 09:30:00'),
-- (30, 255.00, 37.50, '2023-05-01 09:30:00'),
-- (31, 255.00, 37.50, '2023-05-01 09:30:00'),
-- (32, 90.00, 37.50, '2023-05-01 09:30:00'),
-- (33, 202.50, 37.50, '2023-05-01 09:30:00'),
-- (34, 187.50, 37.50, '2023-05-01 09:30:00');