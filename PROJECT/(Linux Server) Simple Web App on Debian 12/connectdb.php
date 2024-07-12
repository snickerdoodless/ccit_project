<?php
// Database connection
$servername = "localhost"; // Change this to your MySQL server
$username = "root"; // Change this to your MySQL username
$password = "123"; // Change this to your MySQL password
$database = "webserver"; // Change this to your MySQL database

$conn = new mysqli($servername, $username, $password, $database)

// Check connection
if ($conn->connection_error) {
    die("Connection failed: " . $conn->connection_error);
}

// Form submission handling
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username];
    $password = $_POST["password"];

    // SQL query to insert new user into the database
    $sql = "INSERT INTO username (username, password") VALUES ('$username', '$password')";

    if ($conn->query($sql) === TRUE) {
        echo "Registration Successful!";
    } else {
        echo "Error: " . sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>
    
