SELECT
    DISTINCT auxiliar
FROM
    MovimientosTabla
WHERE
  auxiliar!=''
  and fecha between DATE('NOW', '-1 YEARS', 'START OF YEAR') AND  DATE('NOW', 'START OF YEAR')
ORDER BY
    auxiliar ASC