def get_similar_listings(base_listing):
    similar_qs = base_listing.__class__.objects.filter(
        car__make=base_listing.car.make,
        car__model=base_listing.car.model,
        car__year=base_listing.car.year
    ).exclude(id=base_listing.id)

    results = []
    for item in similar_qs:
        item.similarity_score = 0.92
        results.append(item)
    return results
