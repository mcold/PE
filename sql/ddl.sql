create table item (id   integer primary key,
                   name text not null);

create table exam (id       integer primary key,
                   id_item  integer references item(id),
                   name     text not null);

create table testset (id        integer primary key,
                      id_exam   integer references exam(id),
                      name      text not null);

create table section (id    integer primary key,
                      name  text not null);

create table quest (id          integer primary key,
                    id_testset  integer references testset(id),
                    id_section  integer references section(id),
                    name        text not null,
                    content     text not null);

create table ans (id            integer primary key,
                  id_quest      integer references quest(id),
                  content       text not null,
                  is_correct    integer not null default 0);

create table exp (id        integer primary key,
                  id_quest  integer references quest(id),
                  content   text not null);