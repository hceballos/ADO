SELECT
    ACTIVO_CORRIENTE,
    PASIVO_CORRIENTE
FROM
    (
    SELECT
        sum(debe-haber) as ACTIVO_CORRIENTE
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