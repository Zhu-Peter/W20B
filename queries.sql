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
    health int not null,
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
