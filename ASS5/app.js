const express = require('express');
const fs = require('fs');
const app = express();

// Middleware to parse JSON request bodies
app.use(express.json());

// In-memory database (users stored in a text file)
const userDataFile = 'users.txt';

// Helper function to read users from the file
function readUsers() {
    if (!fs.existsSync(userDataFile)) {
        return {};
    }
    const data = fs.readFileSync(userDataFile, 'utf-8');
    const users = {};
    data.split('\n').forEach(line => {
        if (line.trim()) {
            const [name, email, phone, age] = line.split(',');
            users[email] = { name, email, phone, age: parseInt(age) };
        }
    });
    return users;
}

// Helper function to write users to the file
function writeUsers(users) {
    const data = Object.values(users)
        .map(user => `${user.name},${user.email},${user.phone},${user.age}`)
        .join('\n');
    fs.writeFileSync(userDataFile, data, 'utf-8');
}

// Route to register a new user (POST /add_user)
app.post('/add_user', (req, res) => {
    const { name, email, phone, age } = req.body;
    if (!name || !email || !phone || !age) {
        return res.status(400).json({ error: 'Name, email, phone, and age are required!' });
    }

    const users = readUsers();
    if (users[email]) {
        return res.status(400).json({ error: 'User already exists!' });
    }

    users[email] = { name, email, phone, age };
    writeUsers(users);
    res.status(201).json({ message: 'User registered successfully!' });
});

// Route to retrieve user information (GET /user)
app.get('/user', (req, res) => {
    const { email } = req.query;
    if (!email) {
        return res.status(400).json({ error: 'Email is required!' });
    }

    const users = readUsers();
    if (!users[email]) {
        return res.status(404).json({ error: 'User not found!' });
    }

    res.json(users[email]);
});

// Route to update user information (PUT /user)
app.put('/user', (req, res) => {
    const { email } = req.query;
    const { name, phone, age } = req.body;
    if (!email || (!name && !phone && !age)) {
        return res.status(400).json({ error: 'Email and at least one field (name, phone, age) are required!' });
    }

    const users = readUsers();
    if (!users[email]) {
        return res.status(404).json({ error: 'User not found!' });
    }

    if (name) users[email].name = name;
    if (phone) users[email].phone = phone;
    if (age) users[email].age = age;

    writeUsers(users);
    res.json({ message: 'User updated successfully!' });
});

// Route to delete user information (DELETE /user)
app.delete('/user', (req, res) => {
    const { email } = req.query;
    if (!email) {
        return res.status(400).json({ error: 'Email is required!' });
    }

    const users = readUsers();
    if (!users[email]) {
        return res.status(404).json({ error: 'User not found!' });
    }

    delete users[email];
    writeUsers(users);
    res.json({ message: 'User deleted successfully!' });
});

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
