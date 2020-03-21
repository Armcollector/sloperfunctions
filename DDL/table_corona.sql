create table corona
(
	date_time datetime not null
		constraint corona_pk
			primary key nonclustered,
	nor_cases int,
	nor_dead int,
	world_cases int,
	world_dead int
)
go

