create table if not exists mainmenu (
id integer primary key autoincrement,
surname text not null,
name text not null,
third_name text not null,
phone integer not null,
email text not null,
times_h integer not null,
times_m integer not null,
simptom text not null,
tm integer not null,
status integer
);