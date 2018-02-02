SELECT
	sum(debe - haber) as ''
FROM
	MovimientosTabla
WHERE
	cuenta=?
	AND fecha between date('NOW', 'START OF YEAR') and date('NOW')
GROUP BY
	cuenta
HAVING
	cuenta