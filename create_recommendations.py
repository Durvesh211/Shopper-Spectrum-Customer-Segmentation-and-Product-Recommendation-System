import joblib
import os
import sqlite3

INPUT_FILE = "product_similarity.pkl"
OUTPUT_FILE = "top20_recommendations.db"
TOP_K =20

print( "File Loading")

similarity_df = joblib.load(INPUT_FILE)
print(f"Products found: {len(similarity_df)}")

connection = sqlite3.connect(OUTPUT_FILE)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        product TEXT NOT NULL,
        rank INTEGER NOT NULL,
        recommended_product TEXT NOT NULL,
        similarity REAL NOT NULL,
        PRIMARY KEY (product, rank)
    )
""")

print("Generating Top-20 recommendations...")

for product in similarity_df.columns:
    similarities = similarity_df[product]

    # Remove the product itself
    similarities = similarities.drop(product, errors="ignore")

    # Get the top 20
    top_products = similarities.nlargest(TOP_K)

    for rank, (recommended_product, similarity) in enumerate(
        top_products.items(), start=1
    ):
        cursor.execute(
            """
            INSERT OR REPLACE INTO recommendations
            (product, rank, recommended_product, similarity)
            VALUES (?, ?, ?, ?)
            """,
            (
                product,
                rank,
                recommended_product,
                float(similarity),
            ),
        )

    if len(top_products) > 0:
        print(f"Processed: {product[:60]}")

connection.commit()

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_product
    ON recommendations(product)
""")

connection.commit()
connection.close()

print()
print("Done!")
print(f"Created: {OUTPUT_FILE}")
print(f"Size: {os.path.getsize(OUTPUT_FILE) / (1024 * 1024):.2f} MB")