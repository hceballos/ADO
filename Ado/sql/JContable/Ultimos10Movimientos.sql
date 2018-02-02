SELECT
  lower(descripcion) as DESCRIPCION,
  lower(nombre) as NOMBRE,
  fecha, N_comprobante as VOUCHER,
  debe as CARGOS, haber as ABONOS
FROM
  MovimientosTabla LEFT OUTER JOIN complemento ON MovimientosTabla.AUXILIAR = complemento.rut
WHERE
  cuenta=?
  and fecha between date('NOW', '-5 YEARS',  'START OF YEAR') and date('NOW')
ORDER BY
  fecha desc
LIMIT 10