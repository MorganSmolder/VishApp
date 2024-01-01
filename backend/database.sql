CREATE DATABASE JournalAppDb;
USE JournalAppDb; 
CREATE TABLE User (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Password VARCHAR(255) NOT NULL;
    Name VARCHAR(255)
);

CREATE TABLE JournalEntry (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE,
    Content TEXT
);

CREATE TABLE UserJournalEntry (
    UserId INT,
    JournalEntryId  INT,
    FOREIGN KEY (UserId) REFERENCES User(Id),
    FOREIGN KEY (JournalEntryId) REFERENCES JournalEntry(Id),
    PRIMARY KEY (UserId, JournalEntryId)
);
