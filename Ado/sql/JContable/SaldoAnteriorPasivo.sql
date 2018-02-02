SELECT
    strftime('%Y', fecha) as YEAR,
    sum(case strftime('%m', fecha) when '01' then (HABER-DEBE) else 0 end) Ene,
    sum(case strftime('%m', fecha) when '02' then (HABER-DEBE) else 0 end) Feb,
    sum(case strftime('%m', fecha) when '03' then (HABER-DEBE) else 0 end) Mar,
    sum(case strftime('%m', fecha) when '04' then (HABER-DEBE) else 0 end) Abr,
    sum(case strftime('%m', fecha) when '05' then (HABER-DEBE) else 0 end) May,
    sum(case strftime('%m', fecha) when '06' then (HABER-DEBE) else 0 end) Jun,
    sum(case strftime('%m', fecha) when '07' then (HABER-DEBE) else 0 end) Jul,
    sum(case strftime('%m', fecha) when '08' then (HABER-DEBE) else 0 end) Ago,
    sum(case strftime('%m', fecha) when '09' then (HABER-DEBE) else 0 end) Sep,
    sum(case strftime('%m', fecha) when '10' then (HABER-DEBE) else 0 end) Oct,
    sum(case strftime('%m', fecha) when '11' then (HABER-DEBE) else 0 end) Nov,
    sum(case strftime('%m', fecha) when '12' then (HABER-DEBE) else 0 end) Dic
FROM
    MovimientosTabla
WHERE
    cuenta =?
    and fecha between DATE('NOW', '-1 YEARS', 'START OF YEAR') AND  DATE('NOW', 'START OF YEAR')
group by
    YEAR
order by
    YEAR desc