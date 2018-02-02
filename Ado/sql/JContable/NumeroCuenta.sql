SELECT
	codcuenta as [Numero de Cuenta]
FROM
	MovimientosTabla INNER JOIN ADO ON MovimientosTabla.CUENTA = ado.CUENTA2
WHERE
	cuenta=?
GROUP BY
	cuenta
HAVING
	cuenta