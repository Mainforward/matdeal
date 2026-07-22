erDiagram

    Store ||--o{ StoreProduct : sells

    Product ||--o{ StoreProduct : represented_as

    StoreProduct ||--o{ PriceHistory : has

    Store {
        uuid id
        string chain
        string name
        string city
    }

    Product {
        uuid id
        string ean
        string brand
        string name
        decimal size_value
        string size_unit
        string category
    }

    StoreProduct {
        uuid id
        uuid store_id
        uuid product_id
        string external_id
        string external_name
        string external_url
        boolean available
    }

    PriceHistory {
        uuid id
        uuid store_product_id
        decimal price
        string currency
        datetime captured_at
    }