SELECT 
	strftime('%Y', fecha) as YEAR, 
	sum(case strftime('%m', fecha) when '01' then (DEBE-HABER) else 0 end) Ene, 
	sum(case strftime('%m', fecha) when '02' then (DEBE-HABER) else 0 end) Feb, 
	sum(case strftime('%m', fecha) when '03' then (DEBE-HABER) else 0 end) Mar, 
	sum(case strftime('%m', fecha) when '04' then (DEBE-HABER) else 0 end) Abr,
	sum(case strftime('%m', fecha) when '05' then (DEBE-HABER) else 0 end) May,
	sum(case strftime('%m', fecha) when '06' then (DEBE-HABER) else 0 end) Jun, 
	sum(case strftime('%m', fecha) when '07' then (DEBE-HABER) else 0 end) Jul,
	sum(case strftime('%m', fecha) when '08' then (DEBE-HABER) else 0 end) Ago,
	sum(case strftime('%m', fecha) when '09' then (DEBE-HABER) else 0 end) Sep, 
	sum(case strftime('%m', fecha) when '10' then (DEBE-HABER) else 0 end) Oct,
	sum(case strftime('%m', fecha) when '11' then (DEBE-HABER) else 0 end) Nov, 
	sum(case strftime('%m', fecha) when '12' then (DEBE-HABER) else 0 end) Dic 
FROM  
	MovimientosTabla
WHERE 
	cuenta = '1-01-02-002  Banco Chile Pesos 886-00940-05 TEAM CHILE' 
	and fecha between date('NOW', 'START OF YEAR') and date('NOW')
group by 
	YEAR
order by 
	YEAR desc