import sqlite3
import os

# Nicely borrowed from excercises... 0=non-secret agent, 1=very secret agent

db = \
"""
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Agent (
    id varchar(9) PRIMARY KEY,
    name varchar(200),
    secrecy int
);
INSERT INTO Agent VALUES('Secret','Clank',0);
INSERT INTO Agent VALUES('Gecko','Gex',0);
INSERT INTO Agent VALUES('Robocod','James Pond',1);
INSERT INTO Agent VALUES('Fox','Sasha Nein',1);
INSERT INTO Agent VALUES('Riddle','Voldemort',1);
COMMIT;
"""

if os.path.exists('agents.sqlite'):
	print('agents.sqlite already exists')
else:
	conn = sqlite3.connect('agents.sqlite')
	conn.cursor().executescript(db)
	conn.commit()
