drop table if exists stories;
drop table if exists comments;

create table stories (
  id integer primary key autoincrement,
  title text not null,
  author text not null,
  content text not null
);

create table comments (
  id integer primary key autoincrement,
  author text, not null,
  content text, not null,
  story id not null
);
