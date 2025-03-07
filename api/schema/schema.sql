CREATE TABLE Squad (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    estimatedHours INTEGER NOT NULL,
    squadId INTEGER NOT NULL,
    FOREIGN KEY (squadId) REFERENCES Squad(id) ON DELETE CASCADE
);

CREATE TABLE Report (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    employeeId INTEGER NOT NULL,
    spentHours INTEGER NOT NULL,
    createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employeeId) REFERENCES Employee(id) ON DELETE CASCADE
);