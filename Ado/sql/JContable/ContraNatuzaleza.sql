SELECT
    centro_de_costo as [C. COSTO],
    lower(nombreccosto) as NOMBRE,
    sum (debe - haber) as SALDO
FROM
    MovimientosTabla INNER JOIN Ccostos ON MovimientosTabla.centro_de_costo = Ccostos.ccosto
WHERE
    cuenta=?
GROUP BY
    centro_de_costo
HAVING
    centro_de_costo and SALDO
ORDER BY
    SALDO desc LIMIT 10
