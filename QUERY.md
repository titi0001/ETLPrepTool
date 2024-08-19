 # A Entrega do resultado deve ser um arquivo contendo as consultas SQL.

 ##### Postgres: Banco de dados utilizado para construção das queries.

 ---
 ##### Arquivos usado para aplicar o teste
 ##### [Cliente](./csv/dCliente.csv)
 ##### [Produto](./csv/dCliente.csv)
 ##### [Metas](./csv/dCliente.csv)
 ##### [Vendas](./csv/dCliente.csv)
 ---
 ##### foi criado um ambiente de desenvolvimento dinamico na raiz do projeto link abaixo
 #####  [Ambiente de teste](README.md)
---

 
 <details>
   <summary><strong> 1. Crie consultas demonstrar o valor total em faturamento, o ticket médio por pedido e o tempo médio entre a realização de um pedido e a saída para entrega; </strong></summary>

```sql
WITH 
TotalFaturamento AS (
    SELECT SUM(fv.OrderQuantity * dp.UnitPrice) AS ValorTotal
    FROM fVendas fv
    JOIN dProduto dp ON fv.ProductKey = dp.ProductKey
    WHERE fv.OrderDate IS NOT NULL
),

TicketMedioPorPedido AS (
    SELECT AVG(fv.OrderQuantity * dp.UnitPrice) AS TicketMedio
    FROM fVendas fv
    JOIN dProduto dp ON fv.ProductKey = dp.ProductKey
    WHERE fv.OrderDate IS NOT NULL
    GROUP BY fv.SalesOrderNumber
),

TempoMedioEntrega AS (
    SELECT FLOOR(AVG(EXTRACT(EPOCH FROM (fv.ShipDate - fv.OrderDate)) / 86400)) AS TempoMedioDias
    FROM fVendas fv
    WHERE fv.OrderDate IS NOT NULL
)

SELECT 
    'R$ ' || TO_CHAR((SELECT ValorTotal FROM TotalFaturamento), 'FM999,999,999,990.00') AS "Valor Total em Faturamento",
    'R$ ' || TO_CHAR((SELECT AVG(TicketMedio) FROM TicketMedioPorPedido), 'FM999,999,999,990.00') AS "Ticket Médio por Pedido",
    TO_CHAR((SELECT TempoMedioDias FROM TempoMedioEntrega), 'FM999999990') AS "Tempo Médio entre Pedido e Entrega (dias)";
```
##### Resultado 
 ![01](/images/01.png)
 </details>

 <details>
    <summary><strong> 2. Crie uma forma de visualizar os valores de meta x realizado por país e por ano; </strong></summary>

```sql
WITH FaturamentoPorPaisAno AS (
    SELECT
        c.CountryName AS Pais,
        EXTRACT(YEAR FROM v.OrderDate) AS Ano,
        SUM(v.OrderQuantity * p.UnitPrice) AS Faturamento_Realizado
    FROM
        fVendas v
    JOIN
        dProduto p ON v.ProductKey = p.ProductKey
    JOIN
        dCliente c ON v.CustomerKey = c.CustomerKey
    GROUP BY
        c.CountryName,
        EXTRACT(YEAR FROM v.OrderDate)
),
MetasPorPaisAno AS (
    SELECT
        m.Pais,
        m.Ano,
        SUM(m.Meta) AS Meta_Anual
    FROM
        fMetas m
    GROUP BY
        m.Pais,
        m.Ano
)
SELECT
    m.Pais,
    m.Ano,
    TO_CHAR(COALESCE(m.Meta_Anual, 0), 'FM"R$"999G999G999D00') AS Meta_Anual,
    TO_CHAR(COALESCE(f.Faturamento_Realizado, 0), 'FM"R$"999G999G999D00') AS Faturamento_Realizado,
    TO_CHAR(COALESCE(f.Faturamento_Realizado, 0) - COALESCE(m.Meta_Anual, 0), 'FM"R$"999G999G999D00') AS Diferenca
FROM
    MetasPorPaisAno m
LEFT JOIN
    FaturamentoPorPaisAno f ON m.Pais = f.Pais AND m.Ano = f.Ano
ORDER BY
    m.Pais,
    m.Ano DESC;
```
##### Resultado 
 ![02](/images/02.png)
 </details>

 <details>
    <summary><strong> 3. Identifique quem é o melhor comprador de cada país e quanto este comprador gastou por ano; </strong></summary>

```sql
WITH GastosPorClienteAno AS (
    SELECT
        c.CountryName AS Pais,
        EXTRACT(YEAR FROM v.OrderDate) AS Ano,
        c.CustomerKey,
        c.Customer AS Nome_Cliente,
        SUM(v.OrderQuantity * p.UnitPrice) AS Gasto_Total
    FROM
        fVendas v
    JOIN
        dProduto p ON v.ProductKey = p.ProductKey
    JOIN
        dCliente c ON v.CustomerKey = c.CustomerKey
    GROUP BY
        c.CountryName,
        EXTRACT(YEAR FROM v.OrderDate),
        c.CustomerKey,
        c.Customer
),
MelhorCompradorPorPaisAno AS (
    SELECT
        Pais,
        Ano,
        CustomerKey,
        Nome_Cliente,
        Gasto_Total,
        RANK() OVER (PARTITION BY Pais, Ano ORDER BY Gasto_Total DESC) AS Ranking
    FROM
        GastosPorClienteAno
)
SELECT
    Pais,
    Ano,
    Nome_Cliente AS Melhor_Comprador,
    TO_CHAR(Gasto_Total, 'FM"R$"999G999G999D00') AS Gasto_Total
FROM
    MelhorCompradorPorPaisAno
WHERE
    Ranking = 1
ORDER BY
    Pais,
    Ano DESC;
```
##### Resultado 
 ![03](/images/03.png)
</details>

<details>
    <summary><strong>  4. Demonstre qual é o produto mais vendido por categoria </strong></summary>

```sql
WITH VendasPorProdutoCategoria AS (
    SELECT
        p.CategoryName AS Categoria,
        p.ProductKey,
        p.ProductName AS Produto,
        SUM(v.OrderQuantity) AS Quantidade_Vendida
    FROM
        fVendas v
    JOIN
        dProduto p ON v.ProductKey = p.ProductKey
    GROUP BY
        p.CategoryName,
        p.ProductKey,
        p.ProductName
),
MaisVendidoPorCategoria AS (
    SELECT
        Categoria,
        Produto,
        Quantidade_Vendida,
        RANK() OVER (PARTITION BY Categoria ORDER BY Quantidade_Vendida DESC) AS Ranking
    FROM
        VendasPorProdutoCategoria
)
SELECT
    Categoria,
    Produto AS Produto_Mais_Vendido,
    Quantidade_Vendida
FROM
    MaisVendidoPorCategoria
WHERE
    Ranking = 1
ORDER BY
    Quantidade_Vendida DESC;
```
##### Resultado 
 ![04](/images/04.png)
</details>

<details>
    <summary><strong> 5. Demonstre quantos e quais produtos venderam mais de 1 milhão em faturamento no ltv; </strong></summary>

```sql
WITH FaturamentoPorProduto AS (
    SELECT 
        p.ProductKey,
        p.ProductName,
        SUM(v.OrderQuantity) AS Quantidade_Vendida,
        SUM(v.OrderQuantity * p.UnitPrice) AS Faturamento_Total
    FROM 
        fVendas v
    JOIN 
        dProduto p ON v.ProductKey = p.ProductKey
    GROUP BY 
        p.ProductKey, p.ProductName
)
SELECT 
    ProductKey,
    ProductName,
    Quantidade_Vendida,
    TO_CHAR(Faturamento_Total, 'FM"R$"999G999G999D00') AS FaturamentoLTV
FROM 
    FaturamentoPorProduto
WHERE 
    Faturamento_Total > 1000000
ORDER BY 
    Quantidade_Vendida DESC;

```
##### Resultado 
 ![05](/images/05.png)
</details>

<details>
    <summary><strong> 6. Crie um ranking de quais cidades mais trouxeram receita; </strong></summary>

```sql
WITH ReceitaPorCidade AS (
    SELECT
        c.CityName AS Cidade,
        c.StateName AS Estado,
        c.CountryName AS Pais,
        SUM(v.OrderQuantity * p.UnitPrice) AS Receita_Total
    FROM
        fVendas v
    JOIN
        dProduto p ON v.ProductKey = p.ProductKey
    JOIN
        dCliente c ON v.CustomerKey = c.CustomerKey
    GROUP BY
        c.CityName,
        c.StateName,
        c.CountryName
)
SELECT
    RANK() OVER (ORDER BY Receita_Total DESC) AS Ranking,
    Cidade,
    Estado,
    Pais,
    TO_CHAR(Receita_Total, 'FM"R$"999G999G999D00') AS Receita_Total
FROM
    ReceitaPorCidade
ORDER BY
    Ranking ASC;

```
##### Resultado 
 ![06](/images/06.png)
</details>

<details>
    <summary><strong> 7. Crie um ranking de quais cidades menos trouxeram receita; </strong></summary>

```sql
WITH ReceitaPorCidade AS (
    SELECT
        c.CityName AS Cidade,
        c.StateName AS Estado,
        c.CountryName AS Pais,
        SUM(v.OrderQuantity * p.UnitPrice) AS Receita_Total
    FROM
        fVendas v
    JOIN
        dProduto p ON v.ProductKey = p.ProductKey
    JOIN
        dCliente c ON v.CustomerKey = c.CustomerKey
    GROUP BY
        c.CityName,
        c.StateName,
        c.CountryName
)
SELECT
    RANK() OVER (ORDER BY Receita_Total ASC) AS Ranking,
    Cidade,
    Estado,
    Pais,
    TO_CHAR(Receita_Total, 'FM"R$"999G999G999D00') AS Receita_Total
FROM
    ReceitaPorCidade
ORDER BY
    Ranking ASC;
```
##### Resultado 
 ![07](/images/07.png)
</details>

<details>
    <summary><strong> 8. Demonstre quanto cada tipo de negócio contribuiu percentualmente para o faturamento total no LTV; </strong></summary>
    
```sql
WITH FaturamentoPorNegocio AS (
    SELECT
        c.BusinessType AS Tipo_Negocio,
        SUM(v.OrderQuantity * p.UnitPrice) AS LTV_Faturamento_Total
    FROM
        fVendas v
    JOIN
        dProduto p ON v.ProductKey = p.ProductKey
    JOIN
        dCliente c ON v.CustomerKey = c.CustomerKey
    GROUP BY
        c.BusinessType
),
FaturamentoTotal AS (
    SELECT
        SUM(LTV_Faturamento_Total) AS LTV_Faturamento_Geral
    FROM
        FaturamentoPorNegocio
)
SELECT
    fn.Tipo_Negocio,
    TO_CHAR(fn.LTV_Faturamento_Total, 'FM"R$"999G999G999D00') AS Faturamento_Total_LTV,
    TO_CHAR((fn.LTV_Faturamento_Total / ft.LTV_Faturamento_Geral) * 100, 'FM990.00') || '%' AS Percentual_Contribuicao
FROM
    FaturamentoPorNegocio fn,
    FaturamentoTotal ft
ORDER BY
    (fn.LTV_Faturamento_Total / ft.LTV_Faturamento_Geral) DESC;
```
##### Resultado 
 ![08](/images/08.png)
</details>

 ## ERD do DB 
![ERD](/images/ERD.png)


>!OBS:
>>Para a coluna **ProductSize** da tabela **dProduto**
>>Uma boa prática seria separar os dados como o número e a unidade de medida 