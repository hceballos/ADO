SELECT
	sum(haber - debe) as ''
FROM
	MovimientosTabla
WHERE
	cuenta=?
GROUP BY
	cuenta
HAVING
	cuenta