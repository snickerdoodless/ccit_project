------ DRY RUN ------


-- AVAIALBLE MOVIES --
SELECT * FROM Movies

-- MOVIES SCHEDULE --
SELECT * FROM Schedule

-- BUYING TICKET --

-- see ticket that available
SELECT * FROM Ticket
SELECT * FROM Seat

-- ordering ticket for movies id 3
EXEC newBooking /* ticket amount */ 2
SELECT * FROM Booking

-- giving detail for ordering ticket
-- see ticket id to match for detail order
EXEC newDetailOrder /* booking id */ 1, /* 1 because its increment */ /* ticket id to movies id 3 */ 7
-- because the buyers buy 2 ticket repeat the procedure but different ticket id
EXEC newDetailOrder /* booking id */ 1, /* 1 because its increment */ /* ticket id to movies id 3 */ 8
SELECT * FROM OrderDetail

-- PAYMENT --
EXEC newPayment /* booking id */ 1, /* dates */ '12-27-2023', /* paymethod */ 'CASH'
SELECT * FROM Payment

-- RESULT --
SELECT * FROM Movies
SELECT s.id_schedule, s.start_at, s.dates, m.title, st.studio_number
FROM Schedule s JOIN Movies m
ON m.id_movies = s.movies_id 
JOIN Studio st ON s.studio_id = st.id_studio

CREATE VIEW view_AvaiableMovies
AS
(
SELECT s.id_schedule, s.start_at, s.dates, m.title, st.studio_number
FROM Schedule s JOIN Movies m
ON m.id_movies = s.movies_id 
JOIN Studio st ON s.studio_id = st.id_studio
)

SELECT * FROM view_AvaiableMovies



SELECT * FROM Seat
SELECT * FROM  Ticket
SELECT * FROM Booking
SELECT * FROM OrderDetail


-- NEW MOVIES CAME OUT --
EXEC addNewMovies 'The Fast & Furious', '1:46:00', 2001, 'PG', '14:00', '2023-12-29', 6, 1
-- new movies mean new ticket
EXEC newTicket '12-28-2023', 1, 6