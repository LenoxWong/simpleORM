-- schema.sql

drop database if exists Test;

create database Test;

use Test;

grant select, insert, update, delete on Test.* to 'test'@'localhost' identified by 'test';

create table users (
    `uid` int not null,
    `name` varchar(16) not null,
    `email` varchar(64),
    primary key (`uid`)
) engine=innodb default charset=utf8;
