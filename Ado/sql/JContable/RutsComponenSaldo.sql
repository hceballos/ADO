SELECT
  auxiliar,
  lower(nombre) as NOMBRE,
  sum (debe - haber) as SALDO
FROM
  MovimientosTabla LEFT OUTER JOIN complemento ON MovimientosTabla.auxiliar = complemento.rut
WHERE
  cuenta=?
  and fecha between date('NOW', '-5 YEARS',  'START OF YEAR') and date('NOW')
  and auxiliar and SALDO
ORDER BY
  SALDO desc
LIMIT 10
