SELECT
    sum(debe - haber) as ''
FROM
    MovimientosTabla
WHERE
    cuenta=?
GROUP BY
    cuenta
HAVING
    cuenta