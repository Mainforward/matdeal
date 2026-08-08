erDiagram

    Store ||--o{ StoreProduct : sells
    Product ||--o{ StoreProduct : represented_as
    StoreProduct ||--o{ PriceHistory : has

    Store {
        uuid id
        string chain
        string name
        string city
        datetime created_at
        datetime updated_at
    }

    Product {
        uuid id
        string ean
        string name
        string brand
        decimal size_value
        string size_unit
        string category
        string image_url
        datetime created_at
        datetime updated_at
    }

    StoreProduct {
        uuid id
        uuid store_id
        uuid product_id
        string external_id
        string external_name
        string external_url
        boolean available
        datetime created_at
        datetime updated_at
    }

    PriceHistory {
        uuid id
        uuid store_product_id
        decimal price
        string currency
        datetime captured_at
    }