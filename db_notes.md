select _ from chains;
select _ from channel;
select _ from users_role;
select _ from areas;
select _ from agency;
select _ from stores;
select _ from users;
select _ from users*schedules;
select * from skus;
select _ from category;
select _ from category*refs;
select * from stores*skus;
select * from devices;
select \_ from logs_logins;

-- SELECT
-- tbl_stores.store_name
-- tbl_stores.tblstoreid AS tblstoreid
-- tbl_stores.geofence
-- longitude
-- latitude
-- null as address
-- to_char(tbl_stores.app_update
-- 'yyyy-mm-dd HH24:MI:SS') AS date_updated
-- FROM
-- tbl_stores
-- INNER JOIN tbl_assigned_stores
-- ON tbl_assigned_stores.tblstoreid = tbl_stores.tblstoreid
-- INNER JOIN tbl_users
-- ON tbl_assigned_stores.tbluserid = tbl_users.tbluserid
-- WHERE
-- username = 'DP-ACSUP' AND
-- password = '176bb4f126c1a6a1f937f31f6ffdf41a' AND
-- tbl_users.active = 'Yes'
-- ORDER BY tbl_stores.store_name ASC

-- select _ from users_schedules ;
-- select _ from users;

insert into tbl*sku_stocks_per_store_new select * from tbl*sku_stocks_per_store
ON CONFLICT (tblstoreid,tblskuid) DO UPDATE
SET (carry,app_update) = (EXCLUDED.carry, now());
select * from tbl_sku_stocks_per_store_new order by date_transaction desc limit 200;

CREATE TABLE public.m_attendance_monitoring(
id bigserial PRIMARY KEY,
tbluserid character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(50) COLLATE pg_catalog."default",
longitude_in character varying(50) COLLATE pg_catalog."default",
latitude_in character varying(50) COLLATE pg_catalog."default",
time_in time without time zone,
timein_status character varying(50) COLLATE pg_catalog."default",
captured_photo character varying(200) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
UNIQUE(tbluserid,tblstoreid,date_created)
);

CREATE TABLE public.m_changedayoff
(
id bigserial PRIMARY KEY,
tblstoreid character varying(50) COLLATE pg_catalog."default",
tbluserid character varying(255) COLLATE pg_catalog."default",
tbldailystockid bigint,
current_day_off character varying(50) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
change_by_id character varying(255) COLLATE pg_catalog."default",
confirm_by character varying(50) COLLATE pg_catalog."default",
confirm_status character varying(50) COLLATE pg_catalog."default",
new_day_off character varying(50) COLLATE pg_catalog."default",
date_confirmed date,
confirmation character varying(50) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
UNIQUE(tbluserid,mobile_generated_id)
);

CREATE TABLE public.m_team_attendance
(
id bigserial PRIMARY KEY,
tblsingleroleid integer,
tblstoreid character varying(50) COLLATE pg_catalog."default",
tbluserid character varying(255) COLLATE pg_catalog."default",
remarks character varying(50) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
filed_by character varying(255) COLLATE pg_catalog."default" DEFAULT 'Team Leader/ Sub-Team Leader'::character varying,
mobile_generated_id text COLLATE pg_catalog."default",
early_file text COLLATE pg_catalog."default",
UNIQUE(tbluserid,mobile_generated_id)
);

CREATE INDEX idx_m_team_attendance_u_c ON m_team_attendance (tbluserid,date_created);
CREATE INDEX idx_m_team_attendance_u_s_c ON m_team_attendance (tbluserid,tblstoreid,date_created);
CREATE INDEX idx_m_team_attendance_m ON m_team_attendance (mobile_generated_id);

CREATE TABLE public.confirm_mcp
(
id serial primary key,
tbluserid character varying(255) COLLATE pg_catalog."default",
tcp_user_id character varying(255) COLLATE pg_catalog."default",
schedule date,
schedule_type character varying(100) COLLATE pg_catalog."default",
tc_tcp_store_id character varying(255) COLLATE pg_catalog."default",
schedule_status character varying(100) COLLATE pg_catalog."default",
adjustment_status character varying(50) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
confirmed_by character varying(50) COLLATE pg_catalog."default",
date_confirmed date,
office character varying(50) COLLATE pg_catalog."default",
status character varying(50) COLLATE pg_catalog."default",
reason character varying(255) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now()
);

CREATE TABLE public.m_mcp
(
id bigserial not null,
tbluserid character varying(255) COLLATE pg_catalog."default",
tcp_user_id character varying(255) COLLATE pg_catalog."default",
schedule date,
schedule_type character varying(100) COLLATE pg_catalog."default",
tc_tcp_store_id character varying(255) COLLATE pg_catalog."default",
schedule_status character varying(100) COLLATE pg_catalog."default",
adjustment_status character varying(50) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
confirmed_by character varying(50) COLLATE pg_catalog."default",
date_confirmed date,
office character varying(50) COLLATE pg_catalog."default",
status character varying(50) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
constraint m_mcp_pk primary key (id, date_created),
UNIQUE(tbluserid,mobile_generated_id,date_created)
) PARTITION BY RANGE (date_created);

CREATE INDEX idx_m_mcp_u_y_s ON m_mcp (tbluserid,schedule_type,schedule);
CREATE INDEX idx_m_mcp_u_s ON m_mcp (tbluserid,schedule);
CREATE INDEX idx_m_mcp_u_s_s ON m_mcp (tbluserid,schedule_status,schedule);

CREATE TABLE m_mcp_y21p1 PARTITION OF m_mcp
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE m_mcp_y21p2 PARTITION OF m_mcp
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE m_mcp_y21p3 PARTITION OF m_mcp
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE m_mcp_y21p4 PARTITION OF m_mcp
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE public.m_osa
(
id bigserial not null,
tbluserid character varying(255) COLLATE pg_catalog."default",
tblskuid character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(255) COLLATE pg_catalog."default",
availability character varying(255) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
sku_generated_id character varying(255) COLLATE pg_catalog."default",
constraint m_osa_pk primary key (id, date_created),
UNIQUE(tbluserid,tblstoreid,sku_generated_id,date_created)
) PARTITION BY RANGE (date_created);

CREATE INDEX idx_m_osa_m_dc ON logs_mobile (tbluserid,module,date_created);
CREATE INDEX idx_m_osa_dc ON logs_mobile (tbluserid,date_created);

CREATE TABLE m_osa_y21p1 PARTITION OF m_osa
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE m_osa_y21p2 PARTITION OF m_osa
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE m_osa_y21p3 PARTITION OF m_osa
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE m_osa_y21p4 PARTITION OF m_osa
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE public.m_facings (
id serial not null,
tbluserid character varying(255) COLLATE pg_catalog."default",
tblrefid integer,
tblcategoryid integer,
no_of_facings integer,
tblstoreid character varying(50) COLLATE pg_catalog."default",
category_space character varying(50) COLLATE pg_catalog."default",
mnc_space character varying(50) COLLATE pg_catalog."default",
actual_cm_space character varying(255) COLLATE pg_catalog."default",
percent_share character varying(50) COLLATE pg_catalog."default",
target real,
complied character varying(50) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
mobile_generated_id character varying(50) COLLATE pg_catalog."default",
constraint m_facings_pk primary key (id,date_created),
UNIQUE(tbluserid,mobile_generated_id,date_created)
) PARTITION BY RANGE (date_created);

CREATE INDEX idx_m_facings_u ON m_facings (tbluserid,tblstoreid,date_created);

CREATE TABLE m_facings_y21p1 PARTITION OF m_facings
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE m_facings_y21p2 PARTITION OF m_facings
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE m_facings_y21p3 PARTITION OF m_facings
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE m_facings_y21p4 PARTITION OF m_facings
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE public.m_planograms
(
id bigserial not null,
tbluserid character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(50) COLLATE pg_catalog."default",
type character varying(50) COLLATE pg_catalog."default",
tblrefid integer,
tblcategoryid integer,
followed character varying(50) COLLATE pg_catalog."default",
notes character varying(255) COLLATE pg_catalog."default",
image_path character varying(255) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
constraint m_planograms_pk primary key (id, date_created),
UNIQUE(tbluserid,mobile_generated_id,date_created)
) PARTITION BY RANGE (date_created);

CREATE INDEX idx_m_planograms_u ON m_planograms (tbluserid,tblstoreid,date_created);

CREATE TABLE m_planograms_y21p1 PARTITION OF m_planograms
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE m_planograms_y21p2 PARTITION OF m_planograms
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE m_planograms_y21p3 PARTITION OF m_planograms
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE m_planograms_y21p4 PARTITION OF m_planograms
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE public.m_compet_acts
(
id bigserial not null,
tbluserid character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(50) COLLATE pg_catalog."default",
tblskuid character varying(255) COLLATE pg_catalog."default",
tblcategoryid integer,
sku_name character varying(255) COLLATE pg_catalog."default",
activity_name character varying(255) COLLATE pg_catalog."default",
mechanics character varying(255) COLLATE pg_catalog."default",
notes text COLLATE pg_catalog."default",
scheme character varying(255) COLLATE pg_catalog."default",
price real,
placement character varying(255) COLLATE pg_catalog."default",
duration_type character varying(255) COLLATE pg_catalog."default",
date_from date,
date_to date,
type character varying(100) COLLATE pg_catalog."default",
has_effect_on_offtake character varying(255) COLLATE pg_catalog."default",
image_path character varying(255) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
competitor character varying(255) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
sku_price character varying(255) COLLATE pg_catalog."default",
brand character varying(255) COLLATE pg_catalog."default",
constraint m_compet_acts_pk primary key (id, date_created),
UNIQUE(tbluserid,mobile_generated_id,date_created)
) PARTITION BY RANGE (date_created);

CREATE INDEX idx_m_compet_acts_u ON m_compet_acts (tbluserid,tblstoreid,date_created);

CREATE TABLE m_compet_acts_y21p1 PARTITION OF m_compet_acts
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE m_compet_acts_y21p2 PARTITION OF m_compet_acts
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE m_compet_acts_y21p3 PARTITION OF m_compet_acts
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE m_compet_acts_y21p4 PARTITION OF m_compet_acts
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE public.m_promo_acts
(
id bigserial not null,
tbluserid character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(50) COLLATE pg_catalog."default",
tblskuid character varying(255) COLLATE pg_catalog."default",
tblcategoryid integer,
sku_name character varying(255) COLLATE pg_catalog."default",
activity_name character varying(255) COLLATE pg_catalog."default",
mechanics character varying(255) COLLATE pg_catalog."default",
notes text COLLATE pg_catalog."default",
scheme character varying(255) COLLATE pg_catalog."default",
price real,
placement character varying(255) COLLATE pg_catalog."default",
duration_type character varying(255) COLLATE pg_catalog."default",
date_from date,
date_to date,
type character varying(100) COLLATE pg_catalog."default",
has_effect_on_offtake character varying(255) COLLATE pg_catalog."default",
image_path character varying(255) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
competitor character varying(255) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
sku_price character varying(255) COLLATE pg_catalog."default",
brand character varying(255) COLLATE pg_catalog."default",
constraint m_promo_acts_pk primary key (id, date_created),
UNIQUE(tbluserid,mobile_generated_id,date_created)
) PARTITION BY RANGE (date_created);

CREATE INDEX idx_m_promo_acts_u ON m_promo_acts (tbluserid,tblstoreid,date_created);

CREATE TABLE m_promo_acts_y21p1 PARTITION OF m_promo_acts
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE m_promo_acts_y21p2 PARTITION OF m_promo_acts
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE m_promo_acts_y21p3 PARTITION OF m_promo_acts
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE m_promo_acts_y21p4 PARTITION OF m_promo_acts
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE public.m_file_leave
(
id bigserial primary key,
tbluserid character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(50) COLLATE pg_catalog."default",
mobile_generated_id character varying(200) COLLATE pg_catalog."default",
longitude character varying(50) COLLATE pg_catalog."default",
latitude character varying(50) COLLATE pg_catalog."default",
leave_category character varying(50) COLLATE pg_catalog."default",
date_of_leave_from date,
date_of_leave_to date,
reason character varying(255) COLLATE pg_catalog."default",
confirmation character varying(50) COLLATE pg_catalog."default",
confirm_by character varying(255) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_update timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
UNIQUE(tbluserid,mobile_generated_id)
);

CREATE TABLE public.confirm_over_time
(
id bigserial primary key,
tbluserid character varying(255) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
confirm_by character varying(255) COLLATE pg_catalog."default",
confirmation character varying(255) COLLATE pg_catalog."default",
date_confirmed timestamp without time zone,
date_sync timestamp with time zone DEFAULT now()
);

CCREATE TABLE public.confirm_file_leave(
id bigserial primary key,
tblfileleaveid bigint,
confirmation character varying(50) COLLATE pg_catalog."default",
confirm_by character varying(255) COLLATE pg_catalog."default",
date_confirmed timestamp without time zone,
cancel_generated_id character varying(255) COLLATE pg_catalog."default",
date_sync timestamp with time zone DEFAULT now()
);

CREATE TABLE public.m_breaks
(
id serial PRIMARY KEY,
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
tbluserid character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(50) COLLATE pg_catalog."default",
break_name character varying(50) COLLATE pg_catalog."default",
break_designated_time character varying(255) COLLATE pg_catalog."default",
break_consume_time character varying(50) COLLATE pg_catalog."default",
break_status character varying(50) COLLATE pg_catalog."default",
"time" time without time zone,
date date,
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
over_break_minutes character varying COLLATE pg_catalog."default",
UNIQUE(tbluserid,mobile_generated_id)
);

CREATE TABLE public.m_over_time
(
id bigserial primary key,
tbluserid character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(50) COLLATE pg_catalog."default",
ot_hour character varying(20) COLLATE pg_catalog."default",
reason character varying(255) COLLATE pg_catalog."default",
confirm_by character varying(255) COLLATE pg_catalog."default",
confirmation character varying(50) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
UNIQUE(tbluserid,mobile_generated_id)
);

CREATE TABLE public.app_versions
(
id serial PRIMARY KEY,
version character varying(255) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
mdc text COLLATE pg_catalog."default",
coor_mgr text COLLATE pg_catalog."default"
);

CREATE TABLE public.devices
(
id bigserial PRIMARY KEY,
userid character varying(255) COLLATE pg_catalog."default",
device_id character varying(255) COLLATE pg_catalog."default",
status character varying(255) COLLATE pg_catalog."default" DEFAULT 'active'::character varying,
date_updated character varying(255) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_sync timestamp with time zone DEFAULT now(),
appversion character varying(255) COLLATE pg_catalog."default",
device_info character varying(255) COLLATE pg_catalog."default",
imei character varying(255) COLLATE pg_catalog."default",
UNIQUE(userid,device_id)
);

CREATE INDEX idx_logs_mobile_u ON devices (userid);

CREATE TABLE public.channel
(
id serial PRIMARY KEY,
channelid integer,
name character varying(50) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(name)
);

CREATE TABLE public.users_role
(
id serial PRIMARY KEY,  
 roleid integer,
userrole character varying(255) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(roleid,userrole)
);

CREATE TABLE public.logs_mobile
(  
 id bigserial not null,
tbluserid character varying(255) COLLATE pg_catalog."default",
mgenerated_id character varying(255) COLLATE pg_catalog."default",
module character varying(255) COLLATE pg_catalog."default",
event text COLLATE pg_catalog."default",
current_longitude character varying(50) COLLATE pg_catalog."default",
current_latitude character varying(50) COLLATE pg_catalog."default",
end_longitude character varying(50) COLLATE pg_catalog."default",
end_latitude character varying(50) COLLATE pg_catalog."default",
gps_accuracy real,
gps_provider character varying(5000) COLLATE pg_catalog."default",
battery integer,
date_created timestamp with time zone DEFAULT now(),
date_sync timestamp with time zone DEFAULT now(),
netinfo character varying(600) COLLATE pg_catalog."default",
device_id character varying(255) COLLATE pg_catalog."default",
tblstoreid character varying(255) COLLATE pg_catalog."default",
constraint mobile_logs_pk primary key (id, date_created),
UNIQUE(tbluserid,mgenerated_id,date_created)
) PARTITION BY RANGE (date_created);

CREATE INDEX idx_logs_mobile_m_dc ON logs_mobile (tbluserid,module,date_created);
CREATE INDEX idx_logs_mobile_dc ON logs_mobile (tbluserid,date_created);

CREATE TABLE logs_mobile_y21p1 PARTITION OF logs_mobile
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE logs_mobile_y21p2 PARTITION OF logs_mobile
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE logs_mobile_y21p3 PARTITION OF logs_mobile
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE logs_mobile_y21p4 PARTITION OF logs_mobile
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE public.logs_logins
(
id bigserial not null,
tbluserid character varying(255) COLLATE pg_catalog."default",
device_id character varying(255) COLLATE pg_catalog."default",
message character varying(255) COLLATE pg_catalog."default" DEFAULT 'active'::character varying,
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
date_sync timestamp with time zone DEFAULT now(),
appversion character varying(255) COLLATE pg_catalog."default",
device_info character varying(255) COLLATE pg_catalog."default",
imei text COLLATE pg_catalog."default",
constraint logs_logins_pk primary key (id, date_created),
UNIQUE(tbluserid,date_created)
) PARTITION BY RANGE (date_created);;

CREATE INDEX idx_logs_logins_ifn ON logs_logins (tbluserid,device_id);
CREATE INDEX idx_logs_logins_id ON logs_logins (tbluserid,date_created);

CREATE TABLE logs_logins_y21p1 PARTITION OF logs_logins
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE logs_logins_y21p2 PARTITION OF logs_logins
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE logs_logins_y21p3 PARTITION OF logs_logins
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE logs_logins_y21p4 PARTITION OF logs_logins
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE IF NOT EXISTS public.skus
(
id serial PRIMARY KEY,
catrefsid integer NOT NULL,
catid integer not null,
skucode character varying(255) COLLATE pg_catalog."default",
skuid character varying(255) COLLATE pg_catalog."default",
sap_name character varying(255) COLLATE pg_catalog."default",
case_barcode character varying(255) COLLATE pg_catalog."default",
product_barcode character varying(255) COLLATE pg_catalog."default",
gross_price_case real,
gross_price_piece real,
quantity_per_case real,
packsize real,
unit_of_measure character varying(20) COLLATE pg_catalog."default",
active character varying(200) COLLATE pg_catalog."default",
image_path character varying(200) COLLATE pg_catalog."default" DEFAULT 'sku-default'::character varying,
size character varying(20) COLLATE pg_catalog."default",
form character varying(20) COLLATE pg_catalog."default",
packaging_description character varying(255) COLLATE pg_catalog."default",
remarks character varying(255) COLLATE pg_catalog."default",
packs_or_bags character varying(10) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(skuid)
);

CREATE TABLE IF NOT EXISTS public.users
(  
 id serial PRIMARY KEY,
employeeid character varying(50) COLLATE pg_catalog."default",  
 userid character varying(255) COLLATE pg_catalog."default",
roleid integer,
username character varying(80) COLLATE pg_catalog."default",
password character varying(80) COLLATE pg_catalog."default",
firstname character varying(80) COLLATE pg_catalog."default",
middle_initial character varying(40) COLLATE pg_catalog."default" DEFAULT 'na'::character varying,
lastname character varying(80) COLLATE pg_catalog."default",
mobile_number character varying(14) COLLATE pg_catalog."default",
date_started date,
birthdate date,
image_path character varying(200) COLLATE pg_catalog."default" NOT NULL DEFAULT 'user-default'::character varying,
priority character varying(10) COLLATE pg_catalog."default" DEFAULT '1'::character varying,
active character varying(3) COLLATE pg_catalog."default" NOT NULL DEFAULT 'Yes'::character varying,
agencyid text DEFAULT 'MNC'::text,
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(userid)
);

CREATE INDEX idx_users_id ON users (userid);

CREATE TABLE IF NOT EXISTS public.users_schedules
(
id serial PRIMARY KEY,
storeid character varying(50) COLLATE pg_catalog."default",
userid character varying(255) COLLATE pg_catalog."default",
schedule_day character varying(50) COLLATE pg_catalog."default",
schedule_type character varying(50) COLLATE pg_catalog."default",
working_time character varying(200) COLLATE pg_catalog."default",
day_off character varying(200) COLLATE pg_catalog."default",
day_off2 character varying(200) COLLATE pg_catalog."default",
shift character varying(200) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
PRIMARY KEY(storeid,userid)
);

CREATE INDEX idx_users_schedules_s ON users_schedules (storeid);
CREATE INDEX idx_users_schedules_u ON users_schedules (userid);
CREATE INDEX idx_users_schedules_su ON users_schedules (storeid,userid);

CREATE TABLE IF NOT EXISTS public.agency
(  
 id serial PRIMARY KEY,
agencyid character varying(50) COLLATE pg_catalog."default",
name character varying(100) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(agencyid)
);

CREATE TABLE IF NOT EXISTS public.areas
(  
 id serial PRIMARY KEY,
areaid character varying(50) COLLATE pg_catalog."default",
name character varying(50) COLLATE pg_catalog."default",
agencyid character varying(50) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(areaid)
);

CREATE TABLE IF NOT EXISTS public.chains
(
id serial PRIMARY KEY,
chainid character varying(50) COLLATE pg_catalog."default",
name character varying(50) COLLATE pg_catalog."default",
agencyid character varying(50) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(chainid)
);

CREATE TABLE IF NOT EXISTS public.category
(
id serial PRIMARY KEY,
catid integer not null,
name character varying(50) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS public.category_refs
(
id serial PRIMARY KEY,
refsid integer,
catid integer,
cat_name text,
segment character varying(100) COLLATE pg_catalog."default" DEFAULT 'NA'::character varying,
brand character varying(100) COLLATE pg_catalog."default" DEFAULT 'NA'::character varying,
percent_share character varying(50) COLLATE pg_catalog."default" DEFAULT 'NA'::character varying,
facing_count character varying(50) COLLATE pg_catalog."default" DEFAULT 'NA'::character varying,
pulloutday character varying(50) COLLATE pg_catalog."default" DEFAULT 'NA'::character varying,
facing_segment character varying(255) COLLATE pg_catalog."default",
facing_brand character varying(255) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(catid,refsid)
);

CREATE TABLE IF NOT EXISTS public.stores
(
id serial PRIMARY KEY,
channelid text,
chainid text,
areaid text,
storecode text,
storeid text,
name text,
zipcode text,
geofence integer,
longitude text,
latitude text,
address text,
priority character varying(10) COLLATE pg_catalog."default" DEFAULT '1'::character varying,
active character varying(3) COLLATE pg_catalog."default" NOT NULL DEFAULT 'Yes'::character varying,
groupname bigint NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
agencyid text COLLATE pg_catalog."default" DEFAULT 'MNC'::text,
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(storeid)
);

CREATE INDEX idx_stores ON stores (storeid);
CREATE INDEX idx_stores_cd ON stores (date_created);

CREATE TABLE IF NOT EXISTS public.stores_skus
(
id serial PRIMARY KEY,
skuid character varying(255) COLLATE pg_catalog."default",
storeid character varying(50) COLLATE pg_catalog."default",
stock_per_piece integer,
stock_per_case integer,
carry character varying(10) COLLATE pg_catalog."default",
date_created timestamp with time zone DEFAULT now(),
date_updated timestamp with time zone DEFAULT now(),
UNIQUE(storeid,skuid)
);

CREATE INDEX idx_stores_skus_skus ON stores_skus (skuid,storeid);
CREATE INDEX idx_stores_skus_du ON stores_skus (storeid,date_updated);

//copy old data : insert into tbl_location_logs_v2 select \* from tbl_location_logs where datetime_log::date = '2021-06-01'
CREATE TABLE IF NOT EXISTS public.tbl_location_logs_y21
(
id SERIAL,
tbluserid character varying(255),
mgenerated_id character varying(255),
module character varying(255),
event text,
current_longitude character varying(50) ,
current_latitude character varying(50) ,
end_longitude character varying(50),
end_latitude character varying(50),
gps_accuracy real,
gps_provider character varying(5000),
battery integer,
datetime_log timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
netinfo character varying(600),
device_id character varying(255),
tblstoreid character varying(255)
) PARTITION BY RANGE (datetime_log);

//PG 10 not supported should only applies in Child Partitions
CREATE INDEX idx_user_mod_store_dt_evt ON tbl_location_logs_y21 (tbluserid,module,event,tblstoreid,datetime_log);
CREATE INDEX idx_mod_dt_evt ON tbl_location_logs_y21 (module,event,datetime_log);
CREATE INDEX idx_user_mod_dt_evt ON tbl_location_logs_y21 (tbluserid,module,event,datetime_log);

CREATE TABLE tbl_location_logs_v3_y21p1 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE tbl_location_logs_v3_y21p2 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE tbl_location_logs_v3_y21p3 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE tbl_location_logs_v3_y21p4 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE tbl_location_logs_v3_y22p1 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2021-12-01') TO ('2022-03-01');
CREATE TABLE tbl_location_logs_v3_y22p2 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2022-03-01') TO ('2022-06-01');
CREATE TABLE tbl_location_logs_v3_y22p3 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2022-06-01') TO ('2022-09-01');
CREATE TABLE tbl_location_logs_v3_y22p4 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2022-09-01') TO ('2022-12-01');

CREATE TABLE tbl_location_logs_v3_y23p1 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2022-12-01') TO ('2023-03-01');
CREATE TABLE tbl_location_logs_v3_y23p2 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2023-03-01') TO ('2023-06-01');
CREATE TABLE tbl_location_logs_v3_y23p3 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2023-06-01') TO ('2023-09-01');
CREATE TABLE tbl_location_logs_v3_y23p4 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2023-09-01') TO ('2023-12-01');

CREATE TABLE tbl_location_logs_v3_y24p1 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2023-12-01') TO ('2024-03-01');
CREATE TABLE tbl_location_logs_v3_y24p2 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2024-03-01') TO ('2024-06-01');
CREATE TABLE tbl_location_logs_v3_y24p3 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2024-06-01') TO ('2024-09-01');
CREATE TABLE tbl_location_logs_v3_y24p4 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2024-09-01') TO ('2024-12-01');

//copy backup
insert into tbl_daily_stock_products_bkp select \* from tbl_daily_stock_products where
date_created::date >= '2021-06-24' and date_created::date <= '2021-06-25'

DELETE
FROM tbl_daily_stock_products_bkp
a USING (SELECT MAX(tbldailystockproductssid) as mid,mobile_generated_id
FROM tbl_daily_stock_products_bkp
GROUP BY mobile_generated_id HAVING COUNT(\*) > 1)
b WHERE a.mobile_generated_id = b.mobile_generated_id
AND a.date_created::date >= '2021-06-24'
AND a.date_created::date <= '2021-06-25'
AND a.tbldailystockproductssid <> b.mid;

//copy old data : insert into tbl_daily_stock_products_v2 select \* from tbl_daily_stock_products where date_created::date >= '2021-01-01' and date_created::date <= '2021-01-15'
CREATE TABLE public.tbl_daily_stock_products_v2
(
tbldailystockproductssid serial primary key,
tbluserid character varying(255),
tblskuid character varying(255),
tbldailystocksid integer,
mobiledailystocksid integer,
mobile_generated_id character varying(255),
tblstoreid character varying(50),
image_path character varying(200),
dailystock_status character varying(100),
begin_inventory real,
delivery_today real,
total_deliveries real,
bad_order real,
total_bad_orders real,
transfer_incoming real,
total_transfer_incoming real,
transfer_outgoing real,
total_transfer_outgoing real,
display character varying(255) ,
offtake real,
total_offtake real,
system_offtake real,
average_offtake real,
offtake_status character varying(50),
ending_inventory real,
product_remaining_cases integer,
product_remaining_pieces integer,
sys_discrepancy character varying(10),
stock_out character varying(50),
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
out_of_stock character varying(255)
) PARTITION BY RANGE (date_created);

CREATE TABLE tbl_daily_stock_products_v2_y21p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y21p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y21p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y21p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y22p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2021-12-01') TO ('2022-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y22p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2022-03-01') TO ('2022-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y22p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2022-06-01') TO ('2022-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y22p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2022-09-01') TO ('2022-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y23p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2022-12-01') TO ('2023-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y23p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2023-03-01') TO ('2023-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y23p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2023-06-01') TO ('2023-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y23p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2023-09-01') TO ('2023-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y24p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2023-12-01') TO ('2024-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y24p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-03-01') TO ('2024-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y24p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-06-01') TO ('2024-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y24p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-09-01') TO ('2024-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y25p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-12-01') TO ('2025-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-03-01') TO ('2025-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-06-01') TO ('2025-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-09-01') TO ('2025-12-01');

delete from tbl_daily_stock_products_v2 where
tbldailystockproductssid not in (
select min(tbldailystockproductssid) from tbl_daily_stock_products_v2 where
mobile_generated_id is not NULL group by mobile_generated_id
)
AND mobile_generated_id is not NULL
AND date_created::date >= '2021-06-16'
AND date_created::date <= '2021-06-30'

CREATE TABLE public.tbl_shelf_availability_audit_store_v2
(
tblshelfidstore serial primary key,
tbluserid character varying(255),
tblstoreid character varying(50),
mobile_generated_id character varying(255) ,
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
server_id character varying(255),
) PARTITION BY RANGE (date_created);

CREATE TABLE tbl_daily_stock_products_v2_y21p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y21p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y21p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y21p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y22p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2021-12-01') TO ('2022-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y22p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2022-03-01') TO ('2022-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y22p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2022-06-01') TO ('2022-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y22p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2022-09-01') TO ('2022-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y23p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2022-12-01') TO ('2023-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y23p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2023-03-01') TO ('2023-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y23p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2023-06-01') TO ('2023-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y23p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2023-09-01') TO ('2023-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y24p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2023-12-01') TO ('2024-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y24p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-03-01') TO ('2024-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y24p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-06-01') TO ('2024-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y24p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-09-01') TO ('2024-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y25p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-12-01') TO ('2025-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-03-01') TO ('2025-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-06-01') TO ('2025-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-09-01') TO ('2025-12-01');

CREATE TABLE public.tbl_shelf_availability_audit_sku_v2
(
tblshelfidssku serial primary key,
tblskuid character varying(255) COLLATE pg_catalog."default",
availability character varying(255) COLLATE pg_catalog."default",
mobile_generated_id character varying(255) COLLATE pg_catalog."default",
date_created timestamp without time zone,
date_updated timestamp without time zone,
date_sync timestamp with time zone DEFAULT now(),
sku_generated_id character varying(255) COLLATE pg_catalog."default",
CONSTRAINT tbl_shelf_availability_audit_sku_pkey PRIMARY KEY (tblshelfidssku)
)

CREATE TABLE tbl_daily_stock_products_v2_y25p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2024-12-01') TO ('2025-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-03-01') TO ('2025-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-06-01') TO ('2025-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y25p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-09-01') TO ('2025-12-01');

CREATE TABLE tbl_daily_stock_products_v2_y26p1 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2025-12-01') TO ('2026-03-01');
CREATE TABLE tbl_daily_stock_products_v2_y26p2 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2026-03-01') TO ('2026-06-01');
CREATE TABLE tbl_daily_stock_products_v2_y26p3 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2026-06-01') TO ('2026-09-01');
CREATE TABLE tbl_daily_stock_products_v2_y26p4 PARTITION OF tbl_daily_stock_products_v2
FOR VALUES FROM ('2026-09-01') TO ('2026-12-01');

CREATE TABLE tbl_location_logs_v3_y25p1 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2024-12-01') TO ('2025-03-01');
CREATE TABLE tbl_location_logs_v3_y25p2 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2025-03-01') TO ('2025-06-01');
CREATE TABLE tbl_location_logs_v3_y25p3 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2025-06-01') TO ('2025-09-01');
CREATE TABLE tbl_location_logs_v3_y25p4 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2025-09-01') TO ('2025-12-01');

CREATE TABLE tbl_location_logs_v3_y26p1 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2025-12-01') TO ('2026-03-01');
CREATE TABLE tbl_location_logs_v3_y26p2 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2026-03-01') TO ('2026-06-01');
CREATE TABLE tbl_location_logs_v3_y26p3 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2026-06-01') TO ('2026-09-01');
CREATE TABLE tbl_location_logs_v3_y26p4 PARTITION OF tbl_location_logs_v3
FOR VALUES FROM ('2026-09-01') TO ('2026-12-01');

CREATE TABLE tbl_shelf_availability_audit_store_v2_y21p1 PARTITION OF tbl_shelf_availability_audit_store_v2
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE tbl_shelf_availability_audit_store_v2_y21p2 PARTITION OF tbl_shelf_availability_audit_store_v2
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE tbl_shelf_availability_audit_store_v2_y21p3 PARTITION OF tbl_shelf_availability_audit_store_v2
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE tbl_shelf_availability_audit_store_v2_y21p4 PARTITION OF tbl_shelf_availability_audit_store_v2
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

CREATE TABLE tbl_shelf_availability_audit_sku_v2_y21p1 PARTITION OF tbl_shelf_availability_audit_sku_v2
FOR VALUES FROM ('2020-12-01') TO ('2021-03-01');
CREATE TABLE tbl_shelf_availability_audit_sku_v2_y21p2 PARTITION OF tbl_shelf_availability_audit_sku_v2
FOR VALUES FROM ('2021-03-01') TO ('2021-06-01');
CREATE TABLE tbl_shelf_availability_audit_sku_v2_y21p3 PARTITION OF tbl_shelf_availability_audit_sku_v2
FOR VALUES FROM ('2021-06-01') TO ('2021-09-01');
CREATE TABLE tbl_shelf_availability_audit_sku_v2_y21p4 PARTITION OF tbl_shelf_availability_audit_sku_v2
FOR VALUES FROM ('2021-09-01') TO ('2021-12-01');

insert into tbl_shelf_availability_audit_sku_v2
select \* from tbl_shelf_availability_audit_sku where
date_created::date >= '2021-06-01' and date_created::date <= '2021-06-30'
