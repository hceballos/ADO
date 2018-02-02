SELECT
    ROUND (ACTIVO_CORRIENTE / PASIVO_CORRIENTE ,2) as Liquidez
FROM
    (
    SELECT
        sum(debe-haber)*1.0 as ACTIVO_CORRIENTE
    FROM
        movimientosTabla
    WHERE
        cuenta like '1-01-0%'
    )

LEFT JOIN
    (
    SELECT
        sum(haber-debe) as PASIVO_CORRIENTE
    FROM
        movimientosTabla
    WHERE
        cuenta like '2-01-%'
    )