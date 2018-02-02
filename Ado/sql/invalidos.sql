SELECT
	cuenta,
	fecha,
	N_Comprobante as voucher,
	auxiliar,
	debe,
	haber,
	descripcion
FROM
	MovimientosTabla
WHERE
	auxiliar=?