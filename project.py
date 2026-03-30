import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# ---------------------------

# MySQL Database Connection
# ---------------------------
host="localhost",
user="root",
password="12345",
database="miniproject1"
#---------------------------
engine = create_engine("mysql+pymysql://root:12345@localhost/miniproject1")



#SQL Queries for task
# ------------------------------------

queries = {
    #---Magnitude & Depth---

'1.Top 10 strongest earthquakes (mag)':
"""Select * from earthquake order by mag desc limit 10;""",
'2.Top 10 deepest earthquakes (depth_km)':
"""select * from earthquake order by depth_km  limit 10;""",
'3.Shallow earthquakes < 50 km and mag > 7.5':
"""select * from earthquake where depth_km < 50 and mag > 7.5;""",
'4.Average depth per continent':
"""select 'continent logic not available in DB' as note;""",
'5.Average magnitude per magnitude type':
"""select mag-type, avg(mag) as avg_mag
from earthquake
group by mag-type;""",
'6.Year with most earthquakes':
"""select year(time)as year,count(*)as total
from earthquake
group by year(time)
order by total desc 
limit 1;""",
'7.Month with highest earthquakes':
"""select month(time)as month, count(*) as total
from earthquake
group by month(time)
order by total desc
limit 1;""",
'8.Day of week with most earthquakes':
"""select dayname(time) as day, count(*) as total
from earthquake
group by dayname(time)
order by total desc;""",
'9.Count of earthquakes per hour':
"""select hour(time) as hour, count(*) as total
from earthquake
group by hour(time)
order by hour;""",
'10.Most active reporting network':
"""select net,count(*) as total
from earthquake
group by net 
order by total desc
limit 1;""",
'11.Top 5 places with highest casualties':
"""select place as casualities 
from earthquake
group by place
order by casualities desc
limit 5;""",
'12.Total economic loss per continent':
"""select 'Not available - no economic loss column' as note;""",
'13.Average economic loss by alert level':
"""select alert, count(*) as count 
from earthquake
group by alert;""",
'14.Count of reviewed vs automatic (status)':
"""select status, count(*) as total
from earthquake
group by status;""",
'15.Count by earthquake type':
"""select type, count(*) as count_of_earthquake
from earthquake
group by type;""",
'16.Number of earthquakes by data type (types)':
"""select types,count(*) as total 
from earthquake 
group by types;""",
'17.Avg RMS and gap per continent':
"""select 'Continent mapping not available' as note;""",
'18.Events with high station coverage (nst > 50)':
"""select *
from earthquake
where nst > 50;""",
'19.Number of tsunamis per year':
"""select year(time)as year,count(*)as tsunamis
from earthquake
where tsunami = 1
group by year (time);""",
'20.Top 5 countries with highest avg magnitude (past 10 yrs)':
"""select place,avg(mag) as avg_mag
from earthquake
group by place
order by avg_mag desc
limit 5;""",
'21.Countries with both shallow & deep EQ same month':
"""select place
from earthquake
group by place,year(time),month(time)
having 
sum(depth_km < 70) > 0
and SUM(depth_km > 300) > 0;""",
'22.Compute the year-over-year growth rate':
"""select year,total,lag(total) over (order by year) AS previous_year,
round(((total - lag(total) over (order by year)) / lag(total) over (order by year)) * 100, 2) as growth_rate
from (select year as year, count(*) as total from earthquake
group by year ) as yearly;""",
'23.Top 3 most seismically active regions':
"""select place,
       count(*) as frequency,
       avg(mag) as avg_mag,
       (count(*)*avg(mag)) as score
from earthquake
group by place
order by score desc
limit 3;""",
'24.Average depth within ±5° of equator':
"""select place, avg(depth_km) as avg_depth
from earthquake
where latiude between -5 and 5
group by place;""",
'25.Countries with highest shallow-to-deep ratio':
"""select place,
sum(depth_km < 70) as shallow,
sum(depth_km > 300) as deep,
sum(depth_km < 70) / nullif(sum(depth_km > 300), 0) as ratio
from earthquake
group by place
order by ratio desc;""",
'26.Avg magnitude difference (tsunami vs non-tsunami)':
"""select
    (select avg(mag) from earthquake where tsunami = 1) as tsunami_avg,
    (select avg(mag) from earthquake where tsunami = 0) as no_tsunami_avg,
    (select avg(mag) from earthquake where tsunami = 1)-
    (select avg(mag) from earthquake where tsunami = 0) as difference;""",
'27.Events with lowest data reliability (gap & rms)':
"""select *
from earthquake
order by gap desc, rms desc
limit 20;""",
'28.Consecutive EQ within 50km & 1 hour':
"""select 'Requires advanced spatial logic' as note;""",
'29.Regions with highest deep-focus EQ (>300 km)':
"""select place,count(*) as deep_events
from earthquake
where depth_km > 300
group by place 
order by deep_events desc;""",
}

# Streamlit UI "🌍"
st.title(" Earthquake Data Analysis Dashboard")
st.write("Select any problem statement (1-40) to run the corresponding SQL query.")
#Dropdown
task = st.selectbox("Choose Task Number", list(queries.keys()))
#Run button
if st.button("Run Query"):
   query = queries[task]  
   df = pd.read_sql(query, engine)     

   st.subheader(f"Results for: {task}") 
   st.dataframe(df, use_container_width=True)



