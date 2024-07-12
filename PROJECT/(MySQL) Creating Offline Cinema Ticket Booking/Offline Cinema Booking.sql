------------------- C R E A T I N G  D A T A B A S E -------------------

CREATE DATABASE OfflineBooking
USE OfflineBooking

------------------- C R E A T I N G  T A B L E -------------------

-- CREATING TABLE FOR MOVIES
CREATE TABLE Movies(
id_movies INT PRIMARY KEY NOT NULL IDENTITY (1, 1),
title VARCHAR (30) NOT NULL,
duration VARCHAR (8) NOT NULL,
release_year INT NOT NULL,
age_rate CHAR (5) NOT NULL)

-- CREATING TABLE FOR STUDIO
CREATE TABLE Studio (
id_studio INT PRIMARY KEY NOT NULL IDENTITY (1, 1),
studio_number CHAR (5) UNIQUE NOT NULL)

-- CREATING TABLE FOR SCHEDULE
CREATE TABLE Schedule (
id_schedule INT PRIMARY KEY NOT NULL IDENTITY (1, 1),
start_at CHAR (5) NOT NULL,
dates DATE NOT NULL,
movies_id INT FOREIGN KEY (movies_id) REFERENCES Movies(id_movies) NOT NULL,
studio_id INT FOREIGN KEY (studio_id) REFERENCES Studio (id_studio) NOT NULL)

-- CREATING TABLE FOR SEAT
CREATE TABLE Seat (
id_seat INT PRIMARY KEY NOT NULL IDENTITY (1, 1),
seat_number INT NOT NULL,
studio_id INT FOREIGN KEY (studio_id) REFERENCES Studio(id_studio)NOT NULL) 

-- CREATING TABLE FOR TICKET
CREATE TABLE Ticket (
id_ticket INT PRIMARY KEY NOT NULL IDENTITY (1, 1),
ticket_date DATE NOT NULL,
seat_id INT FOREIGN KEY (seat_id) REFERENCES Seat (id_seat) NOT NULL,
schedule_id INT FOREIGN KEY (schedule_id) REFERENCES Schedule(id_schedule) NOT NULL)

-- CREATING TABLE FOR BOOKING
CREATE TABLE Booking (
id_booking INT PRIMARY KEY IDENTITY (1, 1),
ticket_amount INT,
ticket_price MONEY,
total_price MONEY)

-- CREATING TABLE FOR ORDER DETAIL
CREATE TABLE OrderDetail (
booking_id INT FOREIGN KEY (booking_id) REFERENCES Booking (id_booking),
ticket_id INT FOREIGN KEY (ticket_id) REFERENCES Ticket (id_ticket))


-- CREATING TABLE FOR PAYMENT
CREATE TABLE Payment (
booking_id INT FOREIGN KEY (booking_id) REFERENCES Booking (id_booking),
payment_method VARCHAR (20),
payment_date DATE,
CONSTRAINT PayMthd CHECK ( payment_method IN ('CASH', 'E-WALLET', 'TRANSFER')))


------------------- I N S E R T I N G  D A T A -------------------

-- INSERTING DATA TO TABLE MOVIES
INSERT INTO Movies (title, release_year, duration, age_rate)
VALUES 
    ('Inception', 2010, '2:28:00', 'PG'),
    ('Oppenheimer', 2023, '3:00:00', 'R'),
    ('The Dark Knight', 2008, '2:32:00', 'PG'),
    ('Interstellar', 2014, '2:49:00', 'PG'),
    ('Dunkirk', 2017, '1:46:00', 'G')

	
-- INSERTING DATA TO TABLE STUDIO
INSERT INTO Studio(studio_number)
VALUES 
    ('ST1'),
	('ST2'),
	('ST3')


-- INSERTING DATA TO TABLE SCHEDULE
INSERT INTO Schedule(start_at, dates, movies_id, studio_id)
VALUES 
    ('13:00', '12-29-2023', 1, 1),
	('10:00', '12-29-2023', 2, 1),
	('16:00', '12-30-2023', 3, 2),
	('20:00', '12-30-2023', 4, 2),
	('13:00', '12-31-2023', 5, 3)


-- INSERTING DATA INTO SEAT TABLE
INSERT INTO Seat (seat_number, studio_id)
VALUES 
    (101, 1), -- Seat 101 in Studio 1
    (102, 1), -- Seat 102 in Studio 1
    (103, 1), -- Seat 103 in Studio 1
    (104, 1), -- Seat 104 in Studio 1
    (105, 1), -- Seat 105 in Studio 1
    (101, 2), -- Seat 106 in Studio 2
    (102, 2), -- Seat 107 in Studio 2
    (103, 2), -- Seat 108 in Studio 2
    (104, 2), -- Seat 109 in Studio 2
    (105, 2), -- Seat 110 in Studio 2
	(101, 3), -- Seat 101 in Studio 3
    (102, 3), -- Seat 102 in Studio 3
    (103, 3), -- Seat 103 in Studio 3
    (104, 3), -- Seat 104 in Studio 3
    (105, 3) -- Seat 105 in Studio 3


-- INSERTING DATA INTO TICKET TABLE
INSERT INTO Ticket (ticket_date, seat_id, schedule_id)
VALUES 
	(GETDATE(), 1, 2),
	(GETDATE(), 2, 2),
	(GETDATE(), 6, 4),
	(GETDATE(), 7, 4),
	(GETDATE(), 14, 5),
	(GETDATE(), 15, 5),
	(GETDATE(), 9, 3),
	(GETDATE(), 10, 3)
	
------------------- P R O C E D U R E -------------------

-- PROCEDURE FOR INSERTING NEW MOVIES
CREATE PROCEDURE addNewMovies
    @title VARCHAR(50),
    @duration VARCHAR(50),
    @year INT,
    @age VARCHAR(50),
    @start VARCHAR(19),
    @date DATE,
	@movieID INT,
    @studnum INT
AS
BEGIN
    -- Insert into Movies table
    INSERT INTO Movies (title, duration, release_year, age_rate)
    VALUES (@title, @duration, @year, @age);

    -- Insert into Schedule table
    INSERT INTO Schedule (start_at, dates, movies_id, studio_id)  
    VALUES (@start, @date, @movieId, @studnum);

	PRINT 'Movies data inserted successfully'
	PRINT 'Age Rate Note : (PARENTAL GUIDANCE), (GENERAL), (RESTRICTED)'

END


-- PROCEDURE ADD NEW TICKET
CREATE PROCEDURE newTicket
	@date DATE,
	@seat INT,
	@schedule INT
AS
BEGIN
	-- Insert into Ticket table
	INSERT INTO Ticket (ticket_date, seat_id, schedule_id)
	VALUES (@date, @seat, @schedule)
	PRINT 'New Ticket Successfully Added'
END


-- PROCEDURE NEW BOOKING
CREATE PROCEDURE newBooking
	@amount INT
AS
BEGIN
	INSERT INTO Booking (ticket_amount)
	VALUES (@amount)
	PRINT 'New Order Inserted'
END
 

-- PROCEDURE DETAIL ORDER
-- view ticket table fisrt before inserting new detail order
CREATE PROCEDURE newDetailOrder
	@booking INT,
	@ticket INT
AS
BEGIN
	INSERT INTO OrderDetail (booking_id, ticket_id)
	VALUES (@booking, @ticket)
END


-- PROCEDURE PAYMENT
CREATE PROCEDURE newPayment
	@bookid INT,
	@date DATE,
	@paymethod VARCHAR (20)
AS
BEGIN
	INSERT INTO Payment (booking_id, payment_date, payment_method)
	VALUES (@bookid, @date, @paymethod)
	PRINT 'Payment success'
END


------------------- T R I G G E R  -------------------

-- TRIGGER AUTOMATIC UPDATE TICKET PRICE AND CALCULATE IT IN BOOKING
CREATE TRIGGER bookingPrices
ON Booking
AFTER INSERT
AS
BEGIN
    -- Set fixed ticket_price
    UPDATE b
    SET ticket_price = 5.25
    FROM Booking b
    INNER JOIN inserted i ON b.id_booking = i.id_booking;

    -- Calculate total price based on ticket amount and ticket price
    UPDATE b
    SET total_price = i.ticket_amount * b.ticket_price
    FROM Booking b
    INNER JOIN inserted i ON b.id_booking = i.id_booking;
END

------------------- V I E W   -------------------

-- VIEWING ALL TABLES
SELECT * FROM Movies
SELECT * FROM Schedule
SELECT * FROM Studio
SELECT * FROM Seat
SELECT * FROM  Ticket
SELECT * FROM Booking
SELECT * FROM OrderDetail
SELECT * FROM Payment


