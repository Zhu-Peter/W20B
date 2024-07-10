-- Create a new local DB with the following tables:
-- client
    -- id (PK)
    -- username (unique)
    -- password
    -- joined_on
-- Hint, when creating this column if you give a default value of now() it will automatically give this a value of todays date
create table client (
    id primary key not null auto_increment,
    username varchar(255) unique not null,
    password varchar(255) not null,
    joined_on timestamp not null default now()

-- fighter
    -- id (PK)
    -- client_id (FK)
    -- move_one (FK)
    -- move_two (FK)
    -- move_three (FK)
    -- move_four (FK)
    -- name
    -- health
    -- points
create table fighter (
    id primary key not null auto_increment,
    client_id int not null,
    move_one int not null,
    move_two int not null,
    move_three int not null,
    move_four int not null,
    name varchar(255) not null,
    health int not null,
    points int not null,
    foreign key (client_id) references client(id) on delete cascade,
    foreign key (move_one) references move(id) on delete cascade,
    foreign key (move_two) references move(id) on delete cascade,
    foreign key (move_three) references move(id) on delete cascade,
    foreign key (move_four) references move(id) on delete cascade

-- computer_fighter
    -- id (PK)
    -- move_one (FK)
    -- move_two (FK)
    -- move_three (FK)
    -- move_four (FK)
    -- name
    -- health
create table computer_fighter (
    id primary key not_null auto_increment,
    move_one int not null,
    move_two int not null,
    move_three int not null,
    move_four int not null,
    name varchar(255) not null,
    health int not null default 100,
    foreign key (move_one) references move(id) on delete cascade,
    foreign key (move_two) references move(id) on delete cascade,
    foreign key (move_three) references move(id) on delete cascade,
    foreign key (move_four) references move(id) on delete cascade

-- move
    -- id (PK)
    -- name
    -- lower_damage_range
    -- upper_damage_range
create table move (
    id primary key not_null auto_increment,
    name varchar(255) not null,
    lower_damage_range int not null,
    upper_damage_range int not null

-- Insert at least 10 moves into your DB
insert into move (name, lower_damage_range, upper_damage_range) values 
    ('Rock', 1, 10),
    ('Paper', 11, 20),
    ('Scissors', 21, 30),
    ('Lizard', 31, 40),
    ('Spock', 41, 50),
    ('Punch', 51, 60),
    ('Kick', 61, 70),
    ('Clap', 71, 80),
    ('Boom', 81, 90),
    ('Smash', 91, 100);

-- Insert at least 1 computer_fighter into your DB
insert into computer_fighter (name, health, move_one, move_two, move_three, move_four) values
    ('Bob', 100, 1, 2, 3, 4),
    ('Chuck', 100, 5, 6, 7, 8),
    ('Hulk', 1000, 9, 8, 7, 0)


-- PROCEDURES
-- Add the following stored procedures:
-- One that takes in a username and password and adds a new client
create procedure add_client(user varchar(255), pass varchar(255))
    insert into client (username, password) values (user, pass)

-- One that takes in a username and password and returns the potential user with the matching username and password
create procedure login(user varchar(255), pass varchar(255))
    select * from client where username = user and password = pass

-- One that takes in a client_id, 4 move id's, fighter name and adds a new fighter
create procedure add_fighter(client_id int, move_one int, move_two int, move_three int, move_four int, name varchar(255))
    insert into computer_fighter (client_id, move_one, move_two, move_three, move_four, name, health) values (client_id, move_one, move_two, move_three, move_four, name)

-- One that takes in a client_id and returns all fighters that belong to that client
create procedure get_fighters(client_id int)
    select * from computer_fighter where client_id = client_id

-- One that returns all move id's, names, lower_damage_range and upper_damage_range
create procedure get_moves()
    select * from moves

-- One that takes in an id for a fighter and a point number and adds to their points total
create procedure add_points(id int, points int)
    update computer_fighter set computer_fighter.points = computer_fighter.points + points where computer_fighter.id = id

-- One that takes 0 arguments and returns all computer_fighters id, name, health, move_one, move_two, move_three, move_four
create procedure get_all_fighters()
    select * from computer_fighter
